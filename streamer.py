import tweepy
import time
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime, timedelta
import os
import subprocess
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

if os.name == 'nt':
	#Running the zookeeper server
	subprocess.Popen("(cd " + os.path.dirname(os.path.realpath(__file__)) + "\kafka " + "&& bin\windows\zookeeper-server-start.bat config\zookeeper.properties)", shell=True)
	time.sleep(15)
	#Running the kafka server
	subprocess.Popen("(cd " + os.path.dirname(os.path.realpath(__file__)) + "\kafka " + "&& bin\windows\kafka-server-start.bat config\server.properties)", shell=True)
	time.sleep(15)
	#Creating topic
	subprocess.Popen("(cd " + os.path.dirname(os.path.realpath(__file__)) + "\kafka " + "&& bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets-lambdal)", shell=True)
	time.sleep(15)
	#Creating consumer
	subprocess.Popen("(cd " + os.path.dirname(os.path.realpath(__file__)) + "\kafka " + "&& bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic tweets-lambdal --from-beginning)", shell=True)
	time.sleep(15)
else:
	#Running the zookeeper server
	subprocess.Popen("/kafka/bin/zookeeper-server-start.sh /kafka/config/zookeeper.properties", shell=True)
	time.sleep(15)
	#Running the kafka server
	subprocess.Popen("(cd " + os.path.dirname(os.path.realpath(__file__)) + "/kafka " + "&& bin/kafka-server-start.sh config/server.properties)", shell=True)
	time.sleep(15)
	#Creating topic
	subprocess.Popen("(cd " + os.path.dirname(os.path.realpath(__file__)) + "/kafka " + "&& bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets-lambdal)", shell=True)
	time.sleep(15)
	#Creating consumer
	subprocess.Popen("(cd " + os.path.dirname(os.path.realpath(__file__)) + "/kafka " + "&& bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic tweets-lambdal --from-beginning)", shell=True)
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

#Gets the twitter data
def get_twitter_data():
	global words_received
	global words_per_hour
	res = api.search("Donald Trump")
	for i in res:
		record = ''
		'''
		A number of data we choose not to run.
		record += str(i.user.id_str)
		record += ';'
		record += str(i.user.followers_count)
		record += ';'
		record += str(i.user.location)
		record += ';'
		record += str(i.favorite_count)
		record += ';'
		record += str(i.retweet_count)
		record += ';'
		'''
		record += str(i.user.name)
		record += '\n'
		record += str(normalize_timestamp(str(i.created_at)))
		record += '\n'
		record += str(i.text)
		words_received += len(i.text.split())
		record += '\n'
		producer.send(topic_name, str.encode(record))

#Setting up the consumer
consumer = KafkaConsumer(
	bootstrap_servers='localhost:9092',
	auto_offset_reset='latest',
	group_id='test4',
	consumer_timeout_ms=10000)
consumer.subscribe('tweets-lambdal')
#Reads twitter data every second
def periodic_work(interval):
	global words_received
	global words_per_hour
	global seconds_spent
	while True:
		get_twitter_data()
		for message in consumer:
			print(message)
		words_per_hour = words_received * 3600/seconds_spent
		seconds_spent += 1
		if seconds_spent == 3600:
			 words_received = 0
			 seconds_spent = 1
		print("------------------------" + str(words_per_hour) + "words per hour")
		producer.send(topic_name, str.encode("--------------------" + str(words_per_hour) + "words per hour"))
		time.sleep(interval)
periodic_work(1)
