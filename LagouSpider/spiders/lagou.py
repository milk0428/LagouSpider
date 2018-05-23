# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ["https://www.lagou.com/"]

    rules = (
        Rule(LinkExtractor(allow='zhaopin/.*'),follow=True),
        Rule(LinkExtractor(allow='gongsi/j\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    # #手动重载该函数，相当于之前的parse()
    # def parse_start_url(self, response):
    #     return []
    #
    # #手动重载该函数，该函数是处理parse_start_url()函数的结果，默认是直接返回parse_start_url()函数的结果。调用该函数的逻辑详见CrawlSpider类的_parse_response（）函数
    # def process_results(self, response, results):
    #     return results

    #该函数名称在rules中设置
    def parse_job(self, response):
        #解析拉勾网的职位
        #不能重载parse()函数
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def start_requests(self):
        #注意传入headers
        # return [scrapy.Request("https://www.zhihu.com/#signin",callback=self.login,headers=self.header)]
        username=input("请输入知乎用户名：")
        password=input("请输入知乎密码：")
        browser=webdriver.Firefox(executable_path="D:/PycharmProjects/ZhihuSpider/geckodriver.exe")
        browser.get("https://www.zhihu.com/signin?next=%2F")

        browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(username)
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(password)

        #暂停10秒以输入验证码
        time.sleep(10)

        browser.find_element_by_css_selector(".SignFlow .SignFlow-submitButton").click()
        #等待5秒以使得页面读取完毕
        time.sleep(15)
        cookies=browser.get_cookies()
        # print(cookies)
        cookie_dict={}
        for cookie in cookies:
            f = open('D:/PycharmProjects/ZhihuSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            #只获取cookie的name/value字段的值并装进字典，将该字典赋值给scrapy的cookies以维持登陆状态。注意该原来的字典中有很多字段。
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        #注意dont_filter参数以及setting.py中设置ROBOTSTXT_OBEY = False
        # 没有写回调函数的话默认调用prase（）
        #注意要传入参数headers
        # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict,headers=self.header)]
        for url in self.start_urls:
            # 不写回调函数即提交至parse()
            yield scrapy.Request(url, dont_filter=True, cookies=cookie_dict,headers=self.header)