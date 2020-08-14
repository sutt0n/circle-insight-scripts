import requests
import configparser
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt

cfg = configparser.ConfigParser()
cfg.read('main.cfg')

CIRCLE_TOKEN = cfg['main']['CIRCLE_TOKEN']
VCS = cfg['main']['VCS']
ORG = cfg['main']['ORG']
REPO = cfg['main']['REPO']
IGNORE_BRANCHES = ['develop']
MAX_PAGES = 20
WORKFLOW = cfg['main']['BUILD_WORKFLOW']

headers = {
    'Circle-Token': CIRCLE_TOKEN
}

offset = 0
response = requests.get(
    'https://circleci.com/api/v1.1/project/' + VCS + '/' + ORG + '/' + REPO + '?shallow=true&limit=100&offset=' + str(offset))
branchData = response.json()

for i in range(MAX_PAGES):
    offset = offset + (100 * i)
    response = requests.get(
        'https://circleci.com/api/v1.1/project/' + VCS + '/' + ORG + '/' + REPO + '?shallow=true&limit=100&offset=' + str(offset))
    paginatedData = response.json()
    branchData = branchData + paginatedData

branches = [x['branch'] for x in branchData if x['workflows']['workflow_name']
            != 'hourly' and x['lifecycle'] == 'finished']
branches = np.unique(branches)

insightData = []

# get branch insights
for branch in branches:
    response = requests.get(
        'https://circleci.com/api/v2/insights/' + VCS + '/' + ORG + '/' + REPO + '/workflows/' + WORKFLOW + '?circle-token='+CIRCLE_TOKEN+'&branch='+branch)
    branchInsightResp = response.json()
    insightData = insightData + branchInsightResp['items']

# only want successful deploys
successfulDeploys = [
    item for item in insightData if item['status'] == 'success']

# aggregated date k/v
for item in successfulDeploys:
    startedDate = datetime.datetime.strptime(
        item['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    item['date'] = startedDate.strftime('%m/%d')

# sort by date, asc order
successfulDeploys = sorted(
    successfulDeploys, key=lambda i: i['date'], reverse=True)

df = pd.DataFrame(successfulDeploys)
print(df)
df.plot(x='date', y='credits_used')
plt.gca().invert_xaxis()
plt.show()
