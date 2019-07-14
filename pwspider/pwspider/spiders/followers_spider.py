from scrapy.spiders import Spider
import scrapy
import json
import codecs
import random


class FollowersSpider(Spider):
    name = 'pw_followers'
    start_urls = ['https://www.programmableweb.com']
    download_delay = 0.2  # 设置爬取网页的间隔，避免速度过快导致被封停

    # def parse(self, response):
    #     print("url", response.url)
    #     urls = response.css('a::attr(href)').re(r'^/.+?/$')
    #     for url in urls:
    #         yield response.follow(url, callback=self.parse)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("init")
        with codecs.open("./proxyIP/https_verified.txt", 'r', encoding='utf-8') as reader:
            self.proxies = reader.readlines()
        self.writer = codecs.open("api_name_num_followers_mapping.txt", 'a', encoding='utf-8')
        self.page_counter = 0

    def parse(self, response):
        # with codecs.open("../8459apis/name_list.json", 'r', encoding='utf-8') as reader:
        #     api_names_list = json.load(reader)
        # print(len(api_names_list))
        api_dic = {}
        with codecs.open("../8459apis/apis.json", 'r', encoding='utf-8') as reader:
            api_list_all = json.load(reader)
            for api in api_list_all:
                api_dic[api['api_id']] = api
        with codecs.open("../8459apis/api_info.json", 'r', encoding='utf-8') as reader:
            api_list_selected = json.load(reader)
        print("原数据共有", len(api_dic), "个api")
        print("选取其中的", len(api_list_selected), "个api")
        for selected_api in api_list_selected:
            url = api_dic[str(selected_api['api_id'])]['api_pw_url']
            yield response.follow(url, callback=self.parse_one, meta={'proxy': self.get_random_proxy()})
            # yield response.follow(url, callback=self.parse_one)

    def parse_one(self, response):
        self.page_counter += 1
        print("已爬取到第", self.page_counter, "个界面")
        print(response.xpath('//title/text()').extract())

    def get_random_proxy(self):
        """
        随机获取一个可用的代理
        :return:
        """
        proxy = random.choice(self.proxies)
        print(proxy)
        return proxy
