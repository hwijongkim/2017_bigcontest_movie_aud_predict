
####final_audience_df data_preprocessing####

import requests
import pandas as pd
import numpy as np
import time
import json
import xlrd
import openpyxl
from bs4 import BeautifulSoup
from xlutils.copy import copy
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,WebDriverException
from selenium import webdriver

# temp_data 파일들 읽어서 합치고 다시 final_audience.xlsx로 저장
total_temp = pd.DataFrame(columns=["movieCd","preview_audience",
                                        "d1_audience","d2_audience","d3_audience","d4_audience","d5_audience","d6_audience","d7_audience",
                                        "d8_audience","d9_audience","d10_audience","d1_screen","d2_screen",
                                        "d3_screen","d4_screen","d5_screen","d6_screen","d7_screen",
                                        "d8_screen","d9_screen","d10_screen","d1_show","d2_show","d3_show",
                                        "d4_show","d5_show","d6_show","d7_show","d8_show","d9_show","d10_show",
                                        "d1_seat","d2_seat","d3_seat","d4_seat","d5_seat","d6_seat","d7_seat",
                                        "d8_seat","d9_seat","d10_seat","audience"])

for i in range(1,3):
    tmp = pd.read_excel('C:/py_saving/movie_data/data_temp'+str(i)+'.xlsx')
    total_temp = total_temp.append(tmp)

total_temp.to_excel('C:/py_saving/movie_data/final_audience2.xlsx', index=False)

final_aud = pd.read_excel('C:/py_saving/movie_data/final_audience2.xlsx')
# change movieCd's type as int
final_aud['movieCd'] = final_aud['movieCd'].astype(int)

# preprocessing varience 'audience' and change type as int(choose only the number is above 10000)
final_aud['audience'] = final_aud['audience'].dropna().apply(lambda x: x.replace(",",""))
final_aud['audience'] = final_aud['audience'].astype(int)
final_aud.fillna(0)
final_aud = final_aud[final_aud['audience'] > 10000]

# change count_format data as int type without ','
def make_num(x):
    try:
        return np.int(x.replace(',',''))
    except:
        try:
            return np.int(x)
        except:
            return np.int(0)

for i in range(1,12):
    final_aud.ix[:,i] = final_aud.ix[:,i].apply(make_num)

# change percent_format data as float type without '%'
def make_float(x):
    try:
        return np.float(x.replace('%',''))
    except:
        try:
            return np.float(x)
        except:
            return np.float(0)

for i in range(12,42):
    final_aud.ix[:,i] = final_aud.ix[:,i].apply(make_float)

#final_audience_df = final_audience_df[final_audience_df["d7_audience"]<1500000].reset_index(drop=True)

boxoffice_df = pd.read_excel('C:/py_saving/movie_data/boxoffice2.xlsx')
final_aud.to_excel('C:/py_saving/movie_data/preprocessed_final_aud2.xlsx', index=False)
total_movie_df = final_aud.merge(boxoffice_df, how='inner', on='movieCd')
total_movie_df = total_movie_df[list(boxoffice_df.columns)+list(final_aud.columns[1:])]
total_movie_df.to_excel('C:/py_saving/movie_data/total_movie2.xlsx', encoding='utf-8', index=False)
    

