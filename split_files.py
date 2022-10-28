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


from support import modify_archive
from typing import Tuple
from zipfile import ZipExtFile
import argparse
import os
import re


def get_output_filename(output_path:str, cur_index:int) -> Tuple[str, int]:
    cur_filename = os.path.basename(output_path)
    ext = os.path.splitext(cur_filename)[1]
    timestamp = re.search('\d{4}-\d{2}-\d{2}T\d{2}_?\d{2}_?\d{2}', cur_filename).group(0)
    timestamp_split = timestamp.split('T')
    old_time = timestamp_split[1]
    new_timestamp = timestamp_split[0] + 'T' + '_'.join(a+b for a,b in zip(old_time[::2], old_time[1::2]))
    tmp_filepath = output_path.replace(cur_filename, f'{new_timestamp}-{str(cur_index)}{ext}')
    while os.path.exists(tmp_filepath):
        cur_index += 1
        tmp_filepath = output_path.replace(cur_filename, f'{new_timestamp}-{str(cur_index)}{ext}')
    return tmp_filepath, cur_index

def dump_split_data(lines_to_split:list, output_path:str, cur_index:int) -> int:
    new_output_path, cur_index = get_output_filename(output_path, cur_index)
    with open(new_output_path, 'w', encoding='utf8') as f:
        for line in lines_to_split:
            f.write(line)
    return cur_index 

def split_nquads(f:ZipExtFile, output_path:str, threshold:int) -> None:
    lines_to_split = []
    cur_subj = None
    cur_index = 1
    for i, line in enumerate(f):
        line = line.decode('utf8')
        if line != '\n':
            subject = line.split()[0]
            if subject != cur_subj:
                if len(lines_to_split) > threshold:
                    cur_index = dump_split_data(lines_to_split, output_path, cur_index)
                    cur_index += 1
                    lines_to_split = []
                elif i > 0:
                    lines_to_split.append('\n')
                cur_subj = subject
                lines_to_split.append(line)
            else:
                lines_to_split.append(line)
    dump_split_data(lines_to_split, output_path, cur_index)

def split_files(src:str, dst:str, file_format:str, threshold:int) -> None:
    modify_archive(src, dst, eval(f'split_{file_format}'), threshold=threshold)


if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='A tool to convert OpenCitations provenance from one format to another')
    parser.add_argument('-s', '--src', dest='src', required=True, help='The folder containing the provenance archives')
    parser.add_argument('-d', '--dst', dest='dst', required=True, help='The folder where new archives will be saved')
    parser.add_argument('-f', '--file_format', dest='file_format', required=True, choices=['csv', 'nquads'], help='The format of files contained in archives')
    parser.add_argument('-t', '--threshold', dest='threshold', required=False, default=500000, type=int, help='Maximum number of lines per file')
    args = parser.parse_args()
    split_files(src=args.src, dst=args.dst, file_format=args.file_format, threshold=args.threshold)