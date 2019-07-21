"""
将爬取到的8,459个api以及其余的api的follower个数整合到新的json里面
"""
import codecs
import json
from collections import defaultdict

api_id_nfollowers_dic = defaultdict(int)
with codecs.open('../../pwspider/api_name_num_followers_mapping_8459.txt', 'r', encoding='utf-8') as reader:
    line = reader.readline()
    while line:
        api_id_nfollowers_dic[line.split(' ')[0]] = int(line.split(' ')[1])
        line = reader.readline()

with codecs.open('../../pwspider/api_name_num_followers_mapping_all.txt', 'r', encoding='utf-8') as reader:
    line = reader.readline()
    while line:
        api_id_nfollowers_dic[line.split(' ')[0]] = int(line.split(' ')[1])
        line = reader.readline()

with codecs.open('apis.json', 'r', encoding='utf-8') as reader:
    api_list_expanded = json.load(reader)

for api in api_list_expanded:
    api['n_followers'] = api_id_nfollowers_dic[api['api_id']]

with codecs.open('apis_expanded.json', 'w', encoding='utf-8') as writer:
    json.dump(api_list_expanded, writer)
