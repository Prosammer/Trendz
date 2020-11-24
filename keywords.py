import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors
from sqlalchemy import create_engine, exc

## TODO: Need to find fix so that I can find 5 related terms at a time (fewer requests)
## TODO: Focus on specific categories for more actionable insights?
## TODO: Decide if I want to keep the GEO for both functions as Canada
## TODO: Should look into  "['link' 'value'] not found in axis" error during related topics lookup


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2,)


# Connect to the database

connection = pymysql.connect(host='localhost',
user='root',
password=password,
db='trends',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)


# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
.format(user="root",
pw=password,
db="trends"))




def df_cleaner(df):
    #Drops any duplicates based on topic_title, and then fixes up the index.
    preclean_len = len(df.index)
    df.drop_duplicates(subset='topic_title', keep='first', inplace=False).reset_index(drop=True)
    cleaned_len = len(df.index)
    if preclean_len != cleaned_len:
        print(abs(preclean_len-cleaned_len)," duplicate records were dropped.")
    return df

def df_list_concatenator(dflist):
    df = pd.concat(dflist)
    cleanedKeywords = df_cleaner(df)
    return cleanedKeywords



def related_topics(current_KW):
    # Note: Max number of queries is 5. Payload only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrends.build_payload(kw_list=[current_KW], timeframe='today 3-m', geo='CA')
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
    except Exception as e:
        print("This is the exception:\n\n\n", str(e))


def retrieve_childless_keywords(num_of_keywords):
    with connection.cursor() as cursor: 
            # Read a single record
            sqlselect = "SELECT topic_title FROM keywords WHERE checked IS NOT TRUE ORDER BY 'id' DESC LIMIT %d;" % num_of_keywords
            sqlupdate = "UPDATE keywords SET checked = TRUE WHERE checked IS NOT TRUE ORDER BY 'id' DESC LIMIT %d;" % num_of_keywords
            cursor.execute(sqlselect)
            # Returns a list of key:value dicts with 'topic_title':keyword
            listofdicts = cursor.fetchall()
            resultlist = [f['topic_title'] for f in listofdicts]
            cursor.execute(sqlupdate)
            connection.commit()
            return resultlist
            


def submitnewkeywords(df):
    #Uses sqlalchemy to submit the concatenated dataframe to mysql (doesn't check for duplicates)
        #df.to_sql('pandas_temp',index = False, con = engine, if_exists = 'replace')

    df.to_sql(name='pandas_temp', con=engine, if_exists = 'replace', index=False)

    with connection.cursor() as cursor:
        insert_sql = "INSERT IGNORE INTO keywords (formattedValue,topic_mid,topic_title,topic_type,parent) SELECT formattedValue,topic_mid,topic_title,topic_type,parent FROM pandas_temp"
        cursor.execute(insert_sql)
        connection.commit()
        connection.close()





# Set desired number of cycles (for easy testing)
numofcycles = 100

if __name__ =='__main__':
    
    print("Number of Cycles to run: ", str(numofcycles))
    #Find numofcycles childless keywords in database
    childless_keywords_list = retrieve_childless_keywords(numofcycles)
    children_kw_list =[]
    
    #Find children keywords for all childless keywords
    for i in childless_keywords_list:
        time.sleep(2)
        try:
            print("Running keyword: ",str(i))
            related_keywords = related_topics(i)
            children_kw_list.append(related_keywords)
        except Exception as e:
            print(str(e))
            
    #Concatenate all keywords into a single dataframe before posting
    print("Running list concatenator...\n\n")
    children_df = df_list_concatenator(children_kw_list)

    print("Running submit newkeywords...\n\n")
    submitnewkeywords(children_df)
    print("New keywords submitted!")
    
    

    
    