from django.contrib.auth.models import User
from approver.models import *

fixture_user = User.objects.get('admin_fixture_user')

def load_ascii_mesh(argv):
    filename = argv[2]
    stream_parse(filename)

def stream_parse(filename):
    with open(filename, 'r') as file:
        accumulator = None
        for line in file:
            accumulator = reduce_by_line(accumulator, line)

def reduce_by_line(accumulator, line):
    # determine what we need to do by the type of line
    split_line = line.split('=')
    LHS = split_line[0].strip()
    RHS = split_line[1].strip()
    # map to different functions based on what we need to do
    actions = import approver.parsers.mesh_ascii.actions
    # return that return value
    return actions[LHS](accumulator, RHS)


