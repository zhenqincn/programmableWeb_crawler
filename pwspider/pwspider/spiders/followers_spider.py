from scrapy.spiders import Spider
import scrapy
import json
import codecs


class FollowersSpider(Spider):
    name = 'pw_followers'
    start_urls = ['https://www.programmableweb.com']
    page_counter = 0
    download_delay = 5  # 设置爬取网页的间隔，避免速度过快导致被封停

    # def parse(self, response):
    #     print("url", response.url)
    #     urls = response.css('a::attr(href)').re(r'^/.+?/$')
    #     for url in urls:
    #         yield response.follow(url, callback=self.parse)

    def parse(self, response):
        with codecs.open("../8459apis/name_list.json", 'r', encoding='utf-8') as reader:
            api_names_list = json.load(reader)
        print(len(api_names_list))
        for api_name in api_names_list:
            url = "https://www.programmableweb.com/api/" + api_name.lower().replace(" ", "-")
            print(url)
            yield response.follow(url, callback=self.parse_one)

    def parse_one(self, response):
        pass
