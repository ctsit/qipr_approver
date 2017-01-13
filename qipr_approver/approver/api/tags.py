from django.http import JsonResponse, HttpResponse, QueryDict
from approver.utils import get_model_from_string

def tags(request):
    if request.method == 'POST':
        #Get the string passed back and search for the right data
        search_value = request.POST.get('tagString')
        filter_fields = request.POST.get('filter_field').split(";")
        exclude_tags = request.POST.get('exclude_tags').split(";")
        model_name = request.POST.get('model_name')
        model = get_model_from_string(model_name)

        #call out and search the model database for values that are similar to passed string
        matches = list_top_matches(model, search_value, filter_fields, exclude_tags)
        matches = unique_only(matches)

        display = [get_string(match, filter_fields) for match in matches]
        tag_props = [getattr(model, model.tag_property) for model in matches]

        data = get_data(display, tag_props, model_name)

        return JsonResponse(data, safe=False)

def list_top_matches(model, search_value, filter_fields, exclude_tags=[]):
    lists = []
    for filter_field in filter_fields:
        lists.append(model.objects.filter(**{(filter_field + '__icontains'): search_value}))
    for index, results in enumerate(lists):
        results.exclude(**{(filter_fields[index]+'__in'): exclude_tags})
    matches = []
    for list_item in lists:
        for item in list_item:
            matches.append(item)
    return matches[:10]

def get_string(model, fields):
    return str(model)

def unique_only(models):
    return set(models)

def get_data(display, tag_props, model_name):
    data = []
    for index, item in enumerate(display):
        data.append({
            'display': display[index],
            'tag_prop': tag_props[index],
            'model_name': model_name
        })
    return data

