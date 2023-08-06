# -*- coding: utf-8 -*-
import requests
import pandas
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO
import csv

URL="http://api.pltshow.com"
def df2array(df):
    buf = StringIO(df.to_csv())
    reader = csv.reader(buf, delimiter=',')
    return [row for row in reader]

class Client:
    def __init__(self, username = None, password = None):
        pass

    def show(self, df, title = 'chart', dfName = None):
        chart = requests.get('%s/api/charts' % URL, params={'title': title}).json()
        usePut = True
        if not chart:
            usePut = False
            chart = {
                    'title': title,
                    'dataset': []
                    }

        modified = False
        if not dfName:
            dfName = 'df'
        ds = {
                'id': dfName,
                'source': df2array(df),
                "sourceHeader": True
                }
        dsLen = len(chart.get('dataset', []))
        if dsLen == 0:
            chart['dataset'] = [ds]
            modified = True
        else:
            for i in range(dsLen):
                if chart['dataset'][i]['id'] == dfName:
                    chart['dataset'][i] = ds
                    modified = True
                    break
        if modified:
            headers = {'Content-Type': 'application/json'}
            if usePut:
                requests.put('%s/api/charts/%s' % (URL, chart['id']), json=chart, headers = headers)
            else:
                requests.post('%s/api/charts' % URL, json=chart, headers = headers)
