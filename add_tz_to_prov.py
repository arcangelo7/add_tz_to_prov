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
from datetime import datetime, timezone, timedelta
from io import TextIOWrapper
from rdflib import ConjunctiveGraph, Literal, URIRef, XSD
from shutil import make_archive, rmtree
from tqdm import tqdm
from typing import List
from zipfile import ZipFile, ZipExtFile
import argparse
import csv
import os
import re


def to_nt_sorted_list(cg:ConjunctiveGraph) -> list:
    nt_list = re.split('\s?\.\s?\n+', cg.serialize(format='nquads'))
    nt_list = filter(None, nt_list)
    sorted_nt_list = sorted(nt_list)
    return sorted_nt_list

def write_csv(path:str, datalist:List[dict], fieldnames:list=None) -> None:
    if datalist:
        fieldnames = datalist[0].keys() if fieldnames is None else fieldnames
        with open(path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(f=output_file, fieldnames=fieldnames, delimiter=',')
            dict_writer.writeheader()
            dict_writer.writerows(datalist)

def add_tz_to_csv(f:ZipExtFile, tz_offset:timedelta, output_path:str) -> None:
    data = list(DictReader(TextIOWrapper(f)))
    for row in data:
        if row['created']:
            row['created'] = datetime.strptime(row['created'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone(offset=tz_offset)).isoformat(sep='T')
        if row['invalidated']:
            row['invalidated'] = datetime.strptime(row['created'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone(offset=tz_offset)).isoformat(sep='T')
    write_csv(output_path, data)

def add_tz_to_nquads(f:ZipExtFile, tz_offset:timedelta, output_path:str) -> None:
    cg = ConjunctiveGraph()
    cg.parse(file=f, format='nquads')
    for s,p,o,c in cg.quads():
        if p in {URIRef('http://www.w3.org/ns/prov#generatedAtTime'), URIRef('http://www.w3.org/ns/prov#invalidatedAtTime')}:
            cg.remove((s,p,o,c))
            o_tz = Literal(datetime.strptime(str(o), '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone(offset=tz_offset)).isoformat(sep='T'), datatype=XSD.dateTime)
            cg.add((s,p,o_tz,c))
    sorted_nt_list = to_nt_sorted_list(cg)
    with open(output_path, 'w') as f:
        for line in sorted_nt_list:
            f.write(f"{line}.\n")

def add_tz_to_prov(src:str, dst:str, file_format:str, tz_offset:timedelta) -> ConjunctiveGraph:
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
                    eval(f'add_tz_to_{file_format}(f, tz_offset, output_path)')
        make_archive(base_name=dst_folder, format='zip', root_dir=dst_folder)
        rmtree(dst_folder)
        pbar.update()
    pbar.close()


if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='Add timezone information to provenance zipped files containing naive time indications')
    parser.add_argument('-s', '--src', dest='src', required=True, help='The folder containing the provenance archives')
    parser.add_argument('-d', '--dst', dest='dst', required=True, help='The folder where new archives will be saved')
    parser.add_argument('-f', '--file_format', dest='file_format', required=True, help='The format of files contained in archives')
    parser.add_argument('-t', '--tz_offset', dest='tz_offset', required=True, type=int, help='An integer representing the UTC offset to be added')
    args = parser.parse_args()
    add_tz_to_prov(src=args.src, dst=args.dst, file_format=args.file_format, tz_offset=timedelta(hours=args.tz_offset))