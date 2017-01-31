from django.db.models import Q

import approver.bridge as bridge
from approver.utils import get_model_from_string
from approver.models import PushQueue


def send_push_queue():
    api_user = bridge.get_api_user()

    to_push = PushQueue.objects.all().values('guid','model_name');

    # get all the types of models
    for item in to_push:
        Model = get_model_from_string(item.get('model_name'))
        item['constructor'] = Model

    # group to push based on those models
    mapping = {}
    for item in to_push:
        if not item['model_name'] in mapping.keys():
            mapping[item['model_name']] = []
            mapping[item['model_name']].append(item['guid'])
        else:
            mapping[item['model_name']].append(item['guid'])

    # make Q for each type
    Qs = {}
    for key in mapping:
        Qs[key] = Q()
        for item in mapping[key]:
            Qs[key] |= Q(guid=item)

    # query and send
    pushables = []
    for key in Qs:
        Model = get_model_from_string(key)
        models = Model.objects.filter(Qs[key])
        for model in models:
            response = bridge.send_model(model, api_user)
            if response.status_code != 200:
                bridge.push_model(model)

    PushQueue.objects.all().delete()
