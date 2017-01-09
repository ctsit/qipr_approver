import approver.parsers.project_spreadsheet.actions as line_actions

def load_projects(argv):
    filename = argv[2]
    stream_parse(filename)

def stream_parse(filename):
    with open(filename, 'r') as file:
        accumulator = None
        count = 0
        for line in file:
            print()
            accumulator = reduce_by_line(accumulator, line, count)
            count += 1
        print()
        print('===========DONE============')

def reduce_by_line(accumulator, line, count):
    # determine what we need to do by the type of line
    print(line.strip(), end="", flush=True)
    actions = line_actions.actions

    func = actions[('data' if count != 0 else 'header')]

    if func != None:
        accumulator = func(accumulator, line)

    return accumulator

