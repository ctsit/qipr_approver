from approver.models import Person, Project, Keyword, ClinicalArea, ClinicalSetting, SafetyTarget, BigAim
from approver.constants import SESSION_VARS
from approver.utils import extract_tags, update_tags
import approver.utils as utils

from django.contrib.auth.models import User
from django.utils import timezone, dateparse

def create_or_update_project(current_user, project_form, project_id=None):
    """
    Creates a new project or updates and existing one using a project form
    """
    project = None
    if project_exists(project_id):
        project = Project.objects.get(id=project_id)
        update_project_from_project_form(project, project_form, current_user)
    else:
        project = create_new_project_from_user_form(current_user, project_form)
    return project

def create_new_project_from_user_form(current_user, form):
    """
    This function creates a project using user information
    from the current session and a title
    """
    now = timezone.now()
    person = current_user.person

    new_project = Project(owner=person, title=form.get('title'))

    new_project.save(last_modified_by=current_user)

    update_project_from_project_form(new_project, form, current_user)

    return new_project

def update_project_from_project_form(project, project_form, editing_user):
    """
    This function changes an existing project entry
    based on the information in the project_form.
    This will not work if the project does not yet
    exist.
    """
    now = timezone.now()
    parse_date = dateparse.parse_date

    project.title = project_form.get('title')
    project.description = project_form.get('description')
    project.proposed_start_date = parse_date(project_form.get('proposed_start_date'))
    project.proposed_end_date = parse_date(project_form.get('proposed_end_date'))

    advisor = extract_tags(project_form, 'advisor')
    big_aim = extract_tags(project_form, 'bigaim')
    clinical_area = extract_tags(project_form, 'clinicalarea')
    clinical_setting = extract_tags(project_form, 'clinicalsetting')
    collaborator = extract_tags(project_form, 'collaborator')
    keyword = extract_tags(project_form, 'keyword')
    safety_target = extract_tags(project_form, 'safetytarget')

    update_tags(model=project,
                tag_property='keyword',
                tags=keyword,
                tag_model=Keyword,
                tagging_user=editing_user)

    update_tags(model=project,
                tag_property='bigaim',
                tags=big_aim,
                tag_model=BigAim,
                tagging_user=editing_user)


    update_tags(model=project,
                tag_property='clinicalarea',
                tags=clinical_area,
                tag_model=ClinicalArea,
                tagging_user=editing_user)

    update_tags(model=project,
                tag_property='clinicalsetting',
                tags=clinical_setting,
                tag_model=ClinicalSetting,
                tagging_user=editing_user)

    update_tags(model=project,
                tag_property='safetytarget',
                tags=safety_target,
                tag_model=SafetyTarget,
                tagging_user=editing_user)

    update_tags(model=project,
                tag_property='collaborator',
                tags=collaborator,
                tag_model=Person,
                tagging_user=editing_user)

    update_tags(model=project,
                tag_property='advisor',
                tags=advisor,
                tag_model=Person,
                tagging_user=editing_user)

    project.save(editing_user)

def get_project_or_none(project_id):
    """
    This returns a project instance if it exists or it returns None
    """
    try:
        project = Project.objects.get(id=project_id)
        return project
    except:
        return None

def project_exists(project_id):
    """
    This returns a boolean for if the project exists or not
    """
    return (len(Project.objects.filter(id=project_id)) > 0)

def curent_user_is_project_owner(current_user, project):
    """
    This returns a boolean about if the current_user.person.id is the
    same as the project.owner.id
    """
    return current_user.person.id == project.owner.id
def current_user_is_project_advisor_or_collaborator(current_user, project):
    """
    This returns a boolean true if the current_user.person.id is in 
    project.advisor or project.collaborator
    """
    for advisor in project.advisor.all():
        if current_user.person.id == advisor.id:
            return True
    for collaborator in project.collaborator.all():
        if current_user.person.id == collaborator.id:
            return True
    return False
def current_user_can_perform_project_delete(current_user,project):
    """
    This returns an error message if user cannot delete the project, returns empty String when
    user is the owner for the project and the project is editable.
    """
    toast_message = ""
    if(toast_message == "" and project is None):
        toast_message = 'Project with id {} does not exist.'.format(project_id)
        return toast_message
    if(toast_message == "" and curent_user_is_project_owner(current_user, project) is not True):
        return 'You are not authorized to delete this project.'
    if (toast_message == "" and project.get_is_editable() is not True):
        return 'You are not allowed to delete/edit this project.'
    project.delete(current_user)
    return 'Deleted Project'
