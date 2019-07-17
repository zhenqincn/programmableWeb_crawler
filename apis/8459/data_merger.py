"""
将8,459个api的num_followers信息合并到原来的json中，生成新的json文件
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

with codecs.open('api_info_8459.json', 'r', encoding='utf-8') as reader:
    api_list = json.load(reader)

api_list_expanded = []
for api in api_list:
    api['n_followers'] = api_id_nfollowers_dic[str(api['api_id'])]
    api_list_expanded.append(api)
with codecs.open('api_info_8459_expanded.json', 'w', encoding='utf-8') as writer:
    json.dump(api_list_expanded, writer)
