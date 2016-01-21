#!/bin/env python2.7

# Investigate the baseball csv files to see what issues there
# are in loading them

import glob
import os
import sys
import pandas as pd
import odo
import sqlalchemy as SA


def create_db():
    metadata = SA.MetaData()

    AllstarFull = SA.Table('AllstarFull', metadata,
                           SA.Column('playerID', SA.String(64)),
                           SA.Column('yearID', SA.Integer()),
                           SA.Column('gameNum', SA.Integer()),
                           SA.Column('gameID', SA.String(64)),
                           SA.Column('teamID', SA.String(64)),
                           SA.Column('lgID', SA.String(64)),
                           SA.Column('GP', SA.Integer()),
                           SA.Column('startingPos', SA.Integer()),
                       )

    Appearances = SA.Table('Appearances', metadata,
                           SA.Column('yearID', SA.Integer()),
                           SA.Column('teamID', SA.String(64)),
                           SA.Column('lgID', SA.String(64)),
                           SA.Column('playerID', SA.String(64)),
                           SA.Column('G_all', SA.Integer()),
                           SA.Column('GS', SA.Integer()),
                           SA.Column('G_batting', SA.Integer()),
                           SA.Column('G_defense', SA.Integer()),
                           SA.Column('G_p', SA.Integer()),
                           SA.Column('G_c', SA.Integer()),
                           SA.Column('G_1b', SA.Integer()),
                           SA.Column('G_2b', SA.Integer()),
                           SA.Column('G_3b', SA.Integer()),
                           SA.Column('G_ss', SA.Integer()),
                           SA.Column('G_lf', SA.Integer()),
                           SA.Column('G_cf', SA.Integer()),
                           SA.Column('G_rf', SA.Integer()),
                           SA.Column('G_of', SA.Integer()),
                           SA.Column('G_dh', SA.Integer()),
                           SA.Column('G_ph', SA.Integer()),
                           SA.Column('G_pr', SA.Integer()),
                    )

    AwardsManagers = SA.Table('AwardsManagers', metadata,
                              SA.Column('playerID', SA.String(64)),
                              SA.Column('awardID', SA.String(64)),
                              SA.Column('yearID', SA.Integer()),
                              SA.Column('lgID', SA.String(64)),
                              SA.Column('tie', SA.String(64)),
                              SA.Column('notes', SA.String(64)),
                          )



    engine = SA.create_engine('sqlite:///baseball.db')
    metadata.create_all(engine)

    return engine
# end def

def main():

    table_names = [ 'AllstarFull', 'Appearances', 'AwardsManagers' ]

    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    data_dir = os.sep.join(script_dir.split(os.sep)[:-2] + ['data', 'lahman_baseball'])

    engine = create_db()

    dataframe_dict = {}
    
    for table in table_names:
        csv = os.path.join(data_dir, table + ".csv")
        odo.odo(csv, 'sqlite:///baseball.db::' + table)


    sys.exit(0)

if __name__ == '__main__':
    main()
