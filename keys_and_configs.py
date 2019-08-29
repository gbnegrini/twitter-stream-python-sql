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

# Write here your search parameters as a list
    # English: 'en'
    # Portuguese: 'pt'
search = {
    'words': ['YOUR', 'SEARCH', 'TERMS'],
    'languages': ['WHICH', 'LANGUAGES']
}

if __name__ == '__main__':
    try:
        json_keys = json.dumps(api_keys)
        with open("api_keys.json", "w") as file:
            file.write(json_keys)

        json_config = json.dumps(my_sql_config)
        with open("mysql_config.json", "w") as file:
            file.write(json_config)

        json_search = json.dumps(search)
        with open("search.json", "w") as file:
            file.write(json_search)

        print('Keys and configs written!')
    except:
        print('Oops, something went wrong!')
