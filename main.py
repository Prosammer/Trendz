import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px



## TODO: Need to find fix so I can use related_topics instead of related_queries


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2)


# Related Topics, returns a dictionary of dataframes
def related_topics(current_KW):
    # Note: Payload only needed for interest_over_time(), interest_by_region() & related_queries()
    # Max number of queries is 5
    pytrends.build_payload(kw_list=current_KW, timeframe='today 3-m', geo='CA')
    related_topics_dict = pytrends.related_topics()

    for key,innerdict in related_topics_dict.items():
        for k,df in innerdict.items():
            # Selects the rising topics of the dataframe (instead of the top ones)
            if str(k) == 'rising' and df is not None:
                df = df.drop(columns=['link','value'])
                df.to_html('temp.html')
                return(df)


def find_interest():
    print("Commencing interest_over_time search...")
    interest_over_time_df = pytrends.interest_over_time()
    print(interest_over_time_df.head())

    print("Interest_over_time data acquired, pickling...")
    df.to_pickle(F"{kw_list[0]}_vs_{kw_list[1]}.pkl") 





kw_list = ["Juul","Tiktok","Canada"]
current_KW_index = 0
related_topics_df_list = []


if __name__ =='__main__':
    print("The name is main, bitch!")
    
    # -- While loop for assembling keywords -- #
    #while len(kw_list) <= 10:

    #Select the first keyword as a single-item list
    current_KW = [kw_list[current_KW_index]]
    #Creates a list of dataframes with the returned results
    related_topics_df_list.append(related_topics(current_KW))
    
    current_KW_index +=1



    # print("Finding similar topics for: \n\n", current_KW)
    #     #Finds and returns keywords for the current group
    # latest_new_keywords = related_topics(current_KW)
    # for i,k in latest_new_keywords:
    #     for eachdataframe in k:
    #         print(str(eachdataframe))
    #     # for i in latest_new_keywords:
    #     #     if i not in kw_list:
    #     #         kw_list.append(i)
    




    # for each5keywords in master_kw_list:
    #     related_topics(each5keywords)
    #     # Add related topics to kw_list
    #     i += 5
    # keyword_count = 125

    # for each5keywords in master_kw_list:
    #     find_interest()