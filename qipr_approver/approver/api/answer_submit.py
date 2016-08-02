from django.http import JsonResponse

from approver.workflows import approve_workflow
from approver.constants import answer_submit_names, answer_response_names

def answer_submit(request):
    if request.method == 'GET':
        api_data = {
            'request': {
                'question_id': 'number',
                'choice_id': 'number',
                'project_id': 'number'
            },
            'response': {
                'user_id': 'number',
                'question_id': 'number',
                'choice_id': 'number',
                'project_id': 'number',
                'response_id': 'number',
                'newly_created': 'boolean',
            }
        }
        return JsonResponse(api_data)

    elif request.method == 'POST':
        api_data = approve_workflow.add_update_response(request.POST, request.session);
        return JsonResponse(api_data)

