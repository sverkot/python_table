# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import pandas as pd
from pandas import DataFrame
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.max_colwidth = 100
pd.options.mode.chained_assignment = None

#Statistics of HINCP - Household income (past 12 months), grouped by HHT - Household/family type
def householdIncomeByType(df):
    hht_description = { 1:'Married couple household',
                        2:'Other family household:Male householder, no wife present',
                        3:'Other family household:Female householder, no husband present',
                        4:'Nonfamily household:Male householder:Living alone',
                        5:'Nonfamily household:Male householder:Not living alone',
                        6:'Nonfamily household:Female householder:Living alone',
                        7:'Nonfamily household:Female householder:Not living alone'}
    hht = df.HHT
    hht.replace(hht_description, inplace=True)
    hincp = df.HINCP
    hincp_grouped = hincp.groupby(hht)
    stat_df = hincp_grouped.apply(get_stats).unstack()
    stat_df = stat_df.sort_values('mean',ascending=False)
    stat_df.index.names = ['HHT - Household/family type']
    stat_df = stat_df[['mean', 'std', 'count', 'min', 'max']]
    print ''
    print('*** Table 1 - Descriptive Statistics of HINCP, grouped by HHT ***')
    print stat_df

#HHL - Household language vs. ACCESS - Access to the Internet (Frequency Table)

def householdLanguageVsAccess(df):
    df = df.dropna(subset = ['ACCESS'])
    hhl = df['HHL']
    access = df['ACCESS']

    hhl_description ={  1 :'English only',
                        2 :'Spanish',
                        3 :'Other Indo-European languages',
                        4 :'Asian and Pacific Island languages',
                        5 :'Other language'}

    hhl.replace(hhl_description, inplace=True)
    access = df['ACCESS']
    access_description ={   1 :'Yes w/ Subscr.',
                            2 :'Yes, w/o Subscr',
                            3 :'No'}
    access.replace(access_description,inplace=True)
    new_df = pd.crosstab(df.HHL,df.ACCESS,values=df.WGTP,aggfunc=np.sum,margins=True).applymap(lambda x:'{:.2%}'.format(x/float(df.WGTP.sum())))
    new_df = new_df[['Yes w/ Subscr.', 'Yes, w/o Subscr', 'No','All']]
    new_df = new_df.reindex(['English only','Spanish','Other Indo-European languages','Asian and Pacific Island languages','Other language','All'])

    print ''
    print '*** Table 2 - HHL vs. ACCESS - Frequency Table ***'
    print new_df

#Quantile Analysis of HINCP - Household income (past 12 months)
def quantileAnalysisHouseholdIncome(df):
    hincp = df['HINCP']
    hincp_grouping = pd.qcut(hincp,3,labels=['low','medium','high'])
    hincp_grouped = hincp.groupby(hincp_grouping)
    grouped_by_weight =df.WGTP.groupby(hincp_grouping)
    quant_df = hincp_grouped.apply(get_stats).unstack()
    quant_df = quant_df[['min','max','mean']]
    quant_df.loc[:,'household_count'] = grouped_by_weight.sum()

    print ''
    print '*** Table 3 - Quantile Analysis of HINCP - Household income (past 12 months) ***'
    print quant_df

#Function that returns the aggregate values of the groupby object
def get_stats(group):
    return {'min': group.min(),'max': group.max(),
            'mean': group.mean(),'std':group.std(),'count':group.count()}
def main():
    pums = pd.read_csv('ss13hil.csv')
    df = DataFrame(pums)
    #Statistics of HINCP - Household income (past 12 months), grouped by HHT - Household/family type
    householdIncomeByType(df)
    #HHL - Household language vs. ACCESS - Access to the Internet (Frequency Table)
    householdLanguageVsAccess(df)
    #Quantile Analysis of HINCP - Household income (past 12 months)
    quantileAnalysisHouseholdIncome(df)

if  __name__ =='__main__':main()
