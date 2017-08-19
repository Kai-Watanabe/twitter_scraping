#ライブラリ
import tweepy
import os
import time
import datetime
from datetime import datetime, timedelta



#取得キー
CONSUMER_KEY='65OzS4TIhdjwxx9zDQFSUcls8'
CONSUMER_SECRET='WTISvUkBWum1AT5oBUdeq8voGWF2vvr9aymIFt3U7OpyYRfhtw'
ACCESS_TOKEN='867582419880165377-dGNug1G0kIqdZcKy8RAeTAjDBvAIAYQ'
ACCESS_SECRET='88YVCdg5lG5yARlLMRfnYGRNYDxy0BtPAFBt8sLEQkHxd'

auth=tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


#class myException(Exception): pass
#Streaming APIで取得したツイートを処理するためのクラス
class MyStreamListener(tweepy.StreamListener):
    #ツイートを受信したときに呼び出されるメソッド
    #引数はツイートを表すstatusオブジェクト
    #on_dataメソッドからon_statusメソッドへデータを渡される
    def on_status(self, status):
        today=datetime.now()
        print(today)
        todaystr=today.strftime('%m%d')
        tweet=status.text
        print(tweet)
        f=open('twitter_nega.text', 'a')
        f.write(todaystr)
        f.write(tweet)
        f.write('\n')
        f.close()


    #エラーを処理すすメソッド
    def on_error(self, status_code):
        if status_code==420:
            return False


#認証情報をStreamListenerを指定してStreamオブジェクトを取得する
while True:
    try:
         stream=tweepy.Stream(auth, MyStreamListener())
         #stream.filter(locations=[136.04,20.25,148.45,24.16])
         #行きたくない
         stream.filter(track=["嫌","嫌だ","いや","難しい","じゃまくさい","邪魔","忙し",
         "出来ない","こまった","疲れた","つかれた","こまる","つら","ムカつく","やば","許さない","くるし",
         "つらい","むかつく","だるい","やばい","ゆるせない","苦し","つまらない","不幸",
         "ついてない","死ぬ","しぬ","うざ","積んだ","つんだ","行きたくない"])
    except UnicodeEncodeError:
         print("unicode")
         today=datetime.now()
         print(today)
         todaystr=today.strftime('%m%d')
         f=open('twitter_tameshi.text', 'a')
         f.write(todaystr)
         f.write("unicode")
         f.close()


        #ツイートを得られなかった場合、１０秒待機して再度取得を行
    except Exception:
        time.sleep(10)
        stream=tweepy.Stream(auth, MyStreamListener())
        #stream.filter(locations=[136.04,20.25,148.45,24.16])
        stream.filter(track=["嫌","嫌だ","いや","難しい","じゃまくさい","邪魔","忙し",
        "出来ない","こまった","疲れた","つかれた","こまる","つら","ムカつく","やば","許さない","くるし",
        "つらい","むかつく","だるい","やばい","ゆるせない","苦し","つまらない","不幸",
        "ついてない","死ぬ","しぬ","うざ","積んだ","つんだ","行きたくない"])
#品詞を変えてみる
#公開しているツイートをサンプリングしたストリームを受信する
#キーワード引数languagesで、日本語のツイートのみに絞り出す
#南端の経度、西端の緯度、北端の経度、東端の緯度
