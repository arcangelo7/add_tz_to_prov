from add_tz_to_prov import add_tz_to_prov
from csv import DictReader
from io import TextIOWrapper
from rdflib import ConjunctiveGraph
from shutil import rmtree
from zipfile import ZipFile
import os
import unittest


class test_add_tz_to_prov(unittest.TestCase):
    def test_add_tz_to_prov_csv(self):
        src = os.path.join('test', 'data', 'csv')
        dst = os.path.join('test', 'output')
        add_tz_to_prov(src, dst, 'csv', 'Europe/Rome')
        output_data = list()
        output_zip_path = os.path.join(dst, '2019-10-21T22_41_20_1-63.zip')
        with ZipFile(output_zip_path, 'r') as archive:
            archived_files = archive.namelist()
            for archived_file in archived_files:
                with archive.open(archived_file) as f:
                    output_data.extend(list(DictReader(TextIOWrapper(f))))
        expected_data = [
            {'oci': '02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513', 'snapshot': '1', 'agent': 'https://w3id.org/oc/index/prov/pa/1', 'source': 'https://api.crossref.org/works/10.1016/j.cgh.2017.06.043', 'created': '2022-06-13T12:57:39+00:00', 'invalidated': '', 'description': 'Creation of the citation', 'update': ''}, 
            {'oci': '020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302', 'snapshot': '1', 'agent': 'https://w3id.org/oc/index/prov/pa/1', 'source': 'https://api.crossref.org/works/10.1215/03616878-3940459', 'created': '2022-06-13T12:57:39+00:00', 'invalidated': '', 'description': 'Creation of the citation', 'update': ''}, 
            {'oci': '020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208', 'snapshot': '1', 'agent': 'https://w3id.org/oc/index/prov/pa/1', 'source': 'https://api.crossref.org/works/10.3161/000345414x682463', 'created': '2022-06-13T12:58:02+00:00', 'invalidated': '', 'description': 'Creation of the citation', 'update': ''}, 
            {'oci': '020010207020036191222370937063704070563040802-020010104053609040103010137090401030103', 'snapshot': '1', 'agent': 'https://w3id.org/oc/index/prov/pa/1', 'source': 'https://api.crossref.org/works/10.12720/jcm.9.6.475-482', 'created': '2022-06-13T12:58:02+00:00', 'invalidated': '', 'description': 'Creation of the citation', 'update': ''}]
        rmtree(dst)
        self.assertEqual(output_data, expected_data)

    def test_add_tz_to_prov_nquads(self):
        src = os.path.join('test', 'data', 'nquads')
        dst = os.path.join('test', 'output')
        add_tz_to_prov(src, dst, 'nquads', 'Europe/Rome')
        output_data = set()
        output_zip_path = os.path.join(dst, '2022-06-13T145737_1-29_1-2.zip')
        with ZipFile(output_zip_path, 'r') as archive:
            archived_files = archive.namelist()
            for archived_file in archived_files:
                with archive.open(archived_file) as f:
                    cg = ConjunctiveGraph()
                    cg.parse(file=f, format='nquads')
                    for s,p,o,c in cg.quads():
                        output_data.add(f'{str(s)} {str(p)} {str(o)} {str(c.identifier)}')
        expected_data = {
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.1016/j.cgh.2017.06.043 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T12:58:02+00:00 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.3161/000345414x682463 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T12:57:39+00:00 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/'}
        rmtree(dst)
        self.assertEqual(output_data, expected_data)
                    

if __name__ == '__main__': # pragma: no cover
    unittest.main()