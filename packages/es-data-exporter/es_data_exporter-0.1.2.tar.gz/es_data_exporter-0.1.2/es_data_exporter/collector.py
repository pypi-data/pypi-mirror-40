import json
import requests
from requests_kerberos import HTTPKerberosAuth
import time
from pandas.io.json import json_normalize
from datetime import datetime


def search_es(config, kerberos, tls):
    pro_rows = '\n'
    host = config['es_host']
    try:
        a = None
        if kerberos:
            a = HTTPKerberosAuth()
        s = ''
        if tls:
            s = 's'
        r = requests.post("http{}://{}/{}/_search".format(s, host, config['es_index']),
                          headers={"Content-Type": "application/json"},
                          data=json.dumps(config['es_query']),
                          auth=a,
                          )
    except:
        raise Exception('Cannot connect to Elasticsearch host: {}\n{}'.format(
            host, "http{}://{}/{}/_search".format(s, host, config['es_index'])))
    if r.status_code == 200:
        es_data = r.json()['hits']['hits']
        es_list = []
        for x in es_data:
            es_list.append(x.get('_source'))
        df = json_normalize(es_list)
        for _, r in df.iterrows():
            df_keys = r.keys()
            stats_tags = ''
            for t in config['prometheus_tags']:
                try:
                    stats_tags += ',{}:"{}"'.format(t.replace('.', '_'), r[t])
                except KeyError:
                    pass
            stats_tags = '{' + stats_tags[1:] + '}'

            timestamp = int(datetime.strptime(
                r[config['timestamp_tag']], '%Y-%m-%dT%H:%M:%S.%f%z').timestamp() * 1000)
            for k in df_keys:
                if isinstance(r[k], int) or isinstance(r[k], float):

                    pro_row = '{}{} {} {}\n'.format(
                        k.replace('.', '_'), stats_tags, r[k], timestamp)
                    pro_rows = pro_rows + pro_row
                else:
                    pass
    else:
        raise Exception('Query failed: {}'.format(r.json()))

    return pro_rows.encode()
