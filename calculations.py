# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 23:09:42 2021

@author: Tejas
"""


import pandas as pd


df_pipe = pd.read_csv('C:/Users/Tejas/OneDrive - Northeastern University/Core Model V1/PipelineSheets' + '/Oct19toMay20.csv')

df_res = pd.read_csv('C:/Users/Tejas/OneDrive - Northeastern University/Core Model V1/LatestData/HistoricFull_V1.4_May_2021.csv')



df_new = df_pipe.merge(df_res[['trialId', 'TRI']], on = 'trialId', how = 'left')
df_new.drop_duplicates(inplace = True)

df_new.to_csv('C:/Users/Tejas/OneDrive - Northeastern University/Core Model V1/PipelineSheets' + '/Oct19toMay201.csv', index = False)





df_clean = pd.read_excel('October 2019 to May 2021 Analysis OOS.xlsx', 'Cleaned Data')

df_trial = pd.read_csv('C:/Users/Tejas/OneDrive - Northeastern University/Core Model V1/LatestData/Trial_Data.csv', lineterminator = '\n')



### Trial Disease Names
a2 = df_trial['trialTherapeuticAreas'].str.strip('[]')
import ast
disease_trial = []
for i in range(0, len(a2)):
    try:
        current_dict = ast.literal_eval(a2.iloc[i])               
        
        if type(current_dict) == dict:                          
            current_disease = current_dict['trialDiseases'][0]['name']       
            disease_trial.append(current_disease)           
        else:
            cf = []
            for i1 in range(0, len(current_dict)):
                cf.append(current_dict[i1]['trialDiseases'][0]['name'])      
                       
            disease_trial.append(list(set(cf)))                  
    except:
        disease_trial.append("")         

for i in range(0,len(disease_trial)):   ### Making everything a list 
    if type(disease_trial[i]) == str:
        disease_trial[i] = list(str(disease_trial[i]).split("'"))

        

### Now create a therapeutic type column
h = df_trial['trialTherapeuticAreas']

delTher = h.apply(lambda x: str(x).replace('[', '').replace(']', '').split("'")[1::2])  ##[1::2] is to take only good words seperetly and avoid null etc

#### Always the 3rd word is the therapeuticArea in the above t sequence
### extract word at '2' always
therList = []
for i in range(0,delTher.shape[0]):
    therList.append(delTher[i][2])

df_trial['trialTherapeuticArea'] = therList

df_clean1 = df_clean.merge(df_trial[['trialId', 'trialTherapeuticArea']])

df_clean1.to_csv("Cleaned_Data.csv", index = False)





