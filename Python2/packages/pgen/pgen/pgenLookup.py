#!/bin/env python2.7

from argparse import ArgumentParser
import re
import pandas as pd
import io
import sys
import random


def random_digit():
    return random.choice('0123456789')
# end def

def random_hex():
    return random.choice('0123456789ABCDEF')
# end def

def table_to_df(table):
    buf = io.BytesIO(table)
    df = pd.read_table(buf,sep='\s+')
    buf.close()
    return df
# end def

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
                        yield table_to_df(table)
                        table = ""
                table += line

        # yield the final table
        yield table_to_df(table)
        
# end def


def main():
    parser = ArgumentParser(description = "Generate password element tables")
    parser.add_argument('dataFile', help="File containing pgen tables")
    parser.add_argument('indices', metavar='trc', nargs='*', help="table/row/column index (zero-based), for example: 1B4")
    parser.add_argument('-g', '--gen_indices', metavar='int', action='store', help="generate the specified number of random indices")
    args = parser.parse_args()

    if args.indices and args.gen_indices:
        sys.stdout.write("Error! 'indices' and 'gen_indices' arguments are mutually exclusive!\n")
        sys.exit(1)
    
    indices = args.indices
    df_list = list(read_data(args.dataFile))
    
    if args.gen_indices:
        indices = []
        for i in range(int(args.gen_indices)):
            t = random_digit()
            r = random_hex()
            c = random_digit()
            indices.append(t+r+c)
            sys.stdout.write("{}{}{} ".format(t,r,c))
        sys.stdout.write("-> ")
    
    lookup = ""
    for index in indices:
        if len(index) != 3:
            sys.stderr.write("Error: Invalid index, must be length 3\n")
            sys.exit(1)
        (t,r,c) = index
        lookup += df_list[int(t)].loc[r,c]
    sys.stdout.write("{}\n".format(lookup))
# end def


if __name__ == "__main__":
    main()
