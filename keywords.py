import logging
import sys
import time

import pandas as pd
import psycopg2
from pytrends.request import TrendReq
import sqlalchemy
from sqlalchemy import create_engine


# TODO: Need to find fix so that I can find 5 related terms at a time (fewer requests)
# TODO: Change to specific categories
# TODO: Change logic to save both "rising" and "top" topics
# TODO: Need to change code to set checked=true only after keywords have been successfully added
def setup():
    """ Sets up logging and connections to pytrends and mysql"""
    proxylist = [
        "https://104.168.51.141:3128",
        "https://192.186.134.157:3128",
        "https://192.3.214.40:3128",
        "https://104.144.220.10:3128",
        "https://104.144.28.167:3128",
        "https://172.245.181.226:3128",
        "https://192.210.185.193:3128",
        "https://23.236.232.162:3128",
        "https://23.254.68.49:3128",
        "https://23.94.176.161:3128",
        "https://69.4.90.17:3128",
        "https://107.172.94.128:3128",
        "https://138.128.84.159:3128",
        "https://192.186.161.228:3128",
        "https://192.241.64.90:3128",
        "https://192.241.80.170:3128",
        "https://198.12.80.148:3128",
        "https://198.23.217.80:3128",
        "https://23.250.94.234:3128",
        "https://45.72.0.245:3128",
    ]

    logging.root.handlers = []
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler("debug.log", mode="w"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.info("Greetings, Pleb!")
    logging.info(f"Number of keywords to find: {num_of_keywords}")

    pytrends = TrendReq(hl="en-CA", tz=-240, retries=2, backoff_factor=0.2)

    # Get database password from file:
    f = open("secrets.txt", "r")
    lines = f.readlines()
    password = lines[0]
    f.close()

    connection = psycopg2.connect(
        database="postgres",
        user="igu8o7iu@trends-timescale-db.postgres.database.azure.com",
        password=password,
        host="trends-timescale-db.postgres.database.azure.com",
        port=5432,
        sslmode="require",
    )

    # create sqlalchemy engine
    engine = create_engine(
        "postgresql+psycopg2://{user}:{pw}@trends-timescale-db.postgres.database.azure.com/{db}".format(
            user="igu8o7iu@trends-timescale-db", pw=password, db="postgres"
        )
    )

    return connection, pytrends, engine


def df_cleaner(df):
    # Drops any duplicates based on topic_mid, and then fixes up the index.
    preclean_len = len(df.index)
    df.drop_duplicates(subset="topic_mid", keep="first", inplace=False).reset_index(
        drop=True
    )
    cleaned_len = len(df.index)
    if preclean_len != cleaned_len:
        print(abs(preclean_len - cleaned_len), " duplicate records were dropped.")
    return df


def df_list_concatenator(dflist):
    df = pd.concat(dflist)
    cleaned_keywords = df_cleaner(df)
    return cleaned_keywords


def related_topics(current_kw):
    # Note: Max number of queries is 5.
    # Payload only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrends.build_payload(kw_list=[current_kw], timeframe="today 3-m", geo="US")
    related_topics_dict = pytrends.related_topics()
    try:
        for key, innerdict in related_topics_dict.items():
            for k, df in innerdict.items():
                # Selects the rising topics of the dataframe (instead of the top ones)
                if str(k) == "rising" and df is not None:
                    print(df.head())
                    df = df.drop(columns=["link", "value"])
                    df["parent"] = str(current_kw)
                    # Returns a single dataframe
                    print("\n\n---------------------\n\n\n")
                    print(df.head())
                    return df
    except Exception as e:
        print("This is the exception:\n\n\n", str(e))


def retrieve_childless_keywords(num_of_keywords, connection):
    with connection.cursor() as cursor:
        # Read a single record
        sqlselect = (
            "SELECT id, topic_title FROM keywords WHERE checked IS NOT TRUE ORDER BY id DESC LIMIT %d;"
            % num_of_keywords
        )
        cursor.execute(sqlselect)
        # Returns a list of key:value dicts with 'topic_title':keyword
        listofdicts = cursor.fetchall()

        idlist = [f[0] for f in listofdicts]
        resultlist = [f[1] for f in listofdicts]
        idtuple = tuple(idlist)
        return resultlist, idtuple


def submitnewkeywords(df, connection,engine, idtuple):
    # Uses sqlalchemy to submit the concatenated dataframe to mysql (doesn't check for duplicates)
    # df.to_sql('pandas_temp',index = False, con = engine, if_exists = 'replace')

    df.to_sql(
        name="pandas_temp",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={"formattedValue": sqlalchemy.types.VARCHAR(length=128)},
    )

    with connection.cursor() as cursor:
        try:
            insert_sql = """INSERT INTO keywords ("formattedValue","topic_mid","topic_title","topic_type","parent") SELECT "formattedValue","topic_mid","topic_title","topic_type","parent" FROM pandas_temp"""
            cursor.execute(insert_sql)
            sqlupdate = "UPDATE keywords SET checked = TRUE WHERE id IN {}".format(idtuple)
            cursor.execute(sqlupdate)
        except psycopg2.errors.UniqueViolation:
            print("Some topics already existed:\n\n",psycopg2.errors.UniqueViolation)
        connection.commit()
        connection.close()

def checked_column_update(idtuple):





num_of_keywords = 2

if __name__ == "__main__":
    # Set desired number of cycles (for easy testing)

    connection, pytrends, engine = setup()
    print("Number of Cycles to run: ", str(num_of_keywords))

    # Find num_of_keywords childless keywords in database
    childless_keywords_list, idtuple = retrieve_childless_keywords(num_of_keywords, connection)
    # childless_keywords_list = open("starter_keywords.txt").readlines()
    children_kw_list = []
    # Find children keywords for all childless keywords
    for i in childless_keywords_list:
        try:
            print("Running keyword: ", str(i))
            time.sleep(1)
            related_keywords = related_topics(i)
            children_kw_list.append(related_keywords)
        except Exception as e:
            print(str(e))

    # Concatenate all keywords into a single dataframe before posting
    print("Running list concatenator...\n\n")
    children_df = df_list_concatenator(children_kw_list)

    print("Running submit newkeywords...\n\n")
    submitnewkeywords(children_df,connection, engine, idtuple)
    print("New keywords submitted!")
