from django.http import JsonResponse, HttpResponse
from approver.utils import get_model_from_string

def tags(request):
    if request.method == 'POST':
        #Get the string passed back and search for the right data
        postedValue = request.POST.get('tagString')
        nodeName = request.POST.get('dataName')
        model = get_model_from_string(nodeName)

        #call out and search the model database for values that are similar to passed string
        ten_matches = list_top_ten_matches(model, postedValue)
        listv=[]
        for matches in ten_matches:
            listv.append(matches.get('name'))

        return JsonResponse(listv, safe=False)
    else:
         return HttpResponse("Hello Get")


def list_top_ten_matches(model, search):
    return model.objects.filter(name__icontains=search).values('name')[:10]
