import pandas as pd
import numpy as np

file_name = './보석십자수2021-07-07.csv'
df = pd.read_csv(file_name)

isNOAD = df['AD'].isnull()

noAD_df = df[isNOAD]
save_noAD_df = noAD_df.sample(frac=1)

isAD = ~isNOAD


save_AD_df = df[isAD].sample(frac=1)

with open('bosuksipzasu50.txt','w') as f:
    for idx in range(1,51):
        if idx<41:
            blog_url = save_noAD_df['Post URL'].iloc[idx]
            f.write("NO AD : " + blog_url+'\n')
        else:
            blog_url = save_AD_df['Post URL'].iloc[idx]
            f.write("AD : " + blog_url+'\n')

