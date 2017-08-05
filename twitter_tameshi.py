#ライブラリ
import tweepy
import os
import time
import datetime

count=0
today1=datetime.date.today()  #datetimeをdtime1に取得する


#取得キー
CONSUMER_KEY='65OzS4TIhdjwxx9zDQFSUcls8'
CONSUMER_SECRET='WTISvUkBWum1AT5oBUdeq8voGWF2vvr9aymIFt3U7OpyYRfhtw'
ACCESS_TOKEN='867582419880165377-dGNug1G0kIqdZcKy8RAeTAjDBvAIAYQ'
ACCESS_SECRET='88YVCdg5lG5yARlLMRfnYGRNYDxy0BtPAFBt8sLEQkHxd'

auth=tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#エラーの受け渡し
#class myException(Exception): pass

#Streaming APIで取得したツイートを処理するためのクラス
class MyStreamListener(tweepy.StreamListener):

    #ツイートを受信したときに呼び出されるメソッド
    #引数はツイートを表すstatusオブジェクト
    def on_status(self, status):
        today2=datetime.date.today()  #datetimeをdtime2に取得する
        tweet="{time},{tweet}".format(time=status.created_at, tweet=status.text)
        print(status.created_at,'@' + status.user.screen_name, status.text)
        f=open('twitter_tameshi.text', 'a')
        f.write(tweet)
        f.write('\n')
        global count
        count+=1     #カウント増やす
        print(count)
        f.close()

        global today1
        todaydef=today2-today1
        if todaydef.days>=1:

            #日数差が１以上だったら更新する（カウントを０に戻す）
            f=open('day.csv', 'a')
            f.write(str(count))
            f.write(',')
            f.write(str(today2))
            f.write('\n')
            count=0
            today1=today2
            f.close()


    def on_error(self, status_code):
        if status_code==420:
            return False

#twitterからpythonにメッセージを受信したときに、cp932でエラーがおこる
#認証情報をStreamListenerを指定してStreamオブジェクトを取得する
while True:
    try:
         stream=tweepy.Stream(auth, MyStreamListener())
         #フィルターをしたものを返す
         #＃＃＃＃＃＃まだ位置情報はいれていません＃＃＃＃＃＃＃
         stream.filter(track=["犯罪","不審者","戸締り","つきまとわれる","防犯","わいせつ","公然わいせつ",
         "ちかん","痴漢","危険","声かけ","追いかけられる","脅迫","暴行",
         "声をかけられる","凶悪","事件","詐欺","オレオレ","警察","ひったくり","侵入","万引き",
         "空き巣","犯人","泥棒","放浪","違反","違反","逃走","犯","嫌","嫌だ","いや","難しい","じゃまくさい","邪魔","忙し",
         "出来ない","こまった","疲れた","つかれた","こまる","つら","ムカつく","やば","許さない","くるし",
         "つらい","むかつく","だるい","やばい","ゆるせない","苦し","つまらない","不幸",
         "ついてない","死ぬ","しぬ","うざ","積んだ","つんだ","行きたくない"])


    except UnicodeEncodeError:
         print("unicode")
         print("\n")
         count+=1     #カウント増やす
         print(count)
         today2=datetime.date.today()  #datetimeをdtime2に取得する
         todaydef=today2-today1
         if todaydef.days>=1:
             #日数差が１以上だったら更新する（カウントを０に戻す）
             f=open('day.csv', 'a')
             f.write(str(count))
             f.write(',')
             f.write(str(today2))
             f.write('\n')
             count=0
             today1=today2
             f.close()


    except Exception:
        #ツイートを得られなかった場合、１０秒待機して再度取得を行う
        time.sleep(5)
        stream=tweepy.Stream(auth, MyStreamListener())
        stream.filter(track=["犯罪","不審者","戸締り","つきまとわれる","防犯","わいせつ","公然わいせつ",
        "ちかん","痴漢","危険","声かけ","追いかけられる","脅迫","暴行",
        "声をかけられる","凶悪","事件","詐欺","オレオレ","警察","ひったくり","侵入","万引き",
        "空き巣","犯人","泥棒","放浪","違反","違反","逃走","犯","かけられ"])
