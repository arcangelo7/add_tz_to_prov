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


from csv import DictReader
from io import TextIOWrapper
from rdflib import DCTERMS, PROV, RDF, XSD
from shutil import make_archive, rmtree
from tqdm import tqdm
from zipfile import ZipExtFile, ZipFile
import argparse
import os


def from_csv_to_nquads(f:ZipExtFile, output_path:str):
    data = list(DictReader(TextIOWrapper(f)))
    base_uri = 'https://w3id.org/oc/index/coci'
    lines = []
    for row in data:
        row_lines = []
        oci = row['oci']
        snapshot = row['snapshot']
        agent = row['agent']
        source = row['source']
        created = row['created']
        invalidated = row['invalidated']
        description = row['description']
        update = row['update']
        entity = f'{base_uri}/ci/{oci}'
        subject = f'{entity}/prov/se/{snapshot}'
        context = f'{entity}/prov/'
        row_lines.append(f'<{subject}> <{RDF.type}> <{PROV.Entity}> <{context}> .')
        row_lines.append(f'<{subject}> <{PROV.wasAttributedTo}> <{agent}> <{context}> .')
        row_lines.append(f'<{subject}> <{PROV.generatedAtTime}> "{created}"^^<{XSD.dateTime}> <{context}> .')
        row_lines.append(f'<{subject}> <{PROV.hadPrimarySource}> <{source}> <{context}> .')
        row_lines.append(f'<{subject}> <{PROV.specializationOf}> <{entity}> <{context}> .')
        row_lines.append(f'<{subject}> <{DCTERMS.description}> "{description}" <{context}> .')
        if invalidated:
            row_lines.append(f'<{subject}> <{PROV.generatedAtTime}> "{invalidated}"^^<{XSD.dateTime}> <{context}> .')
        if update:
            row_lines.append(f'<{subject}> <https://w3id.org/oc/ontology/hasUpdateQuery> "{update}" <{context}> .')
        row_lines.append('\n')
        lines.extend(row_lines)
    output_path = output_path.replace('.csv', '.ttl')
    with open(output_path, 'w', encoding='utf8') as f:
        for line in lines:
            f.write(f'{line}\n')

def convert_provenance(src:str, dst:str, origin_format:str, destination_format:str) -> None:
    filenames = os.listdir(src)
    pbar = tqdm(total=len(filenames))
    os.makedirs(dst, exist_ok=True)
    for filename in filenames:
        dst_folder = os.path.join(dst, os.path.splitext(filename)[0])
        if not os.path.exists(dst_folder):
            os.mkdir(dst_folder)
        with ZipFile(os.path.join(src, filename), 'r') as archive:
            archived_files = archive.namelist()
            for archived_file in archived_files:
                with archive.open(archived_file) as f:
                    output_path = os.path.join(dst_folder, archived_file.replace('_', '-').replace(':', '_'))
                    eval(f'from_{origin_format}_to_{destination_format}(f, output_path)')
        make_archive(base_name=dst_folder, format='zip', root_dir=dst_folder)
        rmtree(dst_folder)
        pbar.update()
    pbar.close()


if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='A tool to convert OpenCitations provenance from one format to another')
    parser.add_argument('-s', '--src', dest='src', required=True, help='The folder containing the provenance archives')
    parser.add_argument('-d', '--dst', dest='dst', required=True, help='The folder where new archives will be saved')
    parser.add_argument('-of', '--origin_format', dest='origin_format', required=True, choices=['csv'], help='The original format')
    parser.add_argument('-df', '--destination_format', dest='destination_format', required=True, choices=['nquads'], help='The destination format')
    args = parser.parse_args()
    convert_provenance(src=args.src, dst=args.dst, origin_format=args.origin_format, destination_format=args.destination_format)