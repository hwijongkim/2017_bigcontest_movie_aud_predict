
####Movie_info_WebCrawling_Script####

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

boxoffice_df = pd.read_excel("C:/py_saving/movie_data/boxoffice2.xlsx")

driver = webdriver.Chrome("C:\py_saving/chromedriver.exe")

final_audience_df = pd.DataFrame(columns=["movieCd","preview_audience",
                                        "d1_audience","d2_audience","d3_audience","d4_audience","d5_audience","d6_audience","d7_audience",
                                        "d8_audience","d9_audience","d10_audience","d1_screen","d2_screen","d3_screen","d4_screen","d5_screen",
                                        "d6_screen","d7_screen","d8_screen","d9_screen","d10_screen",
                                        "d1_show","d2_show","d3_show","d4_show","d5_show","d6_show","d7_show",
                                        "d8_show","d9_show","d10_show","d1_seat","d2_seat","d3_seat","d4_seat",
                                        "d5_seat","d6_seat","d7_seat","d8_seat","d9_seat","d10_seat",
                                        "audience"])

#끊겼을 때 그때까지 긁어온 데이터 엑셀파일로 export.
#final_audience_df.to_excel('C:/py_saving/movie_data/data_temp2.xlsx', index=False)

movieCd = boxoffice_df['movieCd']
movieNm = boxoffice_df['movieNm']

#추가로 돌릴 때는 boxoffice2의 1473(더 라이트: 악마는 있다)부터 시작함.
for i in range(1595,len(boxoffice_df)):
    driver.get("http://www.kobis.or.kr/kobis/business/mast/mvie/searchUserMovCdList.do")
    
    #검색코드 설정
    code = movieCd[i]
    code = int(code)
    tmp = [code] #영화코드에 해당하는 목적 데이터들 저장하는 임시 리스트.
    
    #검색
    try:
        search = driver.find_element_by_name('movieCd')
        search.send_keys(code)
        search.submit()
        tb = driver.find_element_by_class_name('boardList03')
        title = tb.find_element_by_tag_name('a')
        title.click()
    except WebDriverException:
        continue

    tab = driver.find_element_by_class_name('tab_layer')
    info = tab.find_element_by_link_text('통계정보')
    info.click()
    ####영화코드 검색 결과 페이지####
    try:
        tables = []
        cnt=0
        while(len(tables)!=9):
            tables = []
            tables_all = driver.find_elements_by_tag_name('table')
            for j in range(0,len(tables_all)):
                if tables_all[j].text!='':
                    tables.append(tables_all[j])
            cnt = cnt+1
            if cnt>200:
                break
        if cnt>200:
            continue
        tbody = tables[6].find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')
        if len(trs)<11:
            continue
        else:
            for z in range(0,11):
                tds = trs[z].find_elements_by_tag_name('td')
                if z == 0:
                    preview_audience = tds[6].text
                    tmp.append(preview_audience)
                else:
                    tmp.append(tds[2].text)
                    tmp.append(tds[4].text)
                    tmp.append(tds[6].text)
                    tmp.append(tds[7].text)
            tfoot = tables[8].find_element_by_tag_name('tfoot')
            tds = tfoot.find_elements_by_tag_name('td')
            tmp.append(tds[4].text[:-6])
            index=['movieCd','preview_audience','d1_screen','d1_show','d1_audience','d1_seat',
               'd2_screen','d2_show','d2_audience','d2_seat','d3_screen','d3_show','d3_audience',
               'd3_seat','d4_screen','d4_show','d4_audience','d4_seat','d5_screen','d5_show',
               'd5_audience','d5_seat','d6_screen','d6_show','d6_audience','d6_seat','d7_screen',
               'd7_show','d7_audience','d7_seat','d8_screen',
               'd8_show','d8_audience','d8_seat','d9_screen',
               'd9_show','d9_audience','d9_seat','d10_screen',
               'd10_show','d10_audience','d10_seat','audience']
            final_audience_df = final_audience_df.append(pd.Series(tmp, index),ignore_index=True)
        
    except NoSuchElementException:
        print(code,"[표 없음]")
    continue

driver.quit()
end_time = time.time()
print(end_time-start_time)
            
        
        
        
        