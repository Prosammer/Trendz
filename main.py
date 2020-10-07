import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors
from sqlalchemy import create_engine




## TODO: Need to find fix so that I can find 5 related terms at a time (fewer requests)
## TODO: Focus on specific categories for more actionable insights?
## TODO: Change all mysql types to be correct (bigint > int, text to varchar etc.)


def df_cleaner(df):
    #Drops any duplicates based on topic_title, and then fixes up the index.
    preclean_len = len(df.index)
    df.drop_duplicates(subset='topic_title', keep='first', inplace=False).reset_index(drop=True)
    cleaned_len = len(df.index)
    if preclean_len != cleaned_len:
        print(abs(preclean_len-cleaned_len)," duplicate records were dropped.")
    return df



def find_interest():
    # if there are unchecked keywords in masterkeyword DF:
        #search for each keyword individually for the last year
        # Add interest numbers to master_interest_df
    print("Commencing interest_over_time search...")
    interest_over_time_df = pytrends.interest_over_time()
    print(interest_over_time_df.head())

def df_list_concatenator(dflist):
    df = pd.concat(dflist)
    cleanedKeywords = df_cleaner(df)
    return cleanedKeywords
    


def related_topics(current_KW):
    # Note: Max number of queries is 5. Payload only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrends.build_payload(kw_list=current_KW, timeframe='today 3-m', geo='CA')
    related_topics_dict = pytrends.related_topics()
    try:
        for key,innerdict in related_topics_dict.items():
            for k,df in innerdict.items():
                # Selects the rising topics of the dataframe (instead of the top ones)
                if str(k) == 'rising' and df is not None:
                    df = df.drop(columns=['link','value'])
                    df['parent'] = str(current_KW)
                    return df 
                    # Returns a single dataframe
    except:
        print("Keyword didn't work - Maybe not enough trends data?")



def retrieve_childless_keywords(num_of_keywords):
    with connection.cursor() as cursor: 
            # Read a single record
            sqlupdate = "UPDATE keywords SET checked = TRUE WHERE checked IS NOT TRUE ORDER BY 'index' DESC LIMIT %d;"  % num_of_keywords
            sqlselect = "SELECT topic_title FROM keywords WHERE checked IS NOT TRUE ORDER BY 'index' DESC LIMIT %d;" % num_of_keywords
            cursor.execute(sqlupdate)
            cursor.execute(sqlselect)
            result = cursor.fetchall()
            print("This is the result of the sqlselect: ", str(result))
            # Returns a list of key:value dicts with topic_tile and keyword
            return result


def submitnewkeywords(df):
    # For each df in list
    df.to_sql('keywords', con = engine, if_exists = 'append', chunksize = 1000)

# Connect to the database
connection = pymysql.connect(host='localhost',
user='root',
password='Jura55ic5',
db='trends',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)


# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
.format(user="root",
pw="Jura55ic5",
db="trends"))

kw_list = ["Canada","Juul","Tiktok","Apple","Buddhism","Axe-Throwing"]
index_kw_list = 0
related_topics_df_list = []

# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2,)

# Set desired number of cycles (for easy testing)
numofcycles = 10

if __name__ =='__main__':
    
    print("Number of Cycles to run: ", str(numofcycles))
    time.sleep(1)
    #Find numofcycles childless keywords in database - returns a list of key:value dicts
    childless_keywords_list = retrieve_childless_keywords(numofcycles)
    
    children_kw_list =[]
    #Find children keywords for all childless keywords
    for i in range(numofcycles):
        related_keywords = related_topics(childless_keywords_list[i].values())
        children_kw_list.append(related_keywords)


    #Concatenate all keywords into a single dataframe before posting
    children_df = df_list_concatenator(children_kw_list)
    submitnewkeywords(children_df)
    print("New keywords submitted!")
    
    

    
    