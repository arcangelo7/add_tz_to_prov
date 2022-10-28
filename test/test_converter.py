from converter import convert_provenance
from rdflib import ConjunctiveGraph
from shutil import rmtree
from zipfile import ZipFile
import os
import unittest


class test_converter(unittest.TestCase):
    def test_from_csv_to_nquads(self):
        src = os.path.join('test', 'data', 'csv')
        dst = os.path.join('test', 'converter')
        convert_provenance(src=src, dst=dst, origin_format='csv', destination_format='nquads')
        output_zip_path = os.path.join(dst, '2019-10-21T22_41_20_1-63.zip')
        output_data = set()
        with ZipFile(output_zip_path, 'r') as archive:
            archived_files = archive.namelist()
            for archived_file in archived_files:
                with archive.open(archived_file) as f:
                    cg = ConjunctiveGraph()
                    cg.parse(file=f, format='nquads')
                    for s,p,o,c in cg.quads():
                        output_data.add(f'{str(s)} {str(p)} {str(o)} {str(c.identifier)}')
        expected_data = {
            'https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/',
            'https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.12720/jcm.9.6.475-482 https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/',
            'https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103 https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/',
            'https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/',
            'https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/',
            'https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T14:58:02 https://w3id.org/oc/index/coci/ci/020010207020036191222370937063704070563040802-020010104053609040103010137090401030103/prov/',
            'https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.1215/03616878-3940459 https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/',
            'https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/',
            'https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/',
            'https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/',
            'https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T14:57:39 https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/',
            'https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302 https://w3id.org/oc/index/coci/ci/020010201053600030601060807086303090400040509-0200100010636280000030363030504095800045905000205026302/prov/',
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T14:58:02 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/',
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/',
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/',
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/',
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/',
            'https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.3161/000345414x682463 https://w3id.org/oc/index/coci/ci/020030106013600000003040504010433060802040603-02005090602361117213725102729370200050208/prov/',
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#generatedAtTime 2022-06-13T14:57:39 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/ns/prov#Entity https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://purl.org/dc/terms/description Creation of the citation https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#wasAttributedTo https://w3id.org/oc/index/prov/pa/1 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#specializationOf https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/', 
            'https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/se/1 http://www.w3.org/ns/prov#hadPrimarySource https://api.crossref.org/works/10.1016/j.cgh.2017.06.043 https://w3id.org/oc/index/coci/ci/02001000106361937121617370200010737000637000403-02001000907362821103700110001031403010801101204131513/prov/'}
        rmtree(dst)
        self.assertEqual(output_data, expected_data)


if __name__ == '__main__': # pragma: no cover
    unittest.main()