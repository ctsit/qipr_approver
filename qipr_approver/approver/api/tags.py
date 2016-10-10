from django.http import JsonResponse, HttpResponse, QueryDict
from approver.utils import get_model_from_string

def tags(request):
    if request.method == 'POST':
        #Get the string passed back and search for the right data
        search_value = request.POST.get('tagString')
        filter_field = request.POST.get('filter_field')
        model_name = request.POST.get('model_name')
        model = get_model_from_string(model_name)

        #call out and search the model database for values that are similar to passed string
        ten_matches = list_top_ten_matches(model, search_value, filter_field)
        listv=[]
        for matches in ten_matches:
            listv.append(matches.get(filter_field))

        return JsonResponse(listv, safe=False)
    else:
         return HttpResponse("Hello Get")


def list_top_ten_matches(model, search_value, filter_field):
    filter = filter_field + '__icontains'
    return model.objects.filter(**{ filter: search_value}).values(filter_field)[:10]
