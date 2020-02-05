import csv
import requests
import pandas as pd
from pandas import json_normalize
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

API_KEY = cfg['API_KEY']

# API key and declares final as panda dataframe
final = pd.DataFrame()

# pull source.csv into a panda dataframe
df = pd.read_csv('testzips.csv')

# opens output.csv and sets to 'f'
f = open('output.csv')
csv_file = csv.writer(f)

# loop used to iterate over
for index, row in df.iterrows():
    # API request URL that replaces %s with zipcode value from the dataframe and sets to 'r'
    r = requests.get(
        'https://api.zip-codes.com/ZipCodesAPI.svc/1.0/FindZipCodesInRadius?zipcode=%s&minimumradius=0&maximumradius=30&key=%s' % (
            row['zip'], API_KEY))

    df_normalize = r.json()

    # iterates over each item in the normalized response data
    for item in df_normalize['DataList']:
        df2 = json_normalize(item)
        final = final.append(df2)

    final.to_csv('output.csv', index=False, encoding='utf-8')
