from django.http import JsonResponse

def index(request):
    apidata = {
        'routes': ['api', 'api/users', 'api/projects']
    }
    return JsonResponse(apidata)
