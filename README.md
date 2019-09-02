# Streaming tweets with Python and storing data into a MySQL database

This is a Python script to stream tweets with [Tweepy](https://tweepy.readthedocs.io/en/latest/) and store some Tweet and User attributes into a MySQL database.

## Prerequisites
### Database

First you need to se tup your database. You can easily install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) and then run the SQL script file (```twitter_ddl.sql```) to create all tables.

### Credentials

To obtain your Twitter API keys follow these [instructions](https://developer.twitter.com/en/docs/basics/apps/overview).

### Dependencies
 - tweepy
 - json
 - mysql-connector-python
 
 You can use the following command to create a conda environment (twitter-sql) and install all dependencies:
 ```bash
 $ conda env create -f environment.yaml
 $ conda activate twitter-sql
 ```
 
 ## How to use
 ### Streaming and storing
Use your favorite text editor to open and edit the ```keys_and_configs.py``` file. You need to write your own Twitter API credentials and MySQL access parameters in this file. There you will also need to write your search parameters like search terms and language.
Once you have edited this file you must run it to generate the files that ```stream_tweets.py``` will need.
```bash
$ python keys_and_configs.py
```

With all configurations set you can finally run ```stream_tweets.py``` to start streaming and storing the tweets:
```bash
$ python stream_tweets.py
```
