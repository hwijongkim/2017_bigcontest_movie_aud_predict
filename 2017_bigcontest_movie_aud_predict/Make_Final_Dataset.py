
####더미 변수 생성 및 데이터셋 구성####

import requests
import pandas as pd
import numpy as np
import os
import time
import datetime
import json
from bs4 import BeautifulSoup

data_set = pd.read_xlsx('C:/py_saving/movie_data/total_movie.xlsx')
data_set["openDt"] = data_set["openDt"].apply(lambda x: str(x)[4:6])

def month_change(i):
    if i == "01":
        return 'jan'
    elif i == '02':
        return 'feb'
    elif i == '03':
        return 'mar'
    elif i == '04':
        return 'apr'
    elif i == '05':
        return 'may'
    elif i == '06':
        return 'jun'
    elif i == '07':
        return 'jul'
    elif i == '08':
        return 'aug'
    elif i == '09':
        return 'sep'
    elif i == '10':
        return 'oct'
    elif i == '11':
        return 'nov'
    else:
        return 'dec'
data_set["openDt"] = data_set["openDt"].apply(month_change)

def grade_change(i):
    if i == '연소자관람가' or i == "모든 관람객이 관람할 수 있는 등급" or i == '전체관람가':
        return 'G'
    elif i == '12세관람가' or i == '12세이상관람가' or i == '국민학생관람불가' or i == '연소자관람불가' or i == '중학생이상관람가' or i == 'nan':
        return 'PG_13'
    elif i == '15세관람가' or i == '15세이상관람가' or i == '15세 미만인 자는 관람할 수 없는 등급 ' or i == '고등학생이상관람가':
        return 'R'
    elif i == '18세관람가' or i == '청소년관람불가':
        return 'NC_17'
    else:
        return i
data_set["watchGradeNm"] = data_set["watchGradeNm"].apply(grade_change)

data_set["showTm"] = data_set["showTm"].astype(int)

def time_change(i):
    if i < 90:
        return 'under_90'
    elif i >= 90 and i < 120:
        return '90_120'
    elif i >=120 and i < 150:
        return '120_150'
    else:
        return '150_up'

data_set["showTm"] = data_set["showTm"].apply(time_change)

