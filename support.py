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
import csv
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
