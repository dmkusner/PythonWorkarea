#!/bin/env python2.7

from argparse import ArgumentParser
import re
import pandas as pd
import io
import sys


def read_data(infile):
    header_pat = re.compile(r'^[ 01234567890]+$')
    with open(infile,'r') as f:
        table = ""
        for line in f.readlines():
            if line.strip():
                # if a header line is encountered, and table data currently exists,
                # read it into a dataframe and return it
                if header_pat.search(line):
                    if table:
                        buf = io.BytesIO(table)
                        yield pd.read_table(buf,sep='\s+')
                        table = ""
                table += line

        # yield the final table
        buf = io.BytesIO(table)
        yield pd.read_table(buf,sep='\s+')
        
# end def


def main():
    parser = ArgumentParser(description = "Generate password element tables")
    parser.add_argument('dataFile', help="File containing pgen tables")
    parser.add_argument('indices', metavar='trc', nargs='+', help="table/row/column index (zero-based), for example: 1B4")
    args = parser.parse_args()
    
    df_list = list(read_data(args.dataFile))

    lookup = ""
    for index in args.indices:
        if len(index) != 3:
            sys.stderr.write("Error: Invalid index, must be length 3\n")
            sys.exit(1)
        (t,r,c) = index
        lookup += df_list[int(t)].loc[r,c]
    sys.stdout.write("{}\n".format(lookup))
# end def


if __name__ == "__main__":
    main()
