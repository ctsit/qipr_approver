
from django.contrib import auth
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.conf import settings
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.utils import timezone

from approver.models import Person, Address
from approver import utils


class ApproverShibbolethMiddleware():
    header = "REMOTE_USER"
    force_logout_if_no_header = True

    def __init__(self, get_response):
        self.get_response = get_response
        if not settings.SHIB_ENABLED:
            raise MiddlewareNotUsed

    def __call__(self, request):
    # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if self.force_logout_if_no_header and request.user.is_authenticated:
                self._remove_invalid_user(request)

            return self.get_response(request)

        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            if request.user.get_username() == self.clean_username(username, request):
                return self.get_response(request)

            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(remote_user=username)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            created = self.update_or_create_person(request)
            request.session['IS_NEW_PERSON'] = created
            user.save()
            auth.login(request, user)

        response = self.get_response(request)
        return response

    def update_or_create_person(self, request):
        #creates a new person        #add fake shib variables here
        created = False
        defaults={
                'first_name':request.META['HTTP_GIVENNAME'],
                'last_name':request.META['HTTP_SN'],
                'gatorlink':request.META['HTTP_GLID'],
                'email_address':request.META['HTTP_MAIL'],
                'last_login_time': timezone.now(),
                'account_expiration_time':utils.get_account_expiration_date(timezone.now()),
                }

        try:
            person = Person.objects.get(user=request.user)
            for field, value in defaults.items():
               setattr(person, field, value)
            person.save(request.user)
        except Person.DoesNotExist:
            person = Person(**defaults)
            person.user = request.user
            person.save(request.user)
            created = True

        self._add_person_address(request, person)
        return created

    def _add_person_address(self, request, person):
        ADDRESS1 = 0
        CITY = 1
        STATE = 2
        ZIPCODE = 3
        address_string = request.META.get('HTTP_POSTALADDRESS')
        if address_string:
            address_parts = address_string.split('$')
            address_params = {'address1':address_parts[ADDRESS1],
                              'city':address_parts[CITY],
                              'state':address_parts[STATE],
                              'zip_code':address_parts[ZIPCODE],}

            address = Address(**address_params)
            address.person = person
            address.save(person.user)

    def _remove_invalid_user(self, request):
        """
        Removes the current authenticated user in the request which is invalid
        but only if the user is authenticated via the RemoteUserBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImportError:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, RemoteUserBackend):
                auth.logout(request)


    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username
