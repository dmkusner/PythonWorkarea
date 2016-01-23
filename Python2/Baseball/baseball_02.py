#!/bin/env python2.7

# Investigate the baseball csv files to see what issues there
# are in loading them

import glob
import os
import sys
import pandas as pd
import odo
import sqlalchemy as SA


def main():

    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    data_dir = os.sep.join(script_dir.split(os.sep)[:-2] + ['data', 'lahman_baseball'])
    db_name = 'baseball_02.db'

    csv_files = glob.glob(data_dir + "/*.csv")
    table_names = [x[:-4] for x in (os.path.basename(x) for x in csv_files)]

    if os.path.exists(db_name):
        os.remove(db_name)

    for (csv_file, table_name) in zip(csv_files, table_names):
        csv_odo = odo.CSV(csv_file)
        csv_ds = odo.discover(csv_odo)
        odo.odo(csv_odo, 'sqlite:///' + db_name + '::' + table_name, dshape=csv_ds)

    sys.exit(0)

if __name__ == '__main__':
    main()
