import codecs
import json
import random
import re

from scrapy.spiders import Spider


class FollowersSpider(Spider):
    """
    从programmableWeb上爬取每个api的follower信息
    """
    name = 'pw_followers'
    start_urls = ['https://www.programmableweb.com']
    download_delay = 0.2  # 设置爬取网页的间隔，避免速度过快导致被封停

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("init")
        with codecs.open("./proxyIP/https_verified.txt", 'r', encoding='utf-8') as reader:
            self.proxies = reader.readlines()
        self.crawled_api_ids = []  # 记录已经爬取的api的id
        self.target_number = 0  # 记录还需要爬取的api的数目
        self.page_counter = 0  # 记录本次启动爬虫爬取的页面的数目
        with codecs.open("api_name_num_followers_mapping.txt", 'r', encoding='utf-8') as reader:
            lines = reader.readlines()
            for line in lines:
                self.crawled_api_ids.append(line.split(" ")[0])
        self.writer = codecs.open("api_name_num_followers_mapping.txt", 'a', encoding='utf-8')
        self.api_dic = {}  # 存储原始api信息的字典，key为api_id
        with codecs.open("../8459apis/apis.json", 'r', encoding='utf-8') as reader:
            api_list_all = json.load(reader)
            for api in api_list_all:
                self.api_dic[api['api_id']] = api
        with codecs.open("../8459apis/api_info.json", 'r', encoding='utf-8') as reader:
            self.api_list_selected = json.load(reader)
        print("原数据共有", len(self.api_dic), "个api")
        print("选取其中的", len(self.api_list_selected), "个api进行爬取")
        print("已经爬取到", len(self.crawled_api_ids), "个api")
        self.target_number = len(self.api_list_selected) - len(self.crawled_api_ids)
        print("仍需爬取", self.target_number, "个api")

    def parse(self, response):
        for selected_api in self.api_list_selected:
            if str(selected_api['api_id']) not in self.crawled_api_ids:  # 说明当前api的follower信息还没被爬取过
                url = self.api_dic[str(selected_api['api_id'])]['api_pw_url']
                request = response.follow(url, callback=self.parse_one, meta={'proxy': self.get_random_proxy()})
                request.meta['api_id'] = str(selected_api['api_id'])  # 将api_id作为参数传递过去
                yield request
                # yield response.follow(url, callback=self.parse_one)

    def parse_one(self, response):
        """
        爬取到一个页面后，处理并保存数据
        :param response:
        :return:
        """
        self.page_counter += 1
        print("已爬取到第", self.page_counter, "个界面")
        print("id", response.meta['api_id'])
        span_content = response.xpath(
            '//section[@id="block-views-api-followers-row-top"]/div[@class="block-title"][1]/span[1]').extract()[0]
        follower_num = int(re.findall(re.compile(r'[(](.*?)[)]', re.S), span_content)[0])
        self.writer.write(str(response.meta['api_id']) + " " + str(follower_num) + "\n")
        self.writer.flush()

    def get_random_proxy(self):
        """
        随机获取一个可用的代理
        :return:
        """
        proxy = random.choice(self.proxies)
        return proxy
