import snscrape.modules.twitter as sntwitter
import psycopg2 as db
import pandas as pd

hostname = "localhost"
database = "tweets"
user = "postgres"
password = "12345"
port = 5432

keywords = ["python lang:en", "Java lang:en", "Micheal Jordan lang:en ", "erbatur lang:tr"]
tweets = []
limit = 10
c = 0
for keyword in keywords:
    for tweet in sntwitter.TwitterSearchScraper(keyword).get_items():
        # print(c)
        # print(tweet.user.username)
        c = c + 1
        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.date, tweet.user.username, tweet.content])
            try:
                conn = db.connect(
                    host=hostname,
                    database=database,
                    user=user,
                    password=password,
                    port=port)
                curr = conn.cursor()
                insert_script = 'insert into tweets_users(created_date,name,content) values(%s,%s,%s)'
                insert_value = (tweet.date, tweet.user.username, tweet.content)
                curr.execute(insert_script, insert_value)
                conn.commit()
            except (Exception, db.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
