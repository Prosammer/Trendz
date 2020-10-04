import pandas as pd
import os, requests, time
from pytrends.request import TrendReq
import plotly.express as px


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2)

kw_list = ["Juul", "Tiktok"]

# Note: Payload only needed for interest_over_time(), interest_by_region() & related_queries()
# Max number of queries is 5
pytrends.build_payload(kw_list, timeframe='today 1-m', geo='CA', gprop='')

def related_words():
    # Related Queries, returns a dictionary of dataframes
    related_queries_dict = pytrends.related_queries()
    print("Related Queries:\n\n",related_queries_dict)

def suggested_words():
    suggestions_dict = pytrends.suggestions(keyword='Juul')
    print("Suggestions:\n\n", suggestions_dict)
    

def find_interest():
    try:
        
        # Simple test dataframe:
            #df = pd.DataFrame(dict(a=[1,3,2], b=[3,2,1]))
        #   Main data-retrieval function:
        print("Commencing interest_over_time search...")
        interest_over_time_df = pytrends.interest_over_time()
        print(interest_over_time_df.head())

        print("Interest_over_time data acquired, pickling...")
        df.to_pickle(F"{kw_list[0]}_vs_{kw_list[1]}.pkl") 
    except pytrends.requests.exceptions.Timeout:
        print("Timeout bruv")


if __name__ =='__main__':
    print("The name is main, bitch!")
    related_words()