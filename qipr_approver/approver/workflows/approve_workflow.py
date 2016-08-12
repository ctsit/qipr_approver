from functools import reduce

from django.contrib.auth.models import User

from approver.models import Response, Question, Project, Choice
from approver.constants import answer_submit_names, answer_response_names
from approver.utils import get_current_user_gatorlink, after_approval

def add_update_response(post_data, session):
    """
    This function is responsible for updateing responses as a user is
    filling out the project approver form, ajax-style.
    This is important because we want the user to not lose work as
    they are going along but we also dont want the page refreshing constantly

    Also this function is used by the form update so we dont duplicate code
    """
    api_response = {}

    question_id = int(post_data.get(answer_submit_names.get('question_id')))
    project_id = int(post_data.get(answer_submit_names.get('project_id')))
    choice_id = int(post_data.get(answer_submit_names.get('choice_id')))
    editing_user_gatorlink = get_current_user_gatorlink(session)
    editing_user = User.objects.get(username=editing_user_gatorlink)

    question = Question.objects.get(id=question_id)
    project = Project.objects.get(id=project_id)
    choice = Choice.objects.get(id=choice_id)
    response = Response.objects.filter(question=question, project=project, user=editing_user)

    if len(response) is 0:
        new_response = Response(question=question, project=project, choice=choice, user=editing_user)
        new_response.save(editing_user)
        api_response[answer_response_names.get('response_id')] = new_response.id
        api_response[answer_response_names.get('newly_created')] = 'true'
    elif len(response) is 1:
        response[0].choice = choice
        response[0].save(editing_user)
        api_response[answer_response_names.get('response_id')] = response[0].id
        api_response[answer_response_names.get('newly_created')] = 'false'

    api_response[answer_response_names.get('user_id')] = editing_user.id
    api_response[answer_response_names.get('question_id')] = question_id
    api_response[answer_response_names.get('choice_id')] = choice_id
    api_response[answer_response_names.get('project_id')] = project_id

    return api_response

def save_project_with_form(project, question_form, session):
    """
    Calls the api method to add responses
    Builds a proper call from a project, question_form, and session
    """
    form_fields = question_form.keys()
    for key in form_fields:
        if 'question' in str(key):
            data = {
                answer_submit_names['question_id']: str(key).split('_')[1],
                answer_submit_names['choice_id']: question_form[str(key)],
                answer_submit_names['project_id']: project.id,
            }
            add_update_response(data, session)
    return project

def approve_or_next_steps(project, user):
    responses = project.response.all()
    is_valid = reduce(lambda acc,response : acc and response.is_valid(), responses, True)
    if is_valid:
        project.approve(user)
    return after_approval(project)

