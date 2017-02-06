from itertools import chain

from django.db.models import Q

from approver import utils
from approver.models import Person, Contact

def add_contact_for_person(person, user):
    contact = Contact(business_email=person.email_address, first_name=person.first_name, last_name=person.last_name)
    contact.person = person
    contact.save(user)
    return contact

def get_collaborators_from_form(form, user):
    return __process_tags_get_people(form, 'collaborator', user)

def get_advisors_from_form(form, user):
    return __process_tags_get_people(form, 'advisor', user)

def __process_tags_get_people(form, prop, user):
    """
    Using the form data tags we get back this function gets the right
    person object

    Possibilities:
    ---------------
    1. tag is never before seen email => make new contact and person
    2. tag is contact guid => get matching contact and make new person from that
    3. tag is person guid => get matching person

    return the right people
    """
    tags = __process_tags(form, prop)

    new_contacts = [tag for tag in tags if __is_email(tag)]
    new_contact_people = __handle_email_tags(new_contacts, user)

    # dealt with new contacts
    tags = [tag for tag in tags if not (tag in new_contacts)]

    # now we have guid tags only
    filter_object = __get_filter_object(tags)

    contact_matches = [model for model in Contact.objects.filter(filter_object).select_related('person')]
    person_matches = [model for model in Person.objects.filter(filter_object)]

    people_from_contacts = __handle_contact_matches(contact_matches, user)

    return list(chain(new_contact_people, people_from_contacts, person_matches))

def __process_tags(form, prop):
    """
    Gets the tags ready for use.

    Parses form tag field
    cleans the tag of the "NEW::" identifier
    filters out tags that are not emails or guids

    returns list of correct tag strings
    """
    tags = utils.extract_tags(form, prop)
    cleaned = [__clean_tag(tag) for tag in tags]
    valid = [tag for tag in cleaned if __is_valid(tag)]

    return valid

def __clean_tag(tag):
    """
    This identifier is in the javascript app.js as well
    """
    # return tag.replace('NEW::', '').replace(';', '')
    return utils.clean_tag(tag)

def __is_valid(tag):
    """
    Valid if is email and is guid
    """
    if __is_email(tag):
        return tag
    elif utils.is_guid(tag):
        return tag
    else:
        return None

def __is_email(tag):
    if '@' in tag:
        return tag

def __handle_email_tags(tags, user):
    new_people = []
    for tag in tags:
        contact = Contact(business_email=tag)
        new_people.append(__new_person_from_contact(contact, user))
    return new_people

def __new_person_from_contact(contact, user):
    person = contact.new_person()
    person.save(user)
    contact.person = person
    contact.save(user)
    return person

def __get_q(tag):
    return Q(guid=tag)

def __get_filter_object(tags):
    """
    Or's together a bunch of Q objects to get a more efficient query
    """
    tag_qs = [__get_q(tag) for tag in tags]
    accumulator = Q(guid='None')
    for q in tag_qs:
        accumulator |= q
    return accumulator

def __handle_contact_matches(contacts, user):
    people = []
    for contact in contacts:
        if contact.person:
            people.append(contact.person)
        else:
            people.append(__new_person_from_contact(contact, user))

    return people
