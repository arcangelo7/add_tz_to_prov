import json
import os
import unittest
from shutil import rmtree
from zipfile import ZipFile

from modify_property import run


class test_modify_property(unittest.TestCase):
    def test_modify_was_attributed_to(self):
        src = os.path.join('test', 'data', 'jsonld')
        dst = os.path.join('test', 'data', 'jsonld_out')
        run(src, dst, 'https://orcid.org/0000-0002-8420-0696', 'https://w3id.org/oc/meta/prov/pa/1')
        self.assertTrue(os.path.exists(os.path.join(dst, 'br', '060', '10000', '1000', '1000.json')))
        with ZipFile(os.path.join(dst, 'br', '060', '10000', '1000', 'prov', 'se.zip'), 'r') as archive:
            archived_files = archive.namelist()
            for archived_file in archived_files:
                with archive.open(archived_file) as f:
                    data = json.load(f)
                    for i, entity in enumerate(data):
                        graph = entity['@graph']
                        for j, property_value in enumerate(graph):
                            if 'http://www.w3.org/ns/prov#wasAttributedTo' in property_value:
                                self.assertEqual(data[i]['@graph'][j]['http://www.w3.org/ns/prov#wasAttributedTo'][0]['@id'], 'https://w3id.org/oc/meta/prov/pa/1')
        rmtree(dst)