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
import os
import pathlib
from shutil import copyfile
from zipfile import ZIP_DEFLATED, ZipFile

from pebble import ProcessPool


def run(src:str, dst:str, from_value:str, to_value:str):
    files_to_modify = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk(src) for filename in filenames]
    with ProcessPool() as executor:
        for input_filepath in files_to_modify:
            dirpath = os.path.dirname(input_filepath)
            folders_to_remove = len(src.split(os.sep))
            output_dir = os.path.join(dst, os.sep.join(pathlib.Path(dirpath).parts[folders_to_remove:]))
            executor.schedule(
                function=modify_was_attributed_to_in_jsonld, 
                args=(input_filepath, output_dir, from_value, to_value)) 

def modify_was_attributed_to_in_jsonld(input_filepath, output_dir:str, from_value:str, to_value:str) -> None:
    dirpath = os.path.dirname(input_filepath)
    filename = os.path.basename(input_filepath)
    output_filepath = os.path.join(output_dir, filename)
    os.makedirs(output_dir, exist_ok=True)
    if os.path.basename(dirpath) == 'prov' and os.path.splitext(filename)[1] == '.zip':
        with ZipFile(input_filepath, 'r') as archive:
            archived_files = archive.namelist()
            for archived_file in archived_files:
                with archive.open(archived_file) as f:
                    data = json.load(f)
                    for i, entity in enumerate(data):
                        graph = entity['@graph']
                        for j, property_value in enumerate(graph):
                            if 'http://www.w3.org/ns/prov#wasAttributedTo' in property_value:
                                was_attributed_to = property_value['http://www.w3.org/ns/prov#wasAttributedTo'][0]['@id']
                                if was_attributed_to == from_value:
                                    data[i]['@graph'][j]['http://www.w3.org/ns/prov#wasAttributedTo'][0]['@id'] = to_value
                json_output_filepath = output_filepath.replace('.zip', '.json')
                with open(file=json_output_filepath, mode='w', encoding='utf-8') as output_file:
                    json.dump(data, output_file)
                with ZipFile(file=json_output_filepath.replace('.json', '.zip'), mode='w', compression=ZIP_DEFLATED, allowZip64=True) as zf:
                    zf.write(json_output_filepath, arcname=os.path.basename(json_output_filepath))
                os.remove(json_output_filepath)
    else:
        copyfile(input_filepath, output_filepath)


if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='A tool to replace a property value in OpenCitations provenance with a target value')
    parser.add_argument('-s', '--src', dest='src', required=True, type=str, help='The folder containing the provenance archives')
    parser.add_argument('-d', '--dst', dest='dst', required=True, help='The root folder where new archives will be saved')
    parser.add_argument('-fv', '--from_value', dest='from_value', required=True, type=str, help='Original value')
    parser.add_argument('-tv', '--to_value', dest='to_value', required=True, type=str, help='Target value')
    args = parser.parse_args()
    run(args.src, args.dst, args.from_value, args.to_value)