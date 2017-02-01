import json
import hashlib

from django.core import serializers
from django.contrib.auth.models import User

import requests

import approver.models
from approver.constants import registry_endpoints, api_username, bridge_key

def push_model(model):
    api_user = User.objects.get(username=api_username)
    json_data, req_hash = process_data(model)
    response = None
    url = '/'.join([registry_endpoints.get('add_model'), req_hash])
    try:
        response = requests.post(url, data=json_data)
        if response.status_code == 200 and not model.is_registered():
            model.register()
            model.save(api_user)
    except requests.exceptions.RequestException as e:
        print(e)
    return response

def process_data(model):
    """
    Takes a couple of steps to make the bridge work.

    serializes the model
    adds the model_class_name property for model lookup on the other side
    Adds in a hash with the bridge key for security
    """
    json_data = jsonify(model)
    json_data = add_model_class_name(json_data, model)
    req_hash = get_hash(json_data, bridge_key)
    return json_data, req_hash

def jsonify(model):
    return serializers.serialize('json', [model], use_natural_foreign_keys=True, use_natural_primary_keys=True)

def add_model_class_name(data, model):
    """
    This function adds the model instance's __class__.__name__ property
    to the json before sending it out.

    This is necessary so that the registry knows which module
    from the models package to grab.
    """
    model_dict = json.loads(data)
    model_dict[0]['fields']['model_class_name'] = model.__class__.__name__
    return json.dumps(model_dict)

def get_hash(json_data, bridge_key):
    """
    Adds an md5 hash as hex so the registry can verify add_model validity.
    Meant to be passed as a url parameter
    """
    to_hash = json_data.encode('utf-8') + bridge_key.encode('utf-8')
    return hashlib.md5(to_hash).hexdigest()
