#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 00:02:26 2017

@author: kkalla

Predict Number of Audiences of Movies
"""

import tensorflow as tf
import pandas as pd

## Read xlsx file
origin_data = pd.read_excel('data/total_movie.xlsx',0)
sub1 = origin_data.iloc[:,[1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]]
# Make target variable
colsum = sub1.iloc[:,12:19].sum(axis=1)
sub2 = sub1.iloc[:,1:11]
sub2.loc[:,'target1']=colsum
sub2.columns
# Drop Nas
sub3 = sub2.dropna(how='any')
# Get dummy variable of genre
sub3.repGenreNm.unique()
sub4 = pd.get_dummies(sub3,columns={'repGenreNm'})
# Get dummy variable of watchGrade
unique_watchGrade = sub4.watchGradeNm.unique()
sub5 = sub4.replace(to_replace={'watchGradeNm':{'12세관람가': '12세이상관람가',
                                         '15세관람가': '15세이상관람가',
                                         '18세관람가': '청소년관람불가'}})
sub6 = pd.get_dummies(sub5,columns={'watchGradeNm'})
sub6.head(n=10)

def company_change(i):
    if i == '소니픽쳐스릴리징월트디즈니스튜디오스코리아(주)' or i == '월트디즈니' or i == '월트디즈니컴퍼니코리아(주)' or i == '월트디즈니코리아㈜':
        return 'walt_disney'
    elif i == '이십세기폭스코리아(주)':
        return 'twentieth_century_fox'
    elif i == '씨제이이앤엠(주)':
        return 'cjenm'
    elif i == '(주)쇼박스':
        return 'showbox'
    elif i == '워너 브러더스 픽쳐스' or i == '워너브러더스 코리아(주)':
        return 'warnerbros'
    elif i == '㈜메가박스' or i == '메가박스(주)플러스엠':
        return 'megabox'
    elif i == '유니버셜 픽쳐스' or i == '유니버설픽쳐스인터내셔널 코리아(유)':
        return 'universal'
    elif i == '(주)넥스트엔터테인먼트월드(NEW)':
        return 'next'
    elif i == '(주)와우픽쳐스':
        return 'wowpictures'
    elif i == '롯데쇼핑㈜롯데엔터테인먼트':
        return 'lotte'
    else:
        return 'other_company'
sub6["companyNm"] = sub6["companyNm"].apply(company_change)
sub6 = pd.get_dummies(sub6,columns={'companyNm'})
sub6.shape
# Make analytic data
mydata = sub6.iloc[:,7:42]
mydata.columns

## Simple Linear Regression
from sklearn.cross_validation import train_test_split
import numpy as np

train_set,test_set = train_test_split(mydata,test_size=0.3)

train_data = train_set.iloc[:,1:].astype(float)
train_target = np.log(np.array(train_set.iloc[:,0]))
test_data = test_set.iloc[:,1:].astype(float)
test_target = np.log(np.array(test_set.iloc[:,0]))

## build linear model
sess = tf.Session()

W = tf.Variable(tf.truncated_normal([34,1],mean=0.0,stddev=1.0,dtype=tf.float64))
b = tf.Variable(tf.zeros([1],dtype=tf.float64))
def calc(x,y):
    pred = tf.add(b,tf.matmul(x,W))
    error = tf.reduce_mean(tf.square(y - pred))
    return [pred,error]

y_pred,error = calc(train_data,train_target)
learning_rate = 0.01
epochs = 1000
points = [[],[]]

init = tf.global_variables_initializer()
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(error)

with sess:
    sess.run(init)
    for i in list(range(epochs)):
        sess.run(optimizer)
        if i%10 == 0.:
            points[0].append(i+1)
            points[1].append(sess.run(error))
        
        if i%100 ==0.:
            print(sess.run(error))
    print('W:'+str(sess.run(W))+' b:'+str(sess.run(b)))
    print('result:'+str(sess.run(tf.add(tf.matmul(sub3.iloc[:,1:35],W),b))))

train_data.columns

sub3['result']=





