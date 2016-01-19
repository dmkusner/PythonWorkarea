#!/bin/env python2.7

# Investigate the baseball csv files to see what issues there
# are in loading them

import glob
import os
import sys
import pandas as pd
import odo
import sqlalchemy


def main():
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    data_dir = os.sep.join(script_dir.split(os.sep)[:-2] + ['data', 'lahman_baseball'])

    dataframe_dict = {}

    for csv_path in glob.glob(data_dir + os.sep + '*.csv'):
        csv_name = os.path.basename(csv_path)[:-4]
        df = pd.read_csv(csv_path,keep_default_na=False,na_values=[""])
        dataframe_dict[csv_name] = df

    for (table,data) in dataframe_dict.items():
        print table
        print data.head()
        print data.dtypes
        print

    # Try to stick the data into a sqlite db
    table_name = 'Appearances'
    df = dataframe_dict[table_name]
    odo.odo(df,"sqlite:///baseball.db::"+table_name)
    #print odo.odo(df,list)

    #for (table,data) in dataframe_dict.items():
    #    sqlite_uri = "sqlite:////baseball.db::" + table
    #    odo.odo(data,sqlite_uri)

    sys.exit(0)

if __name__ == '__main__':
    main()
