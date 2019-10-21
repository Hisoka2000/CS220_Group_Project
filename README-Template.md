# Twitter Streamer

This is our Python project for the CS_220 HPC midterm at the American University of Armenia. The peoject gets some data from Twitter and loads it into Apache Kafka

## Getting Started

To get the project up and running on your system, firstly download everything as a zip file from GitHub and unzip it somewhere on your machine.
### Prerequisites

Make sure to have Docker installed on your machine.


### Installing

In the downloaded folder, unzip kafka_2.12-2.3.0 inside the same directory. Now load the twitter_streamer image, provided by the google drive link, by running

```
docker load < twitter.streamer.tar				(>)
```
Then run the image by

```
docker run twitter.streamer
```


## Built With

* [Kafka](https://kafka.apache.org/documentation/)
* [Docker](https://docs.docker.com/) - Dependency Management

## Authors

* **Ofelya Mikayelyan** 
* **Ruben Shahnazaryan** 
* **Ruben Movsisyan** 
* **Narek Azaryan** 
* **Davit Haroyan** 
* **Thomas Petrossian** 




