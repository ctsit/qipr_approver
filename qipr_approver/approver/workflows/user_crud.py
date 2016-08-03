from approver.models import Person, Speciality, Expertise, QI_Interest, Suffix, Address
from approver.constants import SESSION_VARS
from approver.utils import extract_tags, update_tags

from django.contrib.auth.models import User
from django.utils import timezone
from django.http import QueryDict

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
    person.business_address = extract_address(about_you_form, 'business', user)

    specialities = extract_tags(about_you_form, 'speciality')
    expertises = extract_tags(about_you_form, 'expertise')
    qi_interest = extract_tags(about_you_form, 'qi_interest')
    suffixes = extract_tags(about_you_form, 'suffix')

    update_tags(model=person,
                tag_property='speciality',
                tags=specialities,
                tag_model=Speciality,
                tagging_user=editing_user)

    update_tags(model=person,
                tag_property='expertise',
                tags=expertises,
                tag_model=Expertise,
                tagging_user=editing_user)

    update_tags(model=person,
                tag_property='qi_interest',
                tags=qi_interest,
                tag_model=QI_Interest,
                tagging_user=editing_user)

    update_tags(model=person,
                tag_property='suffix',
                tags=suffixes,
                tag_model=Suffix,
                tagging_user=editing_user)

    user.save()
    person.save(last_modified_by=editing_user)

    return person

def extract_address(form, address_type, user):
    """
    This function will take a form and return a list of business addresses
    """
    ADDRESS1 = 0
    ADDRESS2 = 1
    CITY = 2
    STATE = 3
    ZIP_CODE = 4
    COUNTRY = 5

    # first need to get list of each of the address fields on the form, probably in the right order
    address1_list = form.getlist('address1_'+address_type,['a1','a2','a3'])
    address2_list = form.getlist('address2_'+address_type)
    city_list = form.getlist('city_'+address_type,['c1','c2','c3'])
    state_list = form.getlist('state_'+address_type,['fl','fl','fl'])
    zip_code_list = form.getlist('zip_code_'+address_type,['32','32','32'])
    country_list = form.getlist('country_'+address_type,['us','us','us'])

    # then we need to pull each of the same position fields from the lists into a new address
    zipped_address_values = zip(address1_list, city_list, state_list, zip_code_list, country_list)

    # for each tupple created, we need to make it an address
    address_list = []
    print("test")
    for values in zipped_address_values:
        print("*****")
        print (values[0], values[1], values[2], values[3], values[4])
        print("***")
        address = Address(
            address1=values[0],
            city=values[1],
            state=values[2],
            zip_code=values[3],
            country=values[4]
            )
        address.save(user)
        address_list.append(address)
        address.pk

    # finally we need to return a list of these addresses
    return address_list

def moc_get_post():
    q = QueryDict(
        'address1_business=444 nw 6th st&address1_business=222 ne 8th st&' \
        'city_business=atlanta&city_business=macon&' \
        'state_business=FL&state_business=FL&' \
        'zip_code_business=32608&zip_code_business=12345&' \
        'country_business=US&country_business=US'
    )

    return q
