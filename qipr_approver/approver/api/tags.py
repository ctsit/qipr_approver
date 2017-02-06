from django.http import JsonResponse
from django.db.models import Q

from functools import reduce

from approver.utils import get_model_from_string

import operator

def tags(request):
    if request.method == 'POST':
        #Get the string passed back and search for the right data
        search_value = request.POST.get('tagString')
        filter_fields = request.POST.get('filter_field').split(";")
        model_name = request.POST.get('model_name')
        model = get_model_from_string(model_name)
        #exclude_tags = request.POST.get('exclude_tags').split(";") request should have this

        #call out and search the model database for values that are similar to passed string
        matches = list_top_matches(model, search_value, filter_fields)

        display = [get_string(match) for match in matches]

        model_props = [{'tag':getattr(model, model.tagged_with), 'guid':model.guid} for model in matches]

        data = get_data(display, model_props, model_name)

        return JsonResponse(data, safe=False)

def list_top_matches(model, search_value, filter_fields,qty=10):
    """
    Given a model, a search_value to search on, and a filter_field to search on,
    build a query which will match objects. Exclude tags which may be found in the results,
    and limit the result set to the quantity given

    Args:
    model: A model object from Models
    search_value: A string to do the lookup on
    filter_fields: A list of fields found on the model to search the value on
    qty: OPTIONAl- Limit the results to this many, default 10
    """
    filters = []
    for filter_field in filter_fields:
        filters.append((filter_field + '__icontains',search_value))
    q_objects = [Q(each) for each in filters]
    matches = model.objects.filter(reduce(operator.or_,q_objects))
    return matches[:qty]

def get_string(model):
    return str(model)

def get_data(display, model_props, model_name):
    data = []
    for index, item in enumerate(display):
        data.append({
            'display': display[index],
            'model_name': model_name,
            'guid': model_props[index]['guid']
        })
    return data
