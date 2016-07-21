from django.http import JsonResponse
from django.core import serializers

from approver.models import Person

def users(request):
    user_data = {
        'users': 'not yet implemented'
    }
    return JsonResponse(user_data)
