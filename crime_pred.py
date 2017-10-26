# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import itertools
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import chainer
import chainer.links as L
from chainer import training
from chainer.training import extensions
from chainer.datasets import TupleDataset
import crime_model

def get_data():
    #エクセルファイルを読み込み
    file="crime_data.xlsx"
    sheetName="Sheet2"
    cell=pd.read_excel(file, sheetname=sheetName)
    cell.columns=['time', 'tweets', 'stock price', 'weather', 'temparature','police']
    #欠測値を補完する
    #axis=0 で列の平均値を計算する
    #mean は平均値補完を意味する
    imr=Imputer(missing_values='NaN', strategy='mean', axis=0)
    #データを適合
    imr=imr.fit(cell)
    #補完を実行
    imputed_data=imr.transform(cell.values)

    #トレーニングデータとテストデータに分ける
    X, y=imputed_data[:, :5], imputed_data[:, 5]
    X_train, X_test, y_train, y_test=train_test_split(X,y, test_size=0.3, random_state=0)

    #標準化(標準化のインスタンスを生成。平均＝０、標準偏差＝１)
    stdsc=StandardScaler()
    X_train_std=stdsc.fit_transform(X_train[:, :5])
    X_test_std=stdsc.fit_transform(X_test[:, :5])
    return X_train_std, X_test_std, y_train, y_test


def train(batchsize=100, epoch=5, gpu=1, out_dir='result', resume='', in_unit=5, unit=50):
    #定義したモデルを使うことを宣言
    model=L.Classifier(crime_model.Model(in_unit, unit, 24))

    #print("これから学習を始めます")

    #GPUで計算させる
    if gpu>=0:
        chainer.cuda.get_device(gpu).use()
        model.to_gpu()

    #最適化関数を指定
    #アダム：初期値による誤差が少ない、高性能
    optimizer=chainer.optimizers.Adam()
    optimizer.setup(model)

    #データを取得
    X_train, X_test, y_train, y_test=get_data()

    #データセットの形式をchainer用にする
    train=TupleDataset(np.array(X_train, dtype=np.float32), np.array(y_train, dtype=np.float32))
    test=TupleDataset(np.array(X_test, dtype=np.float32), np.array(y_test, dtype=np.float32))

    #イテレータ＝要素を反復して取り出すことのできるインターフェイス
    train_iter=chainer.iterators.SerialIterator(train, batchsize)
    test_iter=chainer.iterators.SerialIterator(test, batchsize, repeat=False, shuffle=False)

    #学習を割り当てる
    updater=training.StandardUpdater(train_iter, optimizer, device=gpu)
    #学習回数（epoch）を指定する
    trainer=training.Trainer(updater, (epoch, 'epoch'), out=out_dir)

    #精度確認
    trainer.extend(extensions.Evaluator(test_iter, model, device=gpu))
    #グラフを描画する
    trainer.extend(extensions.dump_graph('main/loss'))
    #trainerの途中経過をログファイルに蓄積する
    trainer.extend(extensions.LogReport())
    #logReportの中身を出力する
    #main/loss=答えとの差の大きさ、main/accuracy=正解率
    trainer.extend(ensions.PrintReport('epoch', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy'))


    #学習してきた結果を呼び戻す？
    if resume:
        chainer.serializers.load_npz(resume, trainer)
    

    trainer.run()

    return model



if __name__=='__main__':
    #プログラム内で使う引数を定義？
    #perserはpythonでコマンドを実行するときにパラメーターを設定しやすくしてくれる便利なやつ
    #add_argument('後で呼ぶための名前','-ターミナルでの指定方法','数字ならtype=int’,指定なかったら場合のdefault値)
    parser=argparse.ArgumentParser(description='Chainer example: MNIST')
    parser.add_argument('--batchsize', '-b', type=int, default=100, help='Number of images in each mini batch')
    parser.add_argument('--epoch', '-e', type=int, default=1000, help='Number of sweeps over the dataset to train')
    parser.add_argument('--gpu', '-g', type=int, default=1, help='GPU ID(negative value indicates CPU)')
    parser.add_argument('--out_dir', '-o', default='result', help='Directory to output the result')
    parser.add_argument('--resume', '-r',default='', help='Resume the training from snapshot')
    parser.add_argument('--in_unit', '-i', type=int, default=6, help='Number of units in inputlayer')
    parser.add_argument('--unit', '-u', type=int, default=50, help='Number of units in hidden1 layer')
    args=parser.parse_args()

    train(batchsize=args.batchsize, epoch=args.epoch, gpu=args.gpu, out_dir=args.out_dir, resume=args.resume, in_unit=args.in_unit, unit=args.unit)
