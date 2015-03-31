from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import scrapy
from scrapy.http import FormRequest
from scrapy import log
from scrapy.exceptions import DropItem

class ExampleSpider(CrawlSpider):
    name = 'app2'
    start_urls = ['https://app2.com/login/index.php']

    # 'log' and 'pwd' are names of the username and password fields
    # depends on each website, you'll have to change those fields properly
    # one may use loginform lib https://github.com/scrapy/loginform to make it easier
    # when handling multiple credentials from multiple sites.
    def parse(self, response):
        return FormRequest.from_response(
            response,
            formdata={'username': 'admin', 'password': 'AdminAdmin1!'},
            callback=self.parse_page
        )

    # def after_login(self, response):
    #     # check login succeed before going on
    #     if "Invalid login" in response.body:
    #         self.log("Login failed", level=log.ERROR)
    #         return
    #
    #     # continue scraping with authenticated session...
    #     else:
    #         self.log("Login succeed!", level=log.DEBUG)
    #         return Request(url="https://app2.com/",
    #                        callback=self.parse_page)

    # example of crawling all other urls in the site with the same
    # authenticated session.
    def parse_page(self, response):
        """ Scrape useful stuff from page, and spawn new requests
        """
        hxs = HtmlXPathSelector(response)
        # i = CrawlerItem()
        # find all the link in the <a href> tag
        links = hxs.select('//a/@href').extract()
        links.append(hxs.select('//form/@action').extract())
        # actionLinks = hxs.select('//form/@action').extract()
        # for actionLink in actionLinks:
        #     if "https://app2.com" in actionLink and "https://app2.com/calendar/" not in actionLink:
        #         print "actionLink:::"+actionLink
        #         with open("page.txt", 'a') as f:
        #             f.write( "actionLink:::"+actionLink+"\n")

        # Yield a new request for each link we found
        # #this may lead to infinite crawling...
        for link in links:
            print link
            #only process external/full link
            if "https://app2.com" in link and "https://app2.com/calendar/" not in link:
                with open("page.txt", 'a') as f:
                    f.write(link+"\n")
                yield Request(url=link, callback=self.parse_page)

        # item = LinkItem()
        # item["title"] = hxs.select('//title/text()').extract()[0]
        # item["url"] = response.url
        # yield self.collect_item(item)

    def collect_item(self, item):
        return item


class AppSpider(CrawlSpider):
    name = 'app2-check'
    start_urls = ['https://app2.com/login/index.php']

    # 'log' and 'pwd' are names of the username and password fields
    # depends on each website, you'll have to change those fields properly
    # one may use loginform lib https://github.com/scrapy/loginform to make it easier
    # when handling multiple credentials from multiple sites.
    def parse(self, response):
        print "here"
        return FormRequest.from_response(
            response,
            formdata={'username': 'admin', 'password': 'AdminAdmin1!'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "Invalid login" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        # continue scraping with authenticated session...
        else:
            self.log("Login succeed!", level=log.DEBUG)
            return Request(url="https://app2.com/mod/wiki/filesedit.php?subwiki=1&pageid=1",
                           callback=self.parse_page)

    # example of crawling all other urls in the site with the same
    # authenticated session.
    def parse_page(self, response):
        """ Scrape useful stuff from page, and spawn new requests
        """
        with open("body.txt", 'w') as f:
            f.write(response.body)


######################################################################################################################
# __author__ = 'Vignesh Prakasam'
#
# import scrapy
# import os
#
# from selenium import webdriver
#
# #Following are optional required
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
#
# # from scrapIt.items import ScrapitItem
# from scrapy.contrib.spiders.init import InitSpider
# from scrapy.contrib.spiders import CrawlSpider
# from scrapy.http import Request, FormRequest
# from scrapy.selector import HtmlXPathSelector
# from scrapy.spider import BaseSpider
# import time
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.contrib.spiders import Rule
#
# class DomSpider(InitSpider):
#     name = "app2"
#     # allowed_domains = ["https://app2.com/"]
#     login_page = "https://app2.com/login/index.php"
#     start_urls = [
#         "https://app2.com/"
#     ]
#
#     #rules = (Rule(SgmlLinkExtractor(allow=r'^$'), callback='parse', follow=True),)
#
#     # def start_requests(self):
#     #     yield Request(url=self.login_page, callback=self.login, dont_filter=True)
#
#     def init_request(self):
#         return Request(url=self.login_page, callback=self.login)
#
#     def login(self, response):
#         print "here"
#         return FormRequest.from_response(response, formdata={'username': 'admin', 'password': 'AdminAdmin1!'}, callback=self.check_login_response)
#
#
#     def check_login_response(self, response):
#         """Check the response returned by a login request to see if we are
#         successfully logged in.
#         """
#         # print response.body
#         # with open("page.txt", 'w') as f:
#         #     f.write(response.body)
#         if "Admin User" in response.body:
#             self.log("Successfully logged in. Let's start crawling!")
#             return self.initialized()
#         else:
#             print "nope"
#             self.log("Bad times :(")
#
#     def parse_page(self, response):
#         print "there!"
#         with open("page.txt", 'w') as f:
#             f.write(response.url)
#         # print response.body
#         hxs = HtmlXPathSelector(response)
#         links = hxs.select('//a/@href').extract()
#         for link in links:
#             yield Request(url=link, callback=self.parse_page)
#         # print titles.select('/a/@href').extract()
#         # for url in response.xpath('/a/@href').extract():
#         #     yield scrapy.Request(url, callback=self.parse)
#
# # class DomSpider(scrapy.Spider):
# #     name = "app2"
# #     # allowed_domains = ["https://app2.com/"]
# #     login_page = "https://app2.com/login/index.php"
# #     start_urls = [
# #         "https://app2.com/"
# #     ]
# #
# #     def start_requests(self):
# #         yield Request(url=self.login_page, callback=self.login, dont_filter=True)
# #
# #     def login(self, response):
# #         print "here"
# #         return FormRequest.from_response(response, formdata={'username': 'admin', 'password': 'AdminAdmin1!'}, callback=self.check_login_response)
# #
# #     def parse(self, response):
# #         with open("page.txt", 'w') as f:
# #             f.write(response.url)