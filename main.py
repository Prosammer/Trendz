import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px



## TODO: Need to find fix so I can use related_topics instead of related_queries


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2)


# Related Topics, returns a dictionary of dataframes
def related_topics(current_KW_group):
    # Note: Payload only needed for interest_over_time(), interest_by_region() & related_queries()
    # Max number of queries is 5
    pytrends.build_payload(kw_list=current_KW_group, timeframe='today 3-m', geo='CA')
    related_topics_dict = pytrends.related_queries()
    related_topics_list = []
    for key,innerdict in related_topics_dict.items():
        for k,df in innerdict.items():
            # Selects the rising topics of each dataframe (instead of the top ones)
            if str(k) == 'rising' and df is not None:
                # Selects the top 5 closest topics in the "query" column and converts them to a list
                series = df.loc[0:4,'query'].to_list()
                # Appends this list to the related topics list
                related_topics_list.append(series)

    # Flattens the list of lists into just a list.
    related_topics_list = [item for sublist in related_topics_list for item in sublist]
    print(len(related_topics_list))


def find_interest():
    print("Commencing interest_over_time search...")
    interest_over_time_df = pytrends.interest_over_time()
    print(interest_over_time_df.head())

    print("Interest_over_time data acquired, pickling...")
    df.to_pickle(F"{kw_list[0]}_vs_{kw_list[1]}.pkl") 





kw_list = ["Juul","Tiktok","Sam","Nalgene","Canada","Adderall","Android","iPhone","Yukon","Vyvanse"]
current_KW_index = 0



if __name__ =='__main__':
    print("The name is main, bitch!")
    
    # -- While loop for assembling 125 keywords -- #
    #while len(kw_list) <= 120:
        # Select the first group of 5 keywords for processing
    current_KW_group = kw_list[current_KW_index:current_KW_index+5]
    related_topics_dict = related_topics(current_KW_group)
    #kw_list.append(related_topics_dict)
    #print(related_topics_dict)
    #current_KW_index +=6


    # print("Finding similar topics for: \n\n", current_KW_group)
    #     #Finds and returns keywords for the current group
    # latest_new_keywords = related_topics(current_KW_group)
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