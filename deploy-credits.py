import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import datetime
import configparser

cfg = configparser.ConfigParser()
cfg.read('main.cfg')

CIRCLE_TOKEN = cfg['main']['CIRCLE_TOKEN']
VCS = cfg['main']['VCS']
ORG = cfg['main']['ORG']
REPO = cfg['main']['REPO']
VCS_SLUG = VCS + '/' + ORG + '/' + REPO
MAX_PAGES = 8
WORKFLOW = cfg['main']['DEPLOY_WORKFLOW']

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Circle-Token': CIRCLE_TOKEN
}

response = requests.get('https://circleci.com/api/v2/insights/' +
                        VCS_SLUG + '/workflows/' + WORKFLOW, headers=headers)
jsonData = response.json()
nextPageToken = str(jsonData['next_page_token'])

for page in range(MAX_PAGES):
    if nextPageToken is not None:
        response = requests.get('https://circleci.com/api/v2/insights/' + VCS_SLUG +
                                '/workflows/' + WORKFLOW + '?page-token=' + nextPageToken, headers=headers)
        newJsonData = response.json()
        jsonData['items'] = jsonData['items'] + newJsonData['items']
        nextPageToken = newJsonData['next_page_token']

successfulDeploys = [item for item in jsonData['items']
                     if item['status'] == "success"]

for item in successfulDeploys:
    startedDate = datetime.datetime.strptime(
        item['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    item['date'] = startedDate.strftime('%m/%d')

# dump json into file
# with open('data.json', 'w') as data_file:
#     data = json.dump(jsonData, data_file)

df = pd.DataFrame(successfulDeploys)
print(df)
df.plot(x='date', y='credits_used')
plt.gca().invert_xaxis()
plt.show()
