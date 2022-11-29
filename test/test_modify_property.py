import os
import unittest
from modify_property import modify_property 


class test_modify_property(unittest.TestCase):
    def test_modify_was_attributed_to(self):
        src = os.path.join('test', 'data', 'jsonld')
        dst = os.path.join('test', 'modify_property')
        modify_property(src, dst, 'was_attributed_to', 'jsonld', 'https://orcid.org/0000-0002-8420-0696', 'https://w3id.org/oc/meta/prov/pa/1')