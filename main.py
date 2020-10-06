import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px



## TODO: Need to find fix so that I can find 5 related terms at a time (fewer requests)
## TODO: Focus on specific categories for more actionable insights?

## TODO: Next I need to add columns to the masterkeywordDF so that I know 
# which words have been searched for. Then I need to add logic to only search new words. 
# I'd also like a "parent" word column for tree diagrams.


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)


def dupe_cleaner(df):
    preclean_len = len(df.index)
    df.drop_duplicates(subset='topic_title', keep='first', inplace=False)
    cleaned_len = len(df.index)
    if preclean_len != cleaned_len:
        print(abs(preclean_len-cleaned_len)," duplicate records were dropped.")
    return df


# Related Topics, returns a dictionary of dataframes
def related_topics(current_KW):
    # Note: Payload only needed for interest_over_time(), interest_by_region() & related_queries()
    # Max number of queries is 5
    pytrends.build_payload(kw_list=current_KW, timeframe='today 3-m', geo='CA')
    related_topics_dict = pytrends.related_topics()
    try:
        for key,innerdict in related_topics_dict.items():
            for k,df in innerdict.items():
                # Selects the rising topics of the dataframe (instead of the top ones)
                if str(k) == 'rising' and df is not None:
                    df = df.drop(columns=['link','value'])
                    df.to_html('temp.html')
                    return df 
    except:
        print("Keyword didn't work!")


def find_interest():
    print("Commencing interest_over_time search...")
    interest_over_time_df = pytrends.interest_over_time()
    print(interest_over_time_df.head())

    print("Interest_over_time data acquired, pickling...")
    df.to_pickle(F"{kw_list[0]}_vs_{kw_list[1]}.pkl") 


def keyword_adder():
# -- While loop for assembling keywords -- #
    while len(kw_list) <= 25:
        # Select the first keyword as a single-item list
        current_KW = [kw_list[index_kw_list]]
        # Creates a list of dataframes with the returned results (to be merged later)
        newtopics_df = related_topics(current_KW)
        related_topics_df_list.append(newtopics_df)
        # Adds keywords to kw_list for efficiency
        try:
            for i in newtopics_df.topic_title:
                # Only adds unique keywords
                if i not in kw_list:
                    kw_list.append(i)
        except:
            pass
        index_kw_list +=1
        print("Index: ",index_kw_list)
        print("Length of kw_list",len(kw_list))
        time.sleep(1)

 







pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2,)
kw_list = ["Canada","Juul","Tiktok","Apple","Buddhism","Axe-Throwing"]
index_kw_list = 0
related_topics_df_list = []


if __name__ =='__main__':
    # keyword_adder()
    # dupe_cleaner()

    masterkeywordDF = pd.concat(related_topics_df_list)
    masterkeywordDF.to_pickle("masterkeywordDF.pkl")
    masterkeywordDF.to_html('masterkeywordDF.html')