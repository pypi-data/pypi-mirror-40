# coding: utf-8
from __future__ import print_function,division
import pandas as pd
import numpy as np
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
            raise Exception("input data.dtype is not Pandas.DataFrame")
        mvr = data.isnull().sum()/len(data)
        self.score = mvr
        self.col = filter(lambda x:dict(mvr).get(x)> self.threshold,data.columns)
        return self

    def transfrom(self,data):
        '''
        :param data: input data
        :return:
        '''
        data.drop(self.col,axis=1,inplace = True)
        return data

    def fit_transfrom(self,data):
        '''
        :param data: input data
        :return:
        '''
        self.fit(data)
        return self.transfrom(data)

class LVF(object):

    def __init__(self):
        pass

