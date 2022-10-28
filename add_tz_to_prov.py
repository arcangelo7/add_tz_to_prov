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
from datetime import datetime, timezone
from support import modify_archive, write_csv
from io import TextIOWrapper
from rdflib import ConjunctiveGraph
from zipfile import ZipExtFile
import argparse
import pytz
import re


def add_tz_to_csv(f:ZipExtFile, output_path:str, zone:str) -> None:
    data = list(DictReader(TextIOWrapper(f)))
    for row in data:
        if row['created']:
            row['created'] = get_utc_time_str(row['created'], zone)
        if row['invalidated']:
            row['invalidated'] = get_utc_time_str(row['invalidated'], zone)
    write_csv(output_path, data)

def add_tz_to_nquads(f:ZipExtFile, output_path:str, zone:str) -> None:
    new_lines = []
    for line in f:
        line_str = line.decode('utf8')
        if 'http://www.w3.org/ns/prov#generatedAtTime' in line_str or 'http://www.w3.org/ns/prov#invalidatedAtTime' in line_str:
            time_str = re.search('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', line_str).group(0)
            time_tz = get_utc_time_str(time_str, zone)
            new_lines.append(line_str.replace(time_str, time_tz))
        else:
            new_lines.append(line_str)        
    with open(output_path, 'w', encoding='utf8') as f:
        for line in new_lines:
            f.write(line)

def add_tz_to_prov(src:str, dst:str, file_format:str, zone:str) -> ConjunctiveGraph:
    modify_archive(src, dst, eval(f'add_tz_to_{file_format}'), zone)

def get_utc_time_str(naive_time_str:str, zone:str) -> str:
    """
    Given a naive time string in the format '%Y-%m-%dT%H:%M:%S', returns a time string in the same format localised with the UTC time zone.

    :param naive_time_str: a naive time string in the format '%Y-%m-%dT%H:%M:%S'
    :type string: str
    :return: str -- a time string in the format '%Y-%m-%dT%H:%M:%S' localised with the UTC time zone
    """
    local = pytz.timezone(zone)
    naive = datetime.strptime(naive_time_str, "%Y-%m-%dT%H:%M:%S")
    local_dt = local.localize(naive)
    return local_dt.astimezone(timezone.utc).isoformat(sep="T")


if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='Given an OpenCitations provenance dump containing naive time strings in the format "%Y-%m-%dT%H:%M:%S", localise such times with the UTC time zone')
    parser.add_argument('-s', '--src', dest='src', required=True, help='The folder containing the provenance archives')
    parser.add_argument('-d', '--dst', dest='dst', required=True, help='The folder where new archives will be saved')
    parser.add_argument('-f', '--file_format', dest='file_format', required=True, help='The format of files contained in archives')
    parser.add_argument('-z', '--zone', dest='zone', required=True, help='A timezone listed in pytz.all_timezones, such as "Europe/Rome"')
    args = parser.parse_args()
    add_tz_to_prov(src=args.src, dst=args.dst, file_format=args.file_format, zone=args.zone)