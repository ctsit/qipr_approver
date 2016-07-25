from approver.models import Person, Speciality
from approver.constants import SESSION_VARS
from approver.utils import extract_tags, update_tags

from django.contrib.auth.models import User
from django.utils import timezone

def create_new_user_from_current_session(session):
    """
    This function creates a user from the session after shib validates
    """
    now = timezone.now()

    new_user = User(username=session.get(SESSION_VARS['gatorlink']),
                    email=session.get(SESSION_VARS['email']),
                    last_login=now,
                    last_name=session.get(SESSION_VARS['last_name']),
                    first_name=session.get(SESSION_VARS['first_name']))

    new_user.save()

    new_person = Person(user=new_user,
                        first_name=new_user.first_name,
                        last_name=new_user.last_name,
                        email_address=new_user.email,
                        last_login_time=now)

    new_person.save(last_modified_by=new_user)

    return new_user

def update_user_from_about_you_form(user, about_you_form, editing_user):
    """
    This function changes an existing (user,person) entry
    based on the information in the about_you_form.
    This will not work if the (user,person) does not yet
    exist.
    """
    now = timezone.now()
    person = user.person

    user.username = about_you_form.get('user_name')
    user.first_name = about_you_form.get('first_name')
    user.last_name = about_you_form.get('last_name')
    user.email = about_you_form.get('email')

    person.first_name = about_you_form.get('first_name')
    person.last_name = about_you_form.get('last_name')
    person.email_address = about_you_form.get('email')
    person.business_phone = about_you_form.get('business_phone') or 0
    person.contact_phone = about_you_form.get('contact_phone') or 0
    person.webpage_url = about_you_form.get('webpage_url')

    specialities = extract_tags(about_you_form, 'speciality')

    update_tags(model=person,
                tag_property='speciality',
                tags=specialities,
                tag_model=Speciality,
                tagging_user=editing_user)

    user.save()
    person.save(last_modified_by=editing_user)

    return person

