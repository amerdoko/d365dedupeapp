# ProximitySearch.py
# THIS CODE WILL DO FUZZY SEARCH FOR SEARCH TERM INSIDE A DATABASE. THE PRECENDENCE OF SEARCH STARTS WITH THE # NARROWEST FILTER WHICH SLOWLY WIDENES UP. THE IDEA IS TO GET TO PERFECT MATCHES BEFORE NEAR MATCHES. EACH  # FILTER HAS ITS OWN THRESHOLD CUTOFF.

#IMPORT THE PACKAGES NEEDED
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import os


#DEFINE AND CONFIGURE
FULL_MATCHING_THRESHOLD = 80
PARTIAL_MATCHING_THRESHOLD = 100
SORT_MATCHING_THRESHOLD = 100
TOKEN_MATCHING_THRESHOLD = 100
MAX_MATCHES=1

#READ THE CURRENT DATABASE
companies_db = "C:/Accounts1.csv"
pwd = os.getcwd()
os.chdir(os.path.dirname(companies_db))
current_db_dataframe = pd.read_csv(os.path.basename(companies_db),skiprows=1,index_col=False, names=['Account Name'])
os.chdir(pwd)

def find_matches(matchThis):
    rows = current_db_dataframe['Account Name'].values.tolist();
    rows.remove(matchThis)
    matches= process.extractBests(matchThis,rows,scorer=fuzz.ratio,score_cutoff=FULL_MATCHING_THRESHOLD,limit=MAX_MATCHES)
    if len(matches)==0:
        matches= process.extractBests(matchThis,rows,scorer=fuzz.partial_ratio,score_cutoff=PARTIAL_MATCHING_THRESHOLD,limit=MAX_MATCHES);
        if len(matches)==0:
            matches= process.extractBests(matchThis,rows,scorer=fuzz.token_set_ratio,score_cutoff=TOKEN_MATCHING_THRESHOLD,limit=MAX_MATCHES);
            if len(matches)==0:
                matches= process.extractBests(matchThis,rows,scorer=fuzz.token_sort_ratio,score_cutoff=SORT_MATCHING_THRESHOLD,limit=MAX_MATCHES);
    
    return matches[0][0] if len(matches)>0 else None


fn_find_matches = lambda x: find_matches(x)
current_db_dataframe['Duplicate']=current_db_dataframe.applymap(fn_find_matches)

current_db_dataframe.to_csv("results.csv")