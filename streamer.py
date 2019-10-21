import tweepy
import time
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime, timedelta
import os
import appscript

#Running the zookeeper server
appscript.app('Terminal').do_script('cd ' + os.path.dirname(os.path.realpath(__file__)) + '/kafka_2.12-2.3.0 && bin/zookeeper-server-start.sh config/zookeeper.properties')
time.sleep(15)
#Running the kafka server
appscript.app('Terminal').do_script('cd ' + os.path.dirname(os.path.realpath(__file__)) + '/kafka_2.12-2.3.0 && bin/kafka-server-start.sh config/server.properties')
time.sleep(15)
#Creating topic
appscript.app('Terminal').do_script('cd ' + os.path.dirname(os.path.realpath(__file__)) + '/kafka_2.12-2.3.0 && bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets-lambdal')
time.sleep(15)
#Creating consumer
appscript.app('Terminal').do_script('cd ' + os.path.dirname(os.path.realpath(__file__)) + '/kafka_2.12-2.3.0 && bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic tweets-lambdal --from-beginning')
time.sleep(15)

#Keys for twitter API authentication
consumer_key = "eejYxthKBRYGPUXehkNiQZD03"
consumer_secret = "uWEEPyed0EFJK4FVa3aUe9beYlr6mUW12DFMociDWc6YfzQPzj"
access_token = "871016646718214145-l0s1yU6f0xOF9LP8N7nF3iW323FWKqN"
access_token_secret = "mjNu6BJQ5NFy1SZWlMHjExpwBamGtBFcCTE4UtTQOAAMP"
#Setting up authentication and API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#Global variables for counting words per hour
words_received = 0
words_per_hour = 0
seconds_spent = 1

# Working with time (normalizing timestamps)
def normalize_timestamp(time):
	mytime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	mytime += timedelta(hours = 4)
	return (mytime.strftime("%Y-%m-%d %H:%M:%S"))

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
topic_name = 'tweets-lambdal'
