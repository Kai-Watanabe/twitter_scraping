import numpy as np
from sklearn import tree
from sklearn.ensemble import RndamForestClassifier


res_ok=0
res_ng=0


#学習データ作成

train_data=[]
train_result=[]

f=open('')

tmp_data=[]
prev_data=0.0
cur_data=0.0


for item in reader:
    cur_data=float(item[0])

    #過去のn日分データを基に学習データを作成
    if n<=len(tmp_data):
        #ｎ日分のデータ
        train_data.append(tmp_data[:])

        #上がったか下がったかのデータ
        if prev_data<bur_data:
            train_result.append(1)
        else:
            train_result.append(0)


        tmp_data.pop(0)


    #データの更新
    timp_data.append(cur_data)
    prev_data=cur_data




＃学習

clf=tree.DecisionTreeClassfier()
clf.fit(train_data, train_result)


#予測
f=open('')
