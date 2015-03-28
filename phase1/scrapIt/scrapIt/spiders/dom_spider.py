__author__ = 'Vignesh Prakasam'

import scrapy
import os

from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# from scrapIt.items import ScrapitItem
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider
import time
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

class DomSpider(InitSpider):
    name = "app2"
    # allowed_domains = ["https://app2.com/"]
    login_page = "https://app2.com/login/index.php"
    start_urls = [
        "https://app2.com/course/switchrole.php"
    ]

    rules = (Rule(SgmlLinkExtractor(allow=r'^$'), callback='parse', follow=True),)

    def init_request(self):
    #     mydriver = webdriver.Firefox()
    #     mydriver.get(self.login_page)
    #     user_elem =  mydriver.find_element_by_name("username")
    #     user_elem.send_keys("admin")
    #     pass_elem =  mydriver.find_element_by_name("password")
    #     pass_elem.send_keys("AdminAdmin1!")
    #     login_elem =  mydriver.find_element_by_id("loginbtn")
    #     login_elem.send_keys(Keys.RETURN)
    #     if "You are logged in as Admin User" in mydriver.page_source:
    #         print "Successfully logged in. Let's start crawling!"
    #         # self.log("Successfully logged in. Let's start crawling!")
    #         # Now the crawling can begin..
    #         self.initialized()
    #     else:
    #         print "SORRY"
    #         # self.log("Bad times :(")
    #         # Something went wrong, we couldn't log in, so nothing happens.
        return Request(url=self.login_page, callback=self.login)


    def login(self, response):
        print "here"
        return FormRequest.from_response(response, formdata={'username': 'admin', 'password': 'AdminAdmin1!'}, callback=self.check_login_response)


    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        # print response.body
        # with open("page.txt", 'w') as f:
        #     f.write(response.body)
        if "Admin User" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # print "success"
            # print response.body
            # Now the crawling can begin..
            return self.initialized()
        else:
            print "nope"
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.
    # def __init__(self):
    #     self.mydriver = webdriver.Firefox()

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # item = ScrapitItem()
        # item['name'] = response.css('#story-heading').extract()
        # item['desc'] = response.css('#story-body > p:nth-child(4)').extract()
        # yield item
        # print "inside"
        # path = os.path.abspath('page.txt')
        # with open(path, 'w') as f:
        #     f.write(response.body)
        # self.mydriver.get(self.login_page)
        # user_elem =  self.mydriver.find_element_by_name("username")
        # user_elem.send_keys("admin")
        # pass_elem =  self.mydriver.find_element_by_name("password")
        # pass_elem.send_keys("AdminAdmin1!")
        # login_elem =  self.mydriver.find_element_by_id("loginbtn")
        # login_elem.send_keys(Keys.RETURN)
        # time.sleep(2)
        # if "You are logged in as Admin User" in response.body:
        #     print "Successfully logged in. Let's start crawling!"
        #     # self.log("Successfully logged in. Let's start crawling!")
        #     # Now the crawling can begin..
        #     # self.initialized()
        #     print response.body
        # else:
        #     print "sorry"
        #     print response.body
        # self.mydriver.close()
        print "there!"
        with open("page.txt", 'w') as f:
            f.write(response.body)
        # print response.body