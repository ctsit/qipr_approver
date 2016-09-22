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
    print(line.strip(), end="", flush=True)
    actions = mesh_actions

    split_line = line.split('=')

    LHS = split_line[0].strip()
    RHS = split_line[1].strip() if len(split_line) >= 2 else None

    if LHS == '':
        LHS = 'save'

    func = actions.get(LHS)

    if func != None:
        accumulator = func(accumulator, RHS)

    return accumulator
