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


from typing import List
from rdflib import ConjunctiveGraph
from shutil import make_archive, rmtree
from tqdm import tqdm
from zipfile import ZipFile
import csv
import os
import re


def write_csv(path:str, datalist:List[dict], fieldnames:list=None) -> None:
    if datalist:
        fieldnames = datalist[0].keys() if fieldnames is None else fieldnames
        with open(path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(f=output_file, fieldnames=fieldnames, delimiter=',')
            dict_writer.writeheader()
            dict_writer.writerows(datalist)

def to_nt_sorted_list(cg:ConjunctiveGraph) -> list:
    nt_list = re.split('\s?\.\s?\n+', cg.serialize(format='nquads'))
    nt_list = filter(None, nt_list)
    sorted_nt_list = sorted(nt_list)
    return sorted_nt_list

def modify_archive(src:str, dst:str, func:callable, *args, **kwargs) -> ConjunctiveGraph:
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
                    output_path = os.path.join(dst_folder, archived_file)
                    func(f, output_path, *args, **kwargs)
        make_archive(base_name=dst_folder, format='zip', root_dir=dst_folder)
        rmtree(dst_folder)
        pbar.update()
    pbar.close()