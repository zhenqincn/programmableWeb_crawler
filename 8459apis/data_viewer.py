import json
import codecs

with codecs.open("api_info.json", 'r', encoding='utf-8') as reader:
    data = json.load(reader)
api_name_list = [item['api_name'] for item in data]
with codecs.open("name_list.json", 'w', encoding='utf-8') as writer:
    json.dump(api_name_list, writer, ensure_ascii=False)