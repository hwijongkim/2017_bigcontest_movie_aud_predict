
####영화진흥위원회 api####

import requests
import pandas as pd
import numpy as np
import os
import time
import datetime
import json

csv_list = [file for file in os.listdir("C:/py_saving/movie_data/box_office_by_year")]
for i,data in enumerate(csv_list):
    csv_list[i] = 'C:/py_saving/movie_data/box_office_by_year/' + data

for i, data in enumerate(csv_list):
    if i == 0:
        df = pd.read_excel(data)
    else:
        small_df = pd.read_excel(data)
        df = pd.concat([df, small_df]).reset_index(drop=True)

movie_df = df[df["관객수"] > 10000].reset_index(drop=True)
movie_df = movie_df.drop(movie_df.index[[len(movie_df)-1]])
movie_df = movie_df.drop_duplicates("영화명").reset_index(drop=True)

movie_df.to_excel("C:/py_saving/movie_data/movie2.xlsx",encoding="utf-8", index= False)

movie_name = movie_df["영화명"]

def get_movie_data(movie_name):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    params = {"key":"d4a2c02ea2388a7a8d0ecf41d2dd922e", "movieNm":movie_name}
    r = requests.get(url, params)
    return r.json()

def make_movie_df(movie_name):
    movie_df = pd.DataFrame(columns = ["movieCd", "movieNm", "director","prdtYear", "openDt", "typeNm", "repNationNm", "repGenreNm", "companyNm"])
    for i in list(movie_name):
        try:
            for data in get_movie_data(i)['movieListResult']['movieList']:
                if len(data["directors"]) >=2:
                    director = data["directors"][0]["peopleNm"]
                elif len(data["directors"]) == 1:
                    director = data["directors"][0]["peopleNm"]
                if len(data["companys"]) >=2:
                    companyNm = data["companys"][0]["companyNm"]
                elif len(data["companys"]) == 1:
                    companyNm = data["companys"][0]["companyNm"]
                movie_df.loc[len(movie_df)] = [
                    data["movieCd"],
                    data["movieNm"],
                    director,
                    data["prdtYear"],
                    data["openDt"],
                    data["typeNm"],
                    data["repNationNm"],
                    data["repGenreNm"],
                    companyNm
                ]
        except:
            print(i)
    return movie_df

movie_info_df = make_movie_df(movie_name)

movie_info_df = movie_info_df[~movie_info_df["movieNm"].str.contains("시네마정동")].reset_index(drop=True)
movie_info_df = movie_info_df[movie_info_df["repNationNm"] != "기타"].reset_index(drop=True)
movie_info_df = movie_info_df.drop_duplicates("movieCd").reset_index(drop=True)
movie_info_df = movie_info_df.drop_duplicates("movieNm").reset_index(drop=True)
movie_info_df = movie_info_df[movie_info_df["openDt"] != ""].reset_index(drop=True)

movie_info_df.to_excel("C:/py_saving/movie_data/movie_info2.xlsx",encoding="utf-8", index=False)

movieCd = movie_info_df["movieCd"][:len(movie_info_df)-1]

def get_movie_detail(movieCd):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
    params = {"key":"3ad66aa69af2d7e0227d159339613268", "movieCd":movieCd}
    r = requests.get(url, params=params)
    return r.json()

def make_movie_detail_df(movie_info_df):
    movie_detail_df = pd.DataFrame(columns=["movieCd", 
                                            "movieNm", 
                                            "showTm", 
                                            "watchGradeNm", 
                                            "actor_1",
                                            "actor_2",
                                            "actor_3",
                                            "companyNm"
                                            ])
    for i in list(movieCd):
        try:
            data = get_movie_detail(i)['movieInfoResult']['movieInfo']
            actor_list = []
            if len(data["audits"]) >= 2:
                watchGradeNm = data["audits"][0]["watchGradeNm"]
            elif len(data["audits"]) == 1:
                watchGradeNm = data["audits"][0]["watchGradeNm"]
            if len(data["companys"]) >= 2:
                companyNm = data["companys"][0]["companyNm"]
            elif len(data["companys"]) == 1:
                companyNm = data["companys"][0]["companyNm"] 
            if len(data["actors"]) >= 3:
                actor_list = [
                    data["actors"][0]["peopleNm"],
                    data["actors"][1]["peopleNm"],
                    data["actors"][2]["peopleNm"]
                ]
            else:
                for i in range(len(data["actors"])):
                    actor_list.append(data["actors"][i]["peopleNm"])
                for i in range(3-len(data["actors"])):
                    actor_list.append("")
            movie_detail_df.loc[len(movie_detail_df)] = [
                data["movieCd"],
                data["movieNm"],
                data["showTm"],
                watchGradeNm,
                *actor_list,
                companyNm
            ]
        except:
             print(i)
    return movie_detail_df

movie_detail_df = make_movie_detail_df(movieCd)

boxoffice_df = movie_info_df.merge(movie_detail_df, left_on="movieCd", right_on="movieCd")[[
        "movieCd",
        "movieNm_x",
        "director",
        "openDt",
        "prdtYear",
        "repNationNm",
        "repGenreNm",
        "showTm",
        "watchGradeNm",
        "actor_1",
        "actor_2",
        "actor_3",
        "companyNm_y"
    ]]
boxoffice_df = boxoffice_df.rename(columns={"movieNm_x":"movieNm", "companyNm_y":"companyNm"})
boxoffice_df.to_excel("C:/py_saving/movie_data/boxoffice2.xlsx", encoding="utf-8", index = False)
    