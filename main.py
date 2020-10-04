import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px

# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2)



# Related Topics, returns a dictionary of dataframes
def related_topics(current_KW_group):
    # Note: Payload only needed for interest_over_time(), interest_by_region() & related_queries()
    # Max number of queries is 5
    pytrends.build_payload(current_KW_group, timeframe='today 12-m', geo='CA', gprop='')
    related_topics_dict = pytrends.related_topics()
    print("Related Topics:\n\n",related_topics_dict)
    return related_topics_dict


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




kw_list = ["Juul","Tiktok","Sam","Nalgene","Canada","Onlyfans","Android","iPhone","Yukon","Vyvanse"]
current_KW_index = 0




if __name__ =='__main__':
    print("The name is main, bitch!")
    
    # -- While loop for assembling 125 keywords -- #
    while len(kw_list) =< 120:
        # Select the first group of 5 keywords for processing
        current_KW_group = kw_list[current_KW_index:current_KW_index+5]
        print("Finding similar topics for: \n\n", current_KW_group)
        #Finds and returns keywords for the current group
        latest_new_keywords = related_topics(current_KW_group)
        for i in latest_new_keywords:
            if i not in kw_list:
                kw_list.append(i)
        
    for each5keywords in master_kw_list:
        related_topics(each5keywords)
        # Add related topics to kw_list
        i += 5
    keyword_count = 125

    for each5keywords in master_kw_list:
        find_interest()