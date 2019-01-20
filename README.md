# Streaming tweets with Python and storing data into a MySQL database 

This is a Python script to stream tweets filtered by search terms from the Twitter API and store that data into a MySQL database.

## Getting Started
- Database

First you need to setup your database. This was done using MySQL Workbench and the following commands to create a table:

```

CREATE TABLE `tweets` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(255) DEFAULT NULL,
`created_at` varchar(45) DEFAULT NULL,
`tweet` text,
`retweet_count` int(11) DEFAULT NULL,
`location` varchar(100) DEFAULT NULL,
`place` varchar(100) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci 

```

Here we are storing only the username, UTC time when tweet was created, the actual tweet text, retweet count, location and place. There are many other objects that can be obtained, as you can see [here](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html).

- Credentials

You will also need to save your MySQL connection parameters and your Twitter API keys as JSON files.
To obtain your API keys follow these [instructions](https://developer.twitter.com/en/docs/basics/apps/overview).
Having all these information in hand you can edit and run the `keys_and_configs.py` file to generate the needed JSON files.

## Streaming tweets

- Edit the `stream_tweets.py` file (line 7) and write the words or hashtags you would like to search.
- Save and run the script. Tweets should be streamed and saved into your database.
