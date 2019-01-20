import tweepy
import json
import mysql.connector
from mysql.connector import errorcode

# WRITE HERE YOUR LIST OF STRINGS TO BE SEARCHED
search_words = []

class StreamListener(tweepy.StreamListener):

    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        print('Successfully connected to Twitter API.')

    def on_error(self, status_code):
        if status_code != 200:
            print('An error has occurred')
            return False  # disconnects the stream

    def on_data(self, raw_data):
        try:
            data_json = json.loads(raw_data)

            # extracts data from the JSON
            # For more info on available attributes:
            # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html

            if 'text' in data_json:
                username = data_json['user']['screen_name']
                created_at = data_json['created_at']
                tweet = data_json['text']
                retweet_count = data_json['retweet_count']

                if data_json['place'] is not None:
                    place = data_json['place']['country']
                else:
                    place = None

                location = data_json['user']['location']

                # connects to the database and inserts the data
                connect_and_insert(username, created_at, tweet, retweet_count, place, location)

        except Exception as error:
            print('ERROR: {}'.format(error))


def connect_and_insert(username, created_at, tweet, retweet_count, place , location):
    '''Connects to MySQL and inserts the data into the table'''
    try:
        connect = mysql.connector.connect(**mysql_config)
        cursor = connect.cursor()
        print('Successfully connected to the database.')

        #SQL insert query
        query = 'INSERT INTO tweets (username, created_at, tweet, retweet_count,place, location) ' \
                'VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (username, created_at, tweet, retweet_count, place, location))
        connect.commit()

    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Invalid user or password')
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database not found')
        else:
            print('ERROR: {}'.format(error))

    finally:
        cursor.close()
        connect.close()

# Opens as dictionaries the JSON files containing MySQL access parameters and Twitter API keys
try:
    with open('api_keys.json', 'r') as file:
        api_keys = json.loads(file.read())
except FileNotFoundError:
    print('ERROR: your JSON file containing the Twitter API keys was not found.')

try:
    with open('mysql_config.json', 'r') as file:
        mysql_config = json.loads(file.read())
except FileNotFoundError:
    print('ERROR: your JSON file containing the MySQL access parameters was not found.')

# API authentication
auth = tweepy.OAuthHandler(api_keys['consumer_key'], api_keys['consumer_secret'])
auth.set_access_token(api_keys['access_token'], api_keys['access_token_secret'])

listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)

if search_words:
    print('Search terms: {}'.format(search_words))
    streamer.filter(track=search_words, languages = ['en'])
else:
    print('Your list of search terms is empty.')
