import codecs
import json
import random
import re
import os

from scrapy.spiders import Spider


class FollowersSpider(Spider):
    """
    从programmableWeb上爬取每个api的follower信息，爬取全部的
    """
    name = 'pw_followers_all'
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
        if not os.path.exists("api_name_num_followers_mapping_all.txt"):   # 如果不存在文件，则创建
            open("api_name_num_followers_mapping_all.txt", 'w')
        if os.path.exists("api_name_num_followers_mapping_8459.txt"):  # 检查8,459个api的n_followers数据是否存在
            with codecs.open("api_name_num_followers_mapping_8459.txt", 'r', encoding='utf-8') as reader:
                lines = reader.readlines()
                for line in lines:
                    self.crawled_api_ids.append(line.split(" ")[0])
        with codecs.open("api_name_num_followers_mapping_all.txt", 'r', encoding='utf-8') as reader:
            lines = reader.readlines()
            for line in lines:
                self.crawled_api_ids.append(line.split(" ")[0])
        self.writer = codecs.open("api_name_num_followers_mapping_all.txt", 'a', encoding='utf-8')
        with codecs.open("../apis/all/apis.json", 'r', encoding='utf-8') as reader:
            self.api_list = json.load(reader)

        print("原数据共有", len(self.api_list), "个api")
        print("已经爬取到", len(self.crawled_api_ids), "个api")
        self.target_number = len(self.api_list) - len(self.crawled_api_ids)
        print("仍需爬取", self.target_number, "个api")

    def parse(self, response):
        for api in self.api_list:
            if api['api_id'] not in self.crawled_api_ids:  # 说明当前api的follower信息还没被爬取过
                url = api['api_pw_url']
                request = response.follow(url, callback=self.parse_one, meta={'proxy': self.get_random_proxy()})
                request.meta['api_id'] = api['api_id']  # 将api_id作为参数传递过去
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
        contents = response.xpath(
            '//section[@id="block-views-api-followers-row-top"]/div[@class="block-title"][1]/span[1]').extract()
        if len(contents) > 0:
            span_content = contents[0]
            follower_num = int(re.findall(re.compile(r'[(](.*?)[)]', re.S), span_content)[0])
            self.writer.write(str(response.meta['api_id']) + " " + str(follower_num) + "\n")
            self.writer.flush()
        else:
            print("未找到followers信息")
            self.writer.write(str(response.meta['api_id']) + " 0\n")
            self.writer.flush()

    def get_random_proxy(self):
        """
        随机获取一个可用的代理
        :return:
        """
        proxy = random.choice(self.proxies)
        return proxy
