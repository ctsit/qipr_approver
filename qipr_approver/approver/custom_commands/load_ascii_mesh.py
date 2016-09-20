from approver.models import *
import approver.parsers.mesh_ascii.actions as mesh_actions

def load_ascii_mesh(argv):
    filename = argv[2]
    stream_parse(filename)

def stream_parse(filename):
    with open(filename, 'r') as file:
        accumulator = None
        for line in file:
            print()
            accumulator = reduce_by_line(accumulator, line)

def reduce_by_line(accumulator, line):
    # determine what we need to do by the type of line
    split_line = line.split('=')
    LHS = split_line[0].strip()
    print(LHS, end="", flush=True)
    RHS = None
    if len(split_line) > 1:
        RHS = split_line[1].strip()
    # map to different functions based on what we need to do
    actions = mesh_actions
    # return that return value
    func = actions.get(LHS)
    if func != None:
        return func(accumulator, RHS)
    else:
        return accumulator


