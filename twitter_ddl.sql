CREATE SCHEMA twitter;
USE twitter;

CREATE TABLE tweets (
id_tweet VARCHAR(50) NOT NULL,
tweet TEXT,
in_reply_to_status_id VARCHAR(50) DEFAULT NULL,
in_reply_to_user_id VARCHAR(50) DEFAULT NULL,
retweeted_from VARCHAR(50) DEFAULT NULL,
reply_count INT(11) DEFAULT NULL,
quote_count INT(11) DEFAULT NULL,
retweet_count INT(11) DEFAULT NULL,
favorite_count INT(11) DEFAULT NULL,
created_at VARCHAR(50) DEFAULT NULL,
location VARCHAR(100) DEFAULT NULL,
place VARCHAR(100) DEFAULT NULL,
PRIMARY KEY (id_tweet)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE users (
id_user VARCHAR(50) NOT NULL,
username VARCHAR(255) DEFAULT NULL,
screen_name VARCHAR(50) DEFAULT NULL,
verified BIT(1) DEFAULT NULL,
followers_count INT(11) DEFAULT NULL,
friends_count INT(11) DEFAULT NULL,
statuses_count INT(11) DEFAULT NULL,
created_at VARCHAR(50) DEFAULT NULL,
PRIMARY KEY (id_user)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE tweetsbyuser (
id_tweet VARCHAR(50) NOT NULL,
id_user VARCHAR(50) NOT NULL,
PRIMARY KEY (id_tweet, id_user),
FOREIGN KEY (id_tweet) REFERENCES tweets(id_tweet),
FOREIGN KEY (id_user) REFERENCES users(id_user)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
