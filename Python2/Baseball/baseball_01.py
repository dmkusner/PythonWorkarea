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

    AwardsPlayers = SA.Table('AwardsPlayers', metadata,
                             SA.Column('playerID', SA.String(64)),
                             SA.Column('awardID', SA.String(64)),
                             SA.Column('yearID', SA.Integer()),
                             SA.Column('lgID', SA.String(64)),
                             SA.Column('tie', SA.String(64)),
                             SA.Column('notes', SA.String(64)),
                             )

    AwardsShareManagers = SA.Table('AwardsShareManagers', metadata,
                                   SA.Column('awardID', SA.String(64)),
                                   SA.Column('yearID', SA.Integer()),
                                   SA.Column('lgID', SA.String(64)),
                                   SA.Column('playerID', SA.String(64)),
                                   SA.Column('pointsWon', SA.Integer()),
                                   SA.Column('pointsMax', SA.Integer()),
                                   SA.Column('votesFirst', SA.Integer()),
                                   )

    AwardsSharePlayers = SA.Table('AwardsSharePlayers', metadata,
                                  SA.Column('awardID', SA.String(64)),
                                  SA.Column('yearID', SA.Integer()),
                                  SA.Column('lgID', SA.String(64)),
                                  SA.Column('playerID', SA.String(64)),
                                  SA.Column('pointsWon', SA.Integer()),
                                  SA.Column('pointsMax', SA.Integer()),
                                  SA.Column('votesFirst', SA.Integer()),
                                  )

    Batting = SA.Table('Batting', metadata,
                       SA.Column('playerID', SA.String(64)),
                       SA.Column('yearID', SA.Integer()),
                       SA.Column('stint', SA.Integer()),
                       SA.Column('teamID', SA.String(64)),
                       SA.Column('lgID', SA.String(64)),
                       SA.Column('G', SA.Integer()),
                       SA.Column('AB', SA.Integer()),
                       SA.Column('R', SA.Integer()),
                       SA.Column('H', SA.Integer()),
                       SA.Column('2B', SA.Integer()),
                       SA.Column('3B', SA.Integer()),
                       SA.Column('HR', SA.Integer()),
                       SA.Column('RBI', SA.Integer()),
                       SA.Column('SB', SA.Integer()),
                       SA.Column('CS', SA.Integer()),
                       SA.Column('BB', SA.Integer()),
                       SA.Column('SO', SA.Integer()),
                       SA.Column('IBB', SA.Integer()),
                       SA.Column('HBP', SA.Integer()),
                       SA.Column('SH', SA.Integer()),
                       SA.Column('SF', SA.Integer()),
                       SA.Column('GIDP', SA.Integer()),
                       )

    BattingPost = SA.Table('BattingPost', metadata,
                           SA.Column('yearID', SA.Integer()),
                           SA.Column('round', SA.String(64)),
                           SA.Column('playerID', SA.String(64)),
                           SA.Column('teamID', SA.String(64)),
                           SA.Column('lgID', SA.String(64)),
                           SA.Column('G', SA.Integer()),
                           SA.Column('AB', SA.Integer()),
                           SA.Column('R', SA.Integer()),
                           SA.Column('H', SA.Integer()),
                           SA.Column('2B', SA.Integer()),
                           SA.Column('3B', SA.Integer()),
                           SA.Column('HR', SA.Integer()),
                           SA.Column('RBI', SA.Integer()),
                           SA.Column('SB', SA.Integer()),
                           SA.Column('CS', SA.Integer()),
                           SA.Column('BB', SA.Integer()),
                           SA.Column('SO', SA.Integer()),
                           SA.Column('IBB', SA.Integer()),
                           SA.Column('HBP', SA.Integer()),
                           SA.Column('SH', SA.Integer()),
                           SA.Column('SF', SA.Integer()),
                           SA.Column('GIDP', SA.Integer()),
                           )

    CollegePlaying = SA.Table('CollegePlaying', metadata,
                              SA.Column('playerID', SA.String(64)),
                              SA.Column('schoolID', SA.String(64)),
                              SA.Column('yearID', SA.Integer()),
    )

    Fielding = SA.Table('Fielding', metadata,
                        SA.Column('playerID', SA.String(64)),
                        SA.Column('yearID', SA.Integer()),
                        SA.Column('stint', SA.Integer()),
                        SA.Column('teamID', SA.String(64)),
                        SA.Column('lgID', SA.String(64)),
                        SA.Column('POS', SA.String(64)),
                        SA.Column('G', SA.Integer()),
                        SA.Column('GS', SA.Integer()),
                        SA.Column('InnOuts', SA.Integer()),
                        SA.Column('PO', SA.Integer()),
                        SA.Column('A', SA.Integer()),
                        SA.Column('E', SA.Integer()),
                        SA.Column('DP', SA.Integer()),
                        SA.Column('PB', SA.Integer()),
                        SA.Column('WP', SA.Integer()),
                        SA.Column('SB', SA.Integer()),
                        SA.Column('CS', SA.Integer()),
                        SA.Column('ZR', SA.Integer()),
                        )

    FieldingOF = SA.Table('FieldingOF', metadata,
                          SA.Column('playerID', SA.String(64)),
                          SA.Column('yearID', SA.Integer()),
                          SA.Column('stint', SA.Integer()),
                          SA.Column('Glf', SA.Integer()),
                          SA.Column('Gcf', SA.Integer()),
                          SA.Column('Grf', SA.Integer()),
                          )

    FieldingPost = SA.Table('FieldingPost', metadata,
                            SA.Column('playerID', SA.String(64)),
                            SA.Column('yearID', SA.Integer()),
                            SA.Column('teamID', SA.String(64)),
                            SA.Column('lgID', SA.String(64)),
                            SA.Column('round', SA.String(64)),
                            SA.Column('POS', SA.String(64)),
                            SA.Column('G', SA.Integer()),
                            SA.Column('GS', SA.Integer()),
                            SA.Column('InnOuts', SA.Integer()),
                            SA.Column('PO', SA.Integer()),
                            SA.Column('A', SA.Integer()),
                            SA.Column('E', SA.Integer()),
                            SA.Column('DP', SA.Integer()),
                            SA.Column('TP', SA.Integer()),
                            SA.Column('PB', SA.Integer()),
                            SA.Column('SB', SA.Integer()),
                            SA.Column('CS', SA.Integer()),
                            )

    HallOfFame = SA.Table('HallOfFame', metadata,
                          SA.Column('playerID', SA.String(64)),
                          SA.Column('yearID', SA.Integer()),
                          SA.Column('votedBy', SA.String(64)),
                          SA.Column('ballots', SA.Integer()),
                          SA.Column('needed', SA.Integer()),
                          SA.Column('votes', SA.Integer()),
                          SA.Column('inducted', SA.String(64)),
                          SA.Column('category', SA.String(64)),
                          SA.Column('needed_note', SA.String(64)),
                          )

    Managers = SA.Table('Managers', metadata,
                        SA.Column('playerID', SA.String(64)),
                        SA.Column('yearID', SA.Integer()),
                        SA.Column('teamID', SA.String(64)),
                        SA.Column('lgID', SA.String(64)),
                        SA.Column('inseason', SA.Integer()),
                        SA.Column('G', SA.Integer()),
                        SA.Column('W', SA.Integer()),
                        SA.Column('L', SA.Integer()),
                        SA.Column('rank', SA.Integer()),
                        SA.Column('plyrMgr', SA.String(1)),
                        )

    ManagersHalf = SA.Table('ManagersHalf', metadata,
                            SA.Column('playerID', SA.String(64)),
                            SA.Column('yearID', SA.Integer()),
                            SA.Column('teamID', SA.String(64)),
                            SA.Column('lgID', SA.String(64)),
                            SA.Column('inseason', SA.Integer()),
                            SA.Column('half', SA.Integer()),
                            SA.Column('G', SA.Integer()),
                            SA.Column('W', SA.Integer()),
                            SA.Column('L', SA.Integer()),
                            SA.Column('rank', SA.Integer()),
                            )

    Master = SA.Table('Master', metadata,
                      SA.Column('playerID', SA.String(64)),
                      SA.Column('birthYear', SA.Integer()),
                      SA.Column('birthMonth', SA.Integer()),
                      SA.Column('birthDay', SA.Integer()),
                      SA.Column('birthCountry', SA.String(64)),
                      SA.Column('birthState', SA.String(64)),
                      SA.Column('birthCity', SA.String(64)),
                      SA.Column('deathYear', SA.Integer()),
                      SA.Column('deathMonth', SA.Integer()),
                      SA.Column('deathDay', SA.Integer()),
                      SA.Column('deathCountry', SA.String(64)),
                      SA.Column('deathState', SA.String(64)),
                      SA.Column('deathCity', SA.String(64)),
                      SA.Column('nameFirst', SA.String(64)),
                      SA.Column('nameLast', SA.String(64)),
                      SA.Column('nameGiven', SA.String(64)),
                      SA.Column('weight', SA.Integer()),
                      SA.Column('height', SA.Integer()),
                      SA.Column('bats', SA.String(1)),
                      SA.Column('throws', SA.String(1)),
                      SA.Column('debut', SA.Date()),
                      SA.Column('finalGame', SA.Date()),
                      SA.Column('retroID', SA.String(64)),
                      SA.Column('bbrefID', SA.String(64)),
                      )                      
                      

    engine = SA.create_engine('sqlite:///baseball.db')
    metadata.create_all(engine)
# end def

def main():

    table_names = [ 
        'AllstarFull', 'Appearances', 'AwardsManagers', 'AwardsPlayers',
        'AwardsShareManagers', 'AwardsSharePlayers', 'Batting', 'BattingPost',
        'CollegePlaying', 'Fielding', 'FieldingOF', 'FieldingPost',
        'HallOfFame', 'Managers', 'ManagersHalf', 'Master',
    ]

    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    data_dir = os.sep.join(script_dir.split(os.sep)[:-2] + ['data', 'lahman_baseball'])

    create_db()

    for table in table_names:
        csv = os.path.join(data_dir, table + ".csv")
        odo.odo(csv, 'sqlite:///baseball.db::' + table)

    sys.exit(0)

if __name__ == '__main__':
    main()
