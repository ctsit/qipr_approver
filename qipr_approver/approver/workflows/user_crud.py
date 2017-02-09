from approver.models import Person, Speciality, Descriptor, QI_Interest, Suffix, Address, Organization, ClinicalArea, Self_Classification
from approver.constants import SESSION_VARS, ADDRESS_TYPE
from approver.utils import extract_tags, update_tags, true_false_to_bool, extract_model

from django.contrib.auth.models import User
from django.utils import timezone
from approver import utils
from approver.workflows.contact_person import add_contact_for_person

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
                        gatorlink=new_user.username,
                        first_name=new_user.first_name,
                        last_name=new_user.last_name,
                        email_address=new_user.email,
                        last_login_time=now,
                        account_expiration_time=utils.get_account_expiration_date(now))

    new_person.save(last_modified_by=new_user)

    return new_user

def check_changed_contact(person, form):
    new_email_address = form.get('email')
    new_first_name = form.get('first_name')
    new_last_name = form.get('last_name')
    if new_email_address != person.email_address:
        return True
    if new_first_name != person.first_name:
        return True
    if new_last_name != person.last_name:
        return True
    return False

def update_user_from_about_you_form(person, about_you_form, editing_user):
    """
    This function changes an existing (user,person) entry
    based on the information in the about_you_form.
    This will not work if the (user,person) does not yet
    exist.
    """
    now = timezone.now()

    changed_contact = check_changed_contact(person, about_you_form)

    person.business_phone = about_you_form.get('business_phone') or None
    person.contact_phone = about_you_form.get('contact_phone') or None
    person.email_address = about_you_form.get('email')
    person.first_name = about_you_form.get('first_name')
    person.last_name = about_you_form.get('last_name')
    person.webpage_url = about_you_form.get('webpage_url')
    person.title = about_you_form.get('title')
    person.department = about_you_form.get('department')
    person.qi_required = about_you_form.get('qi_required')
    person.training = about_you_form.get('training_program')
    person.self_classification = extract_model(Self_Classification, "name", about_you_form.get('select-self_classification') or '')
    if (about_you_form.get('select-self_classification') == 'other'):
        person.other_self_classification = about_you_form.get('other_classification')
    else:
        person.other_self_classification = None

    clinical_area = extract_tags(about_you_form, 'clinical_area')
    expertises = extract_tags(about_you_form, 'expertise')
    qi_interest = extract_tags(about_you_form, 'qi_interest')
    specialities = extract_tags(about_you_form, 'speciality')
    suffixes = extract_tags(about_you_form, 'suffix')

    person = update_tags(model=person,
                tag_property='expertise',
                tags=expertises,
                tag_model=Descriptor,
                tagging_user=editing_user)

    person = update_tags(model=person,
                tag_property='qi_interest',
                tags=qi_interest,
                tag_model=QI_Interest,
                tagging_user=editing_user)

    person = update_tags(model=person,
                tag_property='speciality',
                tags=specialities,
                tag_model=Speciality,
                tagging_user=editing_user)

    person = update_tags(model=person,
                tag_property='suffix',
                tags=suffixes,
                tag_model=Suffix,
                tagging_user=editing_user)

    person = update_tags(model=person,
                tag_property='clinical_area',
                tags=clinical_area,
                tag_model=ClinicalArea,
                tagging_user=editing_user)

    save_address_from_form(about_you_form, editing_user, ADDRESS_TYPE['business'], person)
    person.save(last_modified_by=editing_user)
    if changed_contact:
        add_contact_for_person(person, editing_user)
    return person

def save_address_from_form(form, user, address_type, person=None, organization=None):
    """
    This function will take a form and save address data found in it.

    This function uses the following values:
    * form: the form from the address.html template
    * user: the current user
    * address_type: the type of address found in constants.ADDRESS_TYPE
    * person: the person who is assigned this address
    * organiztion: the organiztion which is assigned this address
    """

    address1_list = form.getlist('address1_' + address_type)
    address2_list = form.getlist('address2_' + address_type)
    city_list = form.getlist('city_' + address_type)
    state_list = form.getlist('state_' + address_type)
    zip_code_list = form.getlist('zip_code_' + address_type)
    country_list = form.getlist('country_' + address_type)
    address_id_list = form.getlist('address_id_' + address_type)

    zipped_address_values = zip(
        address1_list,
        address2_list,
        city_list,
        state_list,
        zip_code_list,
        country_list,
        address_id_list
    )

    __save_each_address_tuple(zipped_address_values, user, person, organization)

def __save_each_address_tuple(address_values, user, person=None, organization=None):
    """
    This function will save the addresses generated in the save_address_from_list function
    """
    ADDRESS1 = 0
    ADDRESS2 = 1
    CITY = 2
    STATE = 3
    ZIP_CODE = 4
    COUNTRY = 5
    ADDRESS_ID = 6

    for values in address_values:
        address=Address.objects.get(id=values[ADDRESS_ID]) if values[ADDRESS_ID] else Address()
        address.address1=values[ADDRESS1]
        address.address2=values[ADDRESS2]
        address.city=values[CITY]
        address.state=values[STATE]
        address.zip_code=values[ZIP_CODE]
        address.country=values[COUNTRY]
        address.person=person
        address.organization=organization

        address.save(user)
