## setting up PyYAML parser/dumper for xml2yaml

import yaml
from collections import OrderedDict

####### LITERAL BLOCKS

class LiteralString(str):
    pass

def literal_block_style(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")

####### PLAIN INT

class PlainInt(str):
    pass

def plain_int_style(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:int", data, style=None)

####### PLAIN STRING

# Create a custom string class for plain strings
class PlainString(str):
    pass

def plain_string_style(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=None)

####### SINGLE QUOTED STRING

class SingleQuotedString(str):
    pass

def single_quoted_style(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="'")

####### LIST

class PlainList(list):
    pass

def represent_list(dumper, data):
    """
    Custom representer for rendering lists with square brackets
    """
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

####### ORDERED_DICT

def represent_ordereddict(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


####### REGISTRATION

# Register the custom representer for OrderedDict
yaml.add_representer(OrderedDict, represent_ordereddict)
yaml.add_representer(LiteralString, literal_block_style)
yaml.add_representer(SingleQuotedString, single_quoted_style)
yaml.add_representer(PlainInt, plain_int_style)
yaml.add_representer(PlainString, plain_string_style)
yaml.add_representer(PlainList, represent_list)