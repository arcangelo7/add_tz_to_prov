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

import argparse
import json
from support import modify_archive
from zipfile import ZipExtFile

def modify_was_attributed_to_in_jsonld(f:ZipExtFile, output_path:str, from_value:str, to_value:str) -> None:
    data = json.load(f)
    for i, entity in enumerate(data):
        graph = entity['@graph']
        for j, property_value in enumerate(graph):
            if 'http://www.w3.org/ns/prov#wasAttributedTo' in property_value:
                was_attributed_to = property_value['http://www.w3.org/ns/prov#wasAttributedTo'][0]['@id']
                if was_attributed_to == from_value:
                    data[i]['@graph'][j]['http://www.w3.org/ns/prov#wasAttributedTo'][0]['@id'] = to_value
    with open(file=output_path, mode='w', encoding='utf8') as output_file:
        json.dump(data, output_file)

def modify_property(src:str, dst, property_name:str, file_format:str, from_value:str, to_value:str) -> None:
    modify_archive(src, dst, eval(f'modify_{property_name}_in_{file_format}'), from_value, to_value)

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='A tool to replace a property value in OpenCitations provenance with a target value')
    parser.add_argument('-s', '--src', dest='src', required=True, type=str, help='The folder containing the provenance archives')
    parser.add_argument('-d', '--dst', dest='dst', required=True, type=str, help='The folder where new archives will be saved')
    parser.add_argument('-p', '--property', dest='property', required=True, type=str, help='The property to be modified')
    parser.add_argument('-f', '--format', dest='format', required=True, type=str, choices=['jsonld'], help='The source files format')
    parser.add_argument('-fv', '--from_value', dest='from_value', required=True, type=str, help='Original value')
    parser.add_argument('-tv', '--to_value', dest='to_value', required=True, type=str, help='Target value')
    args = parser.parse_args()
    modify_property(args.src, args.dst, args.property, args.format, args.from_value, args.to_value)