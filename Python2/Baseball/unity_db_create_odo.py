#!/datateam/work/david_kusner/tools/anaconda64/bin/python

from sqlalchemy import MetaData, create_engine, Column, Index, Integer, String, Table
from sqlalchemy.types import TEXT, BIGINT
import odo
import pandas as pd
import ipdb

# Here we combine pandas and sqlalchemy to do the hard work of reading
# a csv and entering the data into a database. Pandas reads the csv
# file one chunk at a time using read_csv(), and inserts into the
# database table using to_sql() and the sqlalchemy engine. It saves an
# extraordinary amount of custom code to process a csv file and
# convert the results into input statements for a specific database.
def table_from_csv(engine, table_name, csv_file, chunksize=25000, encoding="utf-8", sep=","):
    row_count = 0
    print 'Creating table: ' + table_name
    for df in pd.read_csv(csv_file, chunksize=chunksize, iterator=True, encoding=encoding, sep=sep):
        row_count += len(df)
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print '  completed {} rows'.format(row_count)


def main():

    metadata = MetaData()

    form_table_dst = Table('unity_form', metadata,
                           Column('speakerId', String(64), nullable=False),
                           Column('sessionId', String(64), nullable=False),
                           Column('formId', String(64), nullable=False),
                           Column('gwZip', String(255)),
                           Column('gwDir', String(255)),
                           Column('ncsxVersion', String(64)),
                           Column('ncsxFile', String(255)),
                           Column('rawZipCreated', String(255)),
                           Column('rawZipReceived', String(64)),
                           Column('sessionStart', String(64)),
                           Column('userName', String(255)),
                           Column('userProfileId', String(255)),
                           Column('userOrganizationId', String(255)),
                           Column('userOrganizationName', String(255)),
                           Column('userLanguage', String(64)),
                           Column('appPartnerName', String(255)),
                           Column('appName', String(64)),
                           Column('appVersion', String(64)),
                           Column('nuanceSDKName', String(64)),
                           Column('nuanceSDKVersion', String(64)),
                           Column('saClientSDK', String(64)),
                           Column('saClientVersion', String(64)),
                           Column('saServerVersion', String(64)),
                           Column('saInputChannel', String(64)),
                           Column('saLanguage', String(64)),
                           Column('saTopic', String(64)),
                           Column('saTechnology', String(64)),
                           Column('s2Version', String(64)),
                           Column('s2mrecVersion', String(64)),
                           Column('s2DatapackName', String(64)),
                           Column('s2BaseLM', String(64)),
                           Column('s2InitialBaseAM', String(64)),
                           Column('s2FinalBaseAM', String(64)),
                           Column('kpiServerTopic', String(64)),
                           Column('kpiServerContextId', String(64)),
                           Column('kpiClientRuntime', String(64)),
                           )

    utts_table_dst = Table('unity_utts', metadata,
                           Column('speakerId', String(64), nullable=False),
                           Column('sessionId', String(64), nullable=False),
                           Column('formId', String(64), nullable=False),
                           Column('uttNum', Integer(), nullable=False),
                           Column('audioPosition', Integer()),
                           Column('uttDur', Integer()),
                           Column('audioFileName', String(255)),
                           Column('codedWvnm', String(64)),
                           Column('codec', String(64)),
                           Column('sampleRate', String(64)),
                           Column('rcgType', String(64)),
                           Column('rcgFile', String(64)),
                           Column('SNR', String(64)),
                           Column('clipping', String(64)),
                           Column('ans', String(255)),
                           Column('anstok', String(255)),
                           Column('tokenCount', Integer()),
                           Column('commandName', String(64)),
                           Column('commandType', String(64)),
                           )

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    engine = create_engine('sqlite:///unity_live_odo.db')
    metadata.create_all(engine)

    form_table_src = odo.CSV('unity_form_table.tsv',delimiter='\t',encoding='utf-8')
    utts_table_src = odo.CSV('unity_utts_table.tsv',delimiter='\t',encoding='utf-8')

    #ipdb.set_trace()

    odo.odo(form_table_src, 'sqlite:///unity_live_odo.db::unity_form')
    odo.odo(utts_table_src, 'sqlite:///unity_live_odo.db::unity_utts')

# end main()


if __name__ == "__main__":
    main()
