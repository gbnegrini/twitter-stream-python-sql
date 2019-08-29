
import tweepy
import json
import mysql.connector
from mysql.connector import errorcode

count = 0

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

                # Tweet Object
                id_tweet = data_json['id_str']
                tweet = data_json['text']
                in_reply_to_status_id = data_json['in_reply_to_status_id_str']
                in_reply_to_user_id = data_json['in_reply_to_user_id_str']
                try:
                    retweeted_from = data_json['retweeted_status']['user']['id_str']
                except:
                    retweeted_from = None
                reply_count = data_json['reply_count']
                quote_count = data_json['quote_count']
                retweet_count = data_json['retweet_count']
                favorite_count = data_json['favorite_count']
                created_at = data_json['created_at']
                location = data_json['user']['location']

                if data_json['place'] is not None:
                    place = data_json['place']['country']
                else:
                    place = None

                # User Object
                id_user = data_json['user']['id_str']
                username = data_json['user']['name']
                screen_name = data_json['user']['screen_name']

                if data_json['user']['verified']:
                    verified = 1
                else:
                    verified = 0

                followers_count = data_json['user']['followers_count']
                friends_count = data_json['user']['friends_count']
                statuses_count = data_json['user']['statuses_count']
                user_created_at = data_json['created_at']

                # connects to the database and inserts the data
                connect_and_insert(id_tweet, tweet, in_reply_to_status_id,
                                in_reply_to_user_id, retweeted_from, reply_count,
                                quote_count, retweet_count, favorite_count,
                                created_at, location, place, id_user, username,
                                screen_name, verified, followers_count, friends_count,
                                statuses_count, user_created_at)

        except Exception as error:
            print('ERROR: {}'.format(error))


def connect_and_insert(id_tweet, tweet, in_reply_to_status_id,
                        in_reply_to_user_id, retweeted_from, reply_count,
                        quote_count, retweet_count, favorite_count,
                        created_at, location, place, id_user, username,
                        screen_name, verified, followers_count, friends_count,
                        statuses_count, user_created_at):

    '''Connects to MySQL and inserts the data into the table'''

    try:
        connect = mysql.connector.connect(**mysql_config)
        cursor = connect.cursor()

        #SQL insert queries
        query_tweets = 'INSERT INTO tweets (id_tweet, tweet, in_reply_to_status_id,'\
                                'in_reply_to_user_id, retweeted_from, reply_count,' \
                                'quote_count, retweet_count, favorite_count,'\
                                'created_at, location, place) ' \
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query_tweets, (id_tweet, tweet, in_reply_to_status_id,
                                in_reply_to_user_id, retweeted_from, reply_count,
                                quote_count, retweet_count, favorite_count,
                                created_at, location, place))

        query_users = 'INSERT INTO users (id_user, username, screen_name,'\
                                'verified, followers_count, friends_count,' \
                                'statuses_count, created_at)'\
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'


        try:
            cursor.execute(query_users, (id_user, username, screen_name,
                                verified, followers_count, friends_count,
                                statuses_count, user_created_at))
        except mysql.connector.Error as error:
            if  error.errno == errorcode.ER_DUP_ENTRY:
                pass
            else:
                pass

        query_tweets_user = 'INSERT INTO tweetsbyuser (id_tweet, id_user)' \
                            'VALUES (%s, %s)'
        cursor.execute(query_tweets_user, (id_tweet, id_user))

        connect.commit()

        global count
        count = count + 1
        print('Streamed tweets: {}'.format(count), end='\r', flush=True)

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


if __name__ == '__main__':

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

    try:
        with open('search.json', 'r') as file:
            search = json.loads(file.read())
    except FileNotFoundError:
        print('ERROR: your JSON file your search parameters was not found.')

    # API authentication
    auth = tweepy.OAuthHandler(api_keys['consumer_key'], api_keys['consumer_secret'])
    auth.set_access_token(api_keys['access_token'], api_keys['access_token_secret'])

    listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    streamer = tweepy.Stream(auth=auth, listener=listener)

    print('Streaming...')

    if search['words']:
        print('Search terms: {}'.format(search['words']))
        print('Languagues: {}'.format(search['languages']))
        streamer.filter(track=search['words'], languages = search['languages'])
    else:
        print('Your list of search terms is empty.')
