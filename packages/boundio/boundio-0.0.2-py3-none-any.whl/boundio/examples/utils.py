import re

beginning = re.compile(r'^[\s\S]+?\n\n')
def get_example_code(path): # Remove the section that gets the example code as an attribute from the example itself.
    with open(path,'r') as f:
        txt = f.read()
    return beginning.sub('',txt)
