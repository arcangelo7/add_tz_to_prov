# ISC License (ISC)
# ==================================
# Copyright 2022 Arcangelo Massari

# Permission to use, copy, modify, and/or distribute this software for any purpose with or
# without fee is hereby granted, provided that the above copyright notice and this permission
# notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from rdflib import ConjunctiveGraph
from shutil import rmtree
from split_files import split_files
from typing import Dict
from zipfile import ZipFile
import os
import unittest


class test_split_files(unittest.TestCase):
    def test_split_files_nquads(self):
        src = os.path.join('test', 'data', 'split_files', 'nquads')
        dst = os.path.join('test', 'data', 'split_files', 'output_nquads')
        split_files(src, dst, 'nquads', 2)
        output_data: Dict[str, set] = dict()
        with ZipFile(os.path.join(dst, '2022-06-13T145737.zip'), 'r') as archive:
            archived_files = archive.namelist()
            for archived_file in archived_files:
                with archive.open(archived_file) as f:
                    cg = ConjunctiveGraph()
                    cg.parse(file=f, format='nquads')
                    for s,p,o,c in cg.quads():
                        output_data.setdefault(archived_file, set())
                        output_data[archived_file].add(f'{str(s)} {str(p)} {str(o)} {str(c.identifier)}')
        expected_data = {
            '2022-06-13T14_57_37-2.ttl': {
                'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.3161/000345414x682463 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/',
                'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
                'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
                'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
                'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T14:58:02 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
                'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/'}, 
            '2022-06-13T14_57_37-1.ttl': {
                'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.1016/j.cgh.2017.06.043 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
                'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
                'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
                'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T14:57:39 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
                'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
                'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/'},
            '2022-06-13T14_57_37-3.ttl': {
                'https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/', 
                'https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/', 
                'https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/', 
                'https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305 https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/', 
                'https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2021-11-15T02:19:22+00:00 https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/', 
                'https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.1021/cg025502y https://w3id.org/oc/index/coci/ci/0200100020136121600020505000234-02001000106360000020263000204085807065909000004016305/prov/'}}
        rmtree(dst)
        self.assertEqual(output_data, expected_data)



if __name__ == '__main__': # pragma: no cover
    unittest.main()