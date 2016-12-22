import hashlib

from django.db import models
from django.contrib.auth.models import User

from approver.models import Person

def get_hash(ua_string):
    return hashlib.md5(ua_string).hexdigest()

class UserAgent(models.Model):
    """
    Used for storing user agents in the access log.
    Though unlikely, hashes may not be unique, when doing a lookup
    use the hash and keep it around.
    """
    ua_string = models.TextField()
    ua_hash = models.CharField(max_length=32, null=False, editable=False)

    def save(self, *args, **kwargs):
        if not self.ua_hash:
            self.ua_hash = get_hash(self.ua_string)
        super(UserAgent, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("id", "ua_hash")

class AccessLog(models.Model):
    """

    name: the name of the tag
    description: the developer's way of understanding the tag
    __str__: Inherited from the TagPrint class
    tag_property_name: always of value 'name'
    get_natural_dict: returns a dictionary describing the tag

    Also Tags are registerable with the registry
    """
    time_requested = models.DateTimeField(auto_now_add=True,editable=False)
    time_responded = models.DateTimeField(auto_now=True)
    gatorlink = models.CharField(max_length=50, null=True)
    ip = models.GenericIPAddressField()
    previous_log = models.ForeignKey('self', null=True, related_name="next_log")
    url = models.TextField()
    user_agent = models.ForeignKey(UserAgent, related_name="+")
    http_verb = models.CharField(max_length=10)
    request_body = models.TextField(null=True)
    response_code = models.IntegerField(null=True)

    def add_user_agent(self, ua_string):
        ua_hash = get_hash(ua_string)
        agents = UserAgent.objects.filter(ua_hash=ua_hash)
        agent = None
        if len(agents) == 1:
            agent = agents[0]
        else:
            for each in agents:
                if each.ua_string == ua_string:
                    agent = each
                    break
        if not agent:
            new_agent = UserAgent(ua_string=ua_string, ua_hash=ua_hash)
            new_agent.save()
            agent = new_agent
        self.user_agent = agent
