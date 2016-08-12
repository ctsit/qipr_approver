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
    question_choice_ids = __get_question_choice_id(question_form)
    for item in question_choice_ids:
        data = {
            answer_submit_names['question_id']: item[0],
            answer_submit_names['choice_id']: item[1],
            answer_submit_names['project_id']: project.id,
        }
        add_update_response(data, session)
    return project

def __get_question_choice_id(question_form):
    """
    Used by save_project_with_form to break the question choice form
    data into a tuple of ids that can be used to find the right item
    """
    answers = []
    ids = []
    for key in question_form.keys():
        if 'question' in key:
            answers.append(key)
    for answer in answers:
        question_and_choice = answer.split('__')
        question_id = question_and_choice[0].split('_')[1]
        choice_id = question_and_choice[1].split('_')[1]
        ids.append((question_id, choice_id))
    return ids

def approve_or_next_steps(project, user):
    responses = project.response.all()
    is_correct_response = reduce(lambda acc,response : acc and response.is_correct_response(), responses, True)
    if is_correct_response:
        project.approve(user)
    return after_approval(project)

