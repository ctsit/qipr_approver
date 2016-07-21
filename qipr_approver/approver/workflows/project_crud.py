from approver.models import Person, Project
from approver.constants import SESSION_VARS
import approver.utils as utils

from django.contrib.auth.models import User
from django.utils import timezone

def create_new_project_from_session_title(session, title):
    """
    This function creates a project using user information
    from the current session and a title
    """
    now = timezone.now()
    current_user_gatorlink = utils.get_current_user_gatorlink(session)
    user = User.objects.get(username=current_user_gatorlink)
    person = user.person

    new_project = Project(owner=person, title=title)

    new_project.after_create(user)

    new_project.save(user)

    return new_project

def update_project_from_project_form(project, project_form, editing_user):
    """
    This function changes an existing project entry
    based on the information in the project_form.
    This will not work if the project does not yet
    exist.
    """
    now = timezone.now()

    project.title = project_form.get('title')
    project.description = project_form.get('description')
    project.proposed_start_date = project_form.get('proposed_start_date')
    project.proposed_end_date = project_form.get('proposed_end_date')

    project.save(editing_user)
