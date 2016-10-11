from django.http import JsonResponse, HttpResponse, QueryDict
from approver.utils import get_model_from_string

def tags(request):
    if request.method == 'POST':
        #Get the string passed back and search for the right data
        search_value = request.POST.get('tagString')
        filter_field = request.POST.get('filter_field')
        exclude_tags = request.POST.get('exclude_tags').split(";")
        model_name = request.POST.get('model_name')
        model = get_model_from_string(model_name)

        #call out and search the model database for values that are similar to passed string
        ten_matches = list_top_ten_matches(model, search_value, filter_field, exclude_tags)
        listv=[]
        for matches in ten_matches:
            listv.append(matches.get(filter_field))

        return JsonResponse(listv, safe=False)
    else:
         return HttpResponse("Hello Get")


def list_top_ten_matches(model, search_value, filter_field, exclude_tags=[]):
    model_filter = filter_field + '__icontains'
    exclude_filter = filter_field + '__in'
    return_list = model.objects.filter(**{ model_filter: search_value}).values(filter_field)
    if(exclude_tags):
        return_list = return_list.exclude(**{exclude_filter: exclude_tags})
    return return_list[:10]
