from os import remove
from xml.etree import ElementTree as ET

all_commands = [
    'loadmesh',
]

def loadmesh(argv):
    filename = argv[2]
    if not ('.xml' in filename):
        print('Pass the xml file to be parsed as the third arg')
        return
    stream_parse(filename)

def stream_parse(filename):
    count = 0
    with open(filename, 'r') as file:
        temp_file_name = 'temp_file.xml'
        temp_file = open(temp_file_name, 'w')
        writing = False
        for line in file:
            if contains_opening_tag(line) and writing == False:
                writing = True
                temp_file = open(temp_file_name, 'w')
                temp_file.write(line)
            elif writing == True and not contains_closing_tag(line):
                temp_file.write(line)
            elif writing == True and contains_closing_tag(line):
                print('.', end='', flush=True)
                count = count + 1
                temp_file.write(line)
                temp_file.close()
                writing = False
                parse_temp_file(temp_file_name)
                remove(temp_file_name)
    print('Parsed {} nodes'.format(count))

def contains_tag(tags, line):
    for tag in tags:
        if tag in line:
            return True
    return False

def contains_opening_tag(line):
    tags = [
        '<DescriptorRecord ',
        '<QualifierRecord ',
        '<SupplementaryRecord ',
    ]
    return contains_tag(tags, line)

def contains_closing_tag(line):
    tags = [
        '</DescriptorRecord>',
        '</QualifierRecord>',
        '</SupplementaryRecord>',
    ]
    return contains_tag(tags, line)

def parse_temp_file(temp_file_name):
    tree = ET.parse(temp_file_name)
    root = tree.getroot()
    """
    parsers = {
        "DescriptorRecord": parse_descriptors,
        "QualifierRecord": parse_qualifiers,
        "SupplementaryRecord": parse_scr,
    }
    parsers.get(root.tag)(root)
    """
    pass
