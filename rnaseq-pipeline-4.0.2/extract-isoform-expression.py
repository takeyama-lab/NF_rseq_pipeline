#!/usr/bin/env python

import argparse
import os
import re
import sys

from lib import Extend
from version import __version__

HEADER = ('transcript_id', 'cov', 'FPKM', 'TPM')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ts', help='transcript.gtf generated by stringtie')
    ap.add_argument('-o', '--output', dest='fout', action='store',
                    metavar='FILE', default=None,
                    help='output file path, default=stdout')
    ap.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    args = ap.parse_args()

    with open(args.ts) as fh:
        header = ('transcript_id', 'cov', 'FPKM', 'TPM')
        p = re.compile('#')
        with Extend.IO.sopen(args.fout) as fo:
            print('\t'.join(HEADER), file=fo)
            for line in fh:
                if p.match(line):
                    continue
                cols = line.strip().split('\t')
                if cols[2] != 'transcript':
                    continue
                data = {}
                for elem in map(lambda v: v.strip(), cols[8].split(';')):
                    vals = elem.split(' ')
                    if len(vals) > 1:
                        data[vals[0]] = re.sub('"', '', vals[1].strip())
                print('\t'.join(map(lambda h: data[h], HEADER)), file=fo)

if __name__ == '__main__':
    main()
