# programmableWeb_crawler
从programmableWeb上爬取各个api的follower数据


`scrapy crawl pw_followers_8459`爬取20个类共8,459个api的follower的个数

`scrapy crawl pw_followers_all`爬取全部的api的follower的个数


`apis/8459`中保存的是8,459个api的信息，这些api的description都经过了词干化，去停用词，删去一些标点符号的操作

`apis/all`保存的是所有api的信息共17,923个api，这里的api的description是原始的未经过处理的