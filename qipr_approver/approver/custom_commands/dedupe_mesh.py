from itertools import chain

from django.db.models import Q

from approver.models import Descriptor, User
from approver.constants import fixture_username

def dedupe_mesh(argv):
    """
    Removes duplicated mesh keywords and makes sure that the right ones
    are attached to the right spots
    """
    fixture_user = User.objects.get(username=fixture_username)

    # handles the condensing of in use keywords
    q1 = Q(projects__isnull=False)
    q2 = Q(persons__isnull=False)
    used_keywords = Descriptor.objects.filter(q1 | q2)

    seen = {}
    for item in used_keywords:
        if (not seen.get(item.mesh_heading)):
            seen[item.mesh_heading] = item
        else:
            keep = seen[item.mesh_heading]
            keep.projects.set(chain(keep.projects.all(), item.projects.all()))
            keep.persons.set(chain(keep.persons.all(), item.persons.all()))
            keep.save(fixture_user)
            item.delete(fixture_user)
    del used_keywords
    print("In use keywords condensed and deduped!")

    # handles the deletion of duplicates
    q1 = Q(projects__isnull=True)
    q2 = Q(persons__isnull=True)
    not_used = Descriptor.objects.filter(q1 & q2)

    seen = {}
    for item in not_used:
        if (not seen.get(item.mesh_heading)):
            seen[item.mesh_heading] = item
        else:
            item.delete(fixture_user)
    print("Not in use keywords deduped!")
    print("=================DONE===================")
