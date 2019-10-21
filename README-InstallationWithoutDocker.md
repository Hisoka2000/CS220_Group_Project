# CS220_Group_Project
Ins
1.	Start Apache Kafka server:
1.1.	Start ZooKeeper server:
 bin/zookeeper-server-start.sh config/zookeeper.properties
1.2.	Start Kafka server:
bin/kafka-server-start.sh config/server.properties
1.3.	Create a topic:
	bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweetData
1.4.	Run producer and send some messages for testing purposes:
	bin/kafka-console-producer.sh --broker-list localhost:9092 --topic tweetData
1.5.	 Start a consumer:
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic tweetData --from-beginning
2.	Open new command window and run the Python program for collecting and counting tweets
3.	How python program works:
3.1.	Use tweepy API to take information from the tweeter account
3.2.	Function that takes specified data and streams it
3.3.	 Function that every second updates tweeted words count per hour
3.3.1.	At the beginning you have more averaged result and nearer to the end of each our data becomes more accurate 
