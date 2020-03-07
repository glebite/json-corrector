"""

json data is sometimes corrupt...

One place where json data gets corrupted is with lists that are 
not properly quoted. 

The first fix here is to try to solve these problems where:

{..., "label": [somestring, someother-string, another-string], ...}

Reading this will cause json parsers a pain in the butt.

Python's json parser will just throw an error.

simplejson is awesome - it will report some error information to 
help the developer to understand where the error is in the data.

It does not correct this kind of error.  This module should assist 
in some cleaning of improperly formed json data to allow the 
living to get on with their life.

The one pattern being solved here is missing quotes for list 
entries.

"""
import simplejson
import re


class Corrector:
    """
    Corrector
    """
    def __init__(self, file_name):
        """ __init__ """
        self.fileName = file_name
        self.data = None

    def load_data(self):
        """ load_data """
        with open(self.fileName, 'r') as file_pointer:
            self.data = file_pointer.read()

    def validate_data(self):
        """ validate_data """
        try:
            self.json = simplejson.loads(self.data)
        except Exception as e:
            raise TypeError(e)

    def cleans_pattern_one(self):
        """ cleans_pattern_one """
        finds = re.findall('\[([a-z0-9\-]*)', self.data)
        for thing in finds:
            if thing:
                result = re.sub(r'\[{}'.format(thing), '[\"{}\"'.format(thing), self.data)
        if result:
            self.data = result
        return result
                
    def cleans_pattern_two(self):
        """ cleans_pattern_two """
        finds = re.findall('([a-z0-9\-]*)\]', self.data)
        for thing in finds:
            if thing:
                result = re.sub(r'{}\]'.format(thing), '"{}\"]'.format(thing), self.data)
        if result:
            self.data = result
        return result

    def cleans_pattern_three(self):
        """ cleans_pattern_three """
        finds = re.findall(r'\[([A-Z]*)', self.data)
        for thing in finds:
            if thing:
                result = re.sub(r'\[{}'.format(thing), '["{}"'.format(thing), self.data)
        if result:
            self.data = result
        return result

    
if __name__ == "__main__":
    c = Corrector('/home/paul/Downloads/api-docs.json')
    c.load_data()
    c.cleans_pattern_one()
    x = c.cleans_pattern_two()
    x = c.cleans_pattern_three()
    try:
        c.validate_data()
        print("Passed")
    except TypeError as e:
        print(e)
