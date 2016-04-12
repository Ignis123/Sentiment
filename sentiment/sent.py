import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import mysql.connector
import sentiment_module as sent_mod
from datetime import date, timedelta
from datetime import datetime
import time
#from apscheduler.schedulers.background import BackgroundScheduler


cKey = 'i0D8S1VRfHXu3VBvhtm1XXN70'
cSecret = 'omTTF24aiNHxwMv5OZOp7yrFgooW8PJofnGuMzBpWNNn7fqe17'
aToken = '4091093909-oZpHDo9Dt2Ax9K4rfCeF1Bi9EXpl0AlmV7ooW5Q'
aSecret = 'ibgEeG5NMJJ7yCqQv1jNaCtQgBRbp3H2F9tpio0jMFIeS'

conn = mysql.connector.connect(host='127.0.0.1', user='tweetuser', password='tweetpasswd', database='tweets', charset='utf8mb4')
myCur = conn.cursor()


# def wait_for_tomorrow():
#     """Wait to tomorrow 00:00 am"""
#     tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1),
#                                          hour=0,
#                                          minute=0,
#                                          second=0)
#     delta = tomorrow - datetime.datetime.now()
#     time.sleep(delta.seconds(600))#set up the number of minutes (10min)

# def wait_to_next_midnight():
#     """Wait to tomorrow 00:00 am."""
#     t = time.localtime()
#     t = time.mktime(t[:3] + (0, 0, 0) + t[6:])
#     time.sleep(t + 24*3600 - time.time())


def old_tweets():
    myCur.execute("SELECT my_date FROM tweets")
    data = myCur.fetchall()
    yesterday = date.today() - timedelta(1)
    print(yesterday)

    for row in data:
        if row[0] == yesterday:
            this_date = row[0]
            myCur.execute("DELETE FROM tweets WHERE my_date = '%s'" % (this_date,))
    conn.commit()


class MyStreamListener(StreamListener):
    old_tweets()
    def on_data(self, data):
        #while self.tweet_count < self.max_tweet_count:
        jsonData = json.loads(data)
        #if not jsonData['retweeted'] and 'RT @' not in jsonData['text']:
        today = date.today()

        try:
            if 'text' in jsonData:
                tweet = jsonData["text"]
                sentiment_value, confidence = sent_mod.sentiment(tweet)

                myCur.execute("INSERT INTO tweets (my_date, tweet, sentiment, confidence) Values (%s, %s, %s, %s)", #VALUES ({0}, '{1}', '{2}', {3})".format(time.time(), tweet, sentiment_value, confidence))
                      (today, tweet, sentiment_value, confidence))
                print("IT IS WORKING!!!")

                conn.commit()

                return True
            else:
                return True
        except Exception:
            pass
        #.encode('ascii', 'ignore')
            #self.tweet_count +=1
        #print("Ending: count: " + str(self.tweet_count))

    def on_status(self, status):
        print(status)


auth = OAuthHandler(cKey, cSecret)
auth.set_access_token(aToken, aSecret)

api = tweepy.API(auth)
#api.update_status('tweepy + oauth')

#query = input('Provide a topic to search Twitter on: ')

#myStreamListener = MyStreamListener()

myStream = Stream(auth, MyStreamListener(api))
#myStream.filter(track=[query], async=True)
myStream.filter(locations=[-10.5, 51.5, -5.5, 55.5], languages=["en"], stall_warnings=True)#locations limited to ireland only
print("Starting")

# if __name__ == "__main__":
#     run_this()