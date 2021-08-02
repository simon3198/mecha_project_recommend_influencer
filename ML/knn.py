import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


csv_name = './test_category'
train_data = pd.read_csv(csv_name+".csv")
train_data = pd.DataFrame(train_data)

from sklearn.neighbors import KNeighborsClassifier

indexNames = train_data[(train_data['comment num']>=290) 
                & (train_data['weekly view']<=10)].index
train_data.drop(indexNames , inplace=True)
data = train_data[['keyword score','tfidf score','josa','noun','noun/josa','paragraph num','Image num','Video num']]
# keyword score = 단어빈도수 분석에 따른 직접후기글 단어 빈도
# tfidf score = tfidf 분석에 따른 직접후기글 단어 빈도
# josa = 조사비율
# noun = 명사 비율
# noun/josa = 조사 비율 / 명사 비율
# paragraph num = 전체 글자수
train_data['comment num']=(train_data['comment num']-train_data['comment num'].min())/(train_data['comment num'].max()-train_data['comment num'].min())
train_data['sympathy num']=(train_data['sympathy num']-train_data['sympathy num'].min())/(train_data['sympathy num'].max()-train_data['sympathy num'].min())

target = (train_data['comment num']+train_data['sympathy num'])/train_data['weekly view']
# target['sum']=target['comment num']+target['sympathy num']
target = (target - target.min())/(target.max()-target.min())

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsRegressor

neigh = KNeighborsRegressor(n_neighbors=5)

# skf=StratifiedKFold(n_splits=5,shuffle=True,random_state=0)
# scores = cross_val_score(classifier , data , target.values.ravel() ,cv=skf)

# kfold = KFold(n_splits=6, shuffle = True, random_state=0)
# scores = cross_val_score(classifier , data , target ,cv=kfold)

x_train, x_valid, y_train, y_valid = train_test_split(data, target, test_size=0.2, shuffle=True, random_state=10)
for k in range(1,5,1):
    idx= 0
    for weigh in ['uniform','distance']:
        idx = idx+1
        neigh = KNeighborsRegressor(n_neighbors=k,weights=weigh)
        neigh.fit(x_train,y_train)
        plt.subplot(2,1,idx)
        y_pred = neigh.predict(x_valid)
        x_lin = np.arange(1,len(x_valid)+1,1)
        plt.plot(x_lin,y_pred,label='predict',color='navy')
        plt.plot(x_lin,y_valid,label='real',color='darkorange')
        plt.legend()
        plt.title(f'KNNRegressor k={k} weigh={weigh}')
        print(neigh.score(x_valid,y_valid))
    plt.show()