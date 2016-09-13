from os import remove
from xml.etree import ElementTree as ET

from approver.parsers import parse_desc_xml, parse_qual_xml, parse_supp_xml
from approver.models import User

def loadmesh(argv):
    filename = argv[2]
    if not ('.xml' in filename):
        print('Pass the xml file to be parsed as the third arg')
        return
    stream_parse(filename)

def stream_parse(filename):
    count = 0
    user = User.objects.get(username='admin_fixture_user')
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
                model = parse_temp_file(temp_file_name)
                model.save(user)
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
    """
    Parses a file that should contain one mesh node that is either
    a descriptor, qualifier ot supplementary record
    returns a model instance.
    """
    tree = ET.parse(temp_file_name)
    root = tree.getroot()
    parsers = {
        "DescriptorRecord": parse_desc_xml,
        "QualifierRecord": parse_qual_xml,
        "SupplementaryRecord": parse_supp_xml,
    }
    return parsers.get(root.tag)(tree)

