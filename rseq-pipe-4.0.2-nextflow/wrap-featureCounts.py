#!/usr/bin/env python

import argparse
import os
import pandas as pd
import subprocess
import sys

from version import __version__

FOUT = 'count_matrix.txt'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('gtf', help='GTF file')
    ap.add_argument('smpl', help='sample information file')
    ap.add_argument('-i', '--input', dest='fin', action='store',
                    metavar='DIR', default=None,
                    help='bam file directory, default=%s' % None)
    ap.add_argument('-o', '--output', dest='fout', action='store',
                    metavar='FILE', default=FOUT,
                    help='output file path, default=%s' % FOUT)
    ap.add_argument('-p', '--paired-end', dest='pair',
                    action='store_true', default=False,
                    help='paired end read')
    ap.add_argument('-T', '--thread', dest='t',
                    metavar='INT', action='store', default=1,
                    help='number of thread, default=1')
    ap.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    args = ap.parse_args()

    smpl = pd.read_csv(args.smpl, sep='\t')
    fout = args.fout
    ftmp = args.fout + '.tmp'
    fsum = fout + '.summary'

    # exec featureCounts
    bams = list(map(lambda seq, s: '%s/%s/04_tagging/%s' % (args.fin, f"{seq}", f"{s}_R1_trim.sort.bam"), smpl.Sequence_ID, smpl.Sample_ID))
    cmds = ['featureCounts',
            '-o %s' % fout,
            '-a %s' % args.gtf,
            '-T %s' % args.t]
    if args.pair:
        cmds.extend(['-p'])
    cmds.extend(bams)
    cmd = ' '.join(cmds)
    print(cmd, file=sys.stderr)
    ret = subprocess.check_call(cmd, shell=True)

    # format tpm_matrix
    mat = pd.read_csv(fout, skiprows=1, sep='\t')
    header = ['Geneid']
    header.extend(bams)
    mat_sel = mat[header]
    new_header = ['gene_id']
    new_header.extend(smpl.Sample_ID)
    mat_sel.columns = new_header
    mat_sel.to_csv(ftmp, index=False, sep='\t')

    # rename
    os.rename(ftmp, fout)

if __name__ == '__main__':
    main()

