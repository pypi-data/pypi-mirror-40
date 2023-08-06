# coding: utf-8
from __future__ import print_function,division
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.feature_selection import  SelectFromModel
import matplotlib.pyplot as plt
class MVR(object):
    '''
    Missing Value Ratio
    '''
    def __init__(self,threshold=0.2):
        '''
        :param threshold:  missiong value ratio threshold
        '''
        if isinstance(threshold,float):
            if threshold >=0 and threshold <=1:
                self.threshold = threshold
            else:
                raise Exception("the threshlod must between 0 ans 1")
        else:
            raise Exception("threshold is not float")


    def fit(self,data):
        '''
        :param data: input data
        :return:
        '''
        if isinstance(data,pd.DataFrame):
            pass
        else:
            raise Exception("inputdata.dtype is not Pandas.DataFrame")
        self.score = data.isnull().sum()/len(data)
        self.col = filter(lambda x:dict(self.score ).get(x)> self.threshold,data.columns)
        return self

    def transform(self,data):
        '''
        :param data: input data
        :return:
        '''
        data.drop(self.col,axis=1,inplace = True)
        return data

    def fit_transform(self,data):
        '''
        :param data: input data
        :return:
        '''
        self.fit(data)
        return self.transform(data)
class LVF(object):
    '''
    Low Variance Filter
    '''
    def __init__(self,filter = False,threshold = 0.01,fillna='mean',fillvalue=None,inplace = False):
        '''

        :param filter:
        :param threshold:
        :param fillna: mean median mode
        '''
        self.filter = filter
        self.threshold = threshold
        if fillna in set(['mean','median','mode','value']):
            self.fillna = fillna
        else:
            raise Exception('the fillna type :%s is not included'%fillna)
        self.fillvalue = fillvalue
        self.inplace = inplace

    def fit(self,data):
        if isinstance(data,pd.DataFrame):
            pass
        else:
            raise Exception('inputdata.dtype is not Pandas.DataFrame')
        if self.fillna == 'value' and self.fillvalue==None:
            self.fillna1 = 'mean'
        else:
            self.fillna1 = self.fillna
        colnew = []
        for colname in data.columns:
            if data[colname].dtypes == 'float' or data[colname].dtypes == 'int':
                if self.inplace == True:
                    colnamenew = colname
                else:
                    colnamenew = colname+'_'
                if self.fillna1 == 'mean':
                    data[colnamenew] = data[colname].fillna(data[colname].mean())
                elif self.fillna1 == 'median':
                    data[colnamenew] = data[colname].fillna(data[colname].median())
                elif self.fillna1 == 'mode':
                    data[colnamenew] = data[colname].fillna(data[colname].mode()[0])
                else:
                    data[colnamenew] = data[colname].fillna(self.fillvalue)
                colnew.append(colnamenew)
        self.colnew = colnew
        self.cv = ((data[colnew]).std())/((data[colnew]).mean())
        self.colfilter = filter(lambda x: dict(self.cv).get(x) < self.threshold, self.colnew)
        return self

    def transform(self,data):
        if self.filter == True:
            data.drop(self.colfilter, axis=1, inplace=True)
        return data

    def fit_transform(self,data):
        self.fit(data)
        return self.transform(data)




class HCF(object):
    '''
    High Correlation Filter
    '''
    def __init__(self,corr_filter = 'High'):
        '''
        :param corr_filter:
        :param y_corr_filter:
        0.8-1.0 Extreme
        0.6-0.8 High
        0.4-0.6 Middle
        0.2-0.4 Weak
        0.0-0.2 Little
        '''
        self.corr_filter = corr_filter
    def getCorrMatrix(self,data):
        if isinstance(data,pd.DataFrame):
            if data.shape[1]>1:
                return  data.corr()
            else:
                raise Exception('input data must more than one sample')
        else:
            raise Exception('input data must Pandas.DataFrame')
    def __getThreshold(self,grade):
        if grade == 'Extreme':
            return [0.8,1.0]
        elif grade == 'High':
            return [0.6,0.8]
        elif grade == 'Middle':
            return [0.4,0.6]
        elif grade == 'Weak':
            return [0.2,0.4]
        elif grade == 'Little':
            return [0.0,0.2]
        else:
            raise Exception('the corr grade is invalid')

    def fit(self,data,**kwargs):
        '''

        :param data:
        :param ycol:
        :param kwargs: corr_filter,y_corr_filter
        :return:
        '''
        self.corr = None
        self.col = None
        for k,v in kwargs.items():
            self.__dict__[k] = v
        self.corr = self.getCorrMatrix(data)
        x_col = set(self.corr.columns)
        x_col1 = set()
        x_col2 = set()
        grade = self.__getThreshold(self.corr_filter)[0]
        x_mean = self.corr.mean()
        for col in x_col:
            x_filter = filter(lambda x:abs((self.corr[col]).loc[x])>=grade and col!=x,x_col)
            if len(x_filter)==0:
                continue
            x_filter_mean = dict(x_mean[x_filter])
            x_target = max(x_filter_mean,key=x_filter_mean.get)
            x_col1.add(x_target)
            x_filter.remove(x_target)
            x_col2 = x_col2|set(x_filter)
        self.filter_columns = list(x_col2 - x_col1)
        return self

    def transform(self,data):
        data.drop(self.filter_columns, axis=1, inplace=True)
        return data
    def fit_transform(self,data,**kwargs):
        self.corr = None
        self.col = None
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.corr = self.getCorrMatrix(data)
        x_col = set(self.corr.columns)
        x_col1 = set()
        x_col2 = set()
        grade = self.__getThreshold(self.corr_filter)[0]
        x_mean = self.corr.mean()
        for col in x_col:
            x_filter = filter(lambda x: abs((self.corr[col]).loc[x]) >= grade and col != x, x_col)
            if len(x_filter) == 0:
                continue
            x_filter_mean = dict(x_mean[x_filter])
            x_target = max(x_filter_mean, key=x_filter_mean.get)
            x_col1.add(x_target)
            x_filter.remove(x_target)
            x_col2 = x_col2 | set(x_filter)
        self.filter_columns = list(x_col2 - x_col1)
        return self.transform(data)

class RF(object):

    def __init__(self,mtype = 'C'):
        '''
        :param mtype: C R
        '''
        self.mtype = mtype

    def fit(self,x,y):
        if self.mtype=='C':
            model = RandomForestClassifier()
        elif self.mtype=='R':
            model = RandomForestRegressor()
        else:
            raise Exception('the model type value %s is invalid!'%self.mtype)
        model.fit(x,y)
        self.feature_important = model.feature_importances_
        self.filter_model = SelectFromModel(model).fit(x,y)
        return self

    def transform(self,x):
        return self.filter_model.transform(x)

    def fit_transform(self,x,y):
        self.fit(x,y)
        return self.transform(x)






