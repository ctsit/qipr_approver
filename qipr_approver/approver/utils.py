from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

import datetime

import approver.constants as constants

def user_exists(about_you_form):
    """
    Returns True if user exists, and False otherwise given an
    about_you_form
    """
    return (len(User.objects.filter(username=about_you_form.get('user_name'))) != 0)

def layout_render(request, context):
    """
    This function should be used in place of render.
    It adds context['content'] into the layout.html so that the nav bar is
    present as well as css and javascript
    """
    return render(request, 'approver/layout.html', context)

def get_current_user_gatorlink(session):
    """
    Gets the current user's gatorlink
    We don't return the user here because the util file shall
    not have a dependency on the models
    """
    return session.get(constants.SESSION_VARS['gatorlink'])

def get_and_reset_toast(session):
    toast = session.get("toast_text")
    session['toast_text'] = ''
    return toast

def dashboard_redirect_and_toast(request, toast_text):
    request.session['toast_text'] = toast_text
    return redirect(reverse("approver:dashboard"))

def set_created_by_if_empty(model, user):
    """
    This function is called by our save function because django
    throws exceptions on object access if something doesn't exist.
    You cannot dereference a related field if it doesn't exist.
    Meaning you have to do a try except block.
    """
    try:
        # the following line throws an exception
        model.created_by is not None
    except:
        model.created_by = user

def format_date(date):
    """
    This format date is used with the date picker. It has to be in a
    particular form in order to work
    """
    date_parts = [date.year, date.month, date.day]
    return '/'.join([str(part) for part in date_parts])

def extract_tags(form, tag_field_name):
    """
    This function extracts the tags from a form and returns
    a list of their names.
    """
    invisible_space = u"\u200B"
    split_character = ';'
    tags = form.get(tag_field_name)
    tags = tags.split(';')
    for tag in tags:
        if tag == '':
            tags.remove('')
    return [tag.replace(invisible_space, '') for tag in tags]

def model_matching_tag(tag_text, model_class, current_user, matching_property=None):
    """
    This returns the model where
    model_class.objects.filter(model_class.tag_property_name=tag_text)
    or
    model_class.objects.filter(matching_property=tag_text)
    if no model matches, make a new one with the current_user
    if more than one model exists, return None
    """
    filter_against = matching_property or model_class.tag_property_name
    models = model_class.objects.filter(**{filter_against: tag_text})

    if len(models) is 1:
        return models[0]

    elif len(models) is 0:
        model = model_class()
        setattr(model, filter_against, tag_text)
        model.save(current_user)
        return model

    else:
        return None

def update_tags(model, tag_property, tags, tag_model, tagging_user):
    """
    Given a model to update,
    a model.tag_property to change,
    a list of strings called tags to add,
    a tag_model to which those tags belong,
    and a tagging_user who is doing the tagging
    This function will add those tags to the model by
    the tagging user and create new tag_models if the
    particular tag does not exist

    if any tag matches against more than one model as determined
    by tag_model.tag_property_name, those models will NOT be added
    """
    taggable = getattr(model, tag_property)
    taggable.clear()

    tag_models = [model_matching_tag(tag, tag_model, tagging_user) for tag in tags]

    for tag in tag_models:
        if isinstance(tag, tag_model):
            taggable.add(tag)

    model.save(tagging_user)

#Get Data from Project for the given field
def get_related_or_empty(modelname,field): 
    return [item.name for item in getattr(modelname,field).all()] if getattr(modelname,'title') else []