import json

# Write here your Twitter API keys
# More info: https://developer.twitter.com/en/docs/basics/apps/overview
api_keys = {
    'consumer_key': 'API KEY',
    'consumer_secret': 'API SECRET KEY',
    'access_token': 'ACCESS TOKEN',
    'access_token_secret': 'ACCESS TOKEN SECRET'
}

# Write here your MySQL access parameters
my_sql_config = {
    'user': 'YOUR USER',
    'password': 'YOUR PASSWORD',
    'host': 'YOUR HOST',
    'database': 'YOUR DATABASE'
}

json_keys = json.dumps(api_keys)
file = open("api_keys.json", "w")
file.write(json_keys)

json_config = json.dumps(my_sql_config)
file = open("mysql_config.json", "w")
file.write(json_config)

file.close()

