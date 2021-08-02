import pandas as pd
import os
import numpy as np 
base_df = pd.read_csv('./crawler/보석십자수2021-07-07.csv')

file_list  = os.listdir('./survey')    
print(file_list)
df_list=[]
for file in file_list:
    df = pd.read_csv('./survey/'+file)
    links = np.array(df.columns[3:-1],dtype='str')
    
    response_df = df.loc[:,links[0]:links[-1]]
    print(links)
    response_df = response_df.mask(response_df=='아니오',0)
    response_df = response_df.mask(response_df=='네',1)

    response_df = response_df.apply(lambda x:x.sum(),axis=0)
    max_score = len(df)
    column_len = len(response_df)
    data = {'Post URL':response_df.keys().values,'response score':response_df.values,'Max score':[max_score]*column_len}

    response_df = pd.DataFrame(data=data,columns=['Post URL','response score','Max score'],index=None)
    merge_df = pd.merge(response_df,base_df)

    df_list.append(merge_df)

save_df = df_list[0]
save_df = save_df.append(df_list[1:])
save_df.drop('Unnamed: 0',axis=1,inplace=True)
save_df.to_csv('savebosuks.csv')
