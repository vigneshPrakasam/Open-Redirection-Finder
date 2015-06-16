from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import scrapy
from scrapy.http import FormRequest
from scrapy import log
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup
import os
import urllib
import json
import ast

class ExampleSpider(CrawlSpider):
    name = 'app2'
    start_urls = ['https://app2.com/login/index.php']
    postParamsJson = {}
    postreq_list = []

    def parse(self, response):
        try:
            os.remove("newPost.txt")
            os.remove("newpostLinks.txt")
            os.remove("newgetLinks.txt")
            #generalize
            os.remove("app2Check.txt")
        except OSError:
            pass
        return FormRequest.from_response(
            response,
            formdata={'username': 'admin', 'password': 'AdminAdmin1!'},
            callback=self.parse_page
        )

    def parse_page(self, response):
        """ Scrape useful stuff from page, and spawn new requests
        """
        ############################################
        soup = BeautifulSoup(response.body)
        forms = soup.find_all('form')
        for form in forms:
            eleJson = {}
            if form.get('method') is not None:
                if form.get('method').lower() == "post":
                    print "******************POST*******************************************"
                    formSoup = BeautifulSoup(str(form))
                    inpTag = formSoup.find_all('input')
                    for inp in inpTag:
                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                            # print inp.get('name'), " = ", inp.get('value')
                            eleJson['type'] = "post"
                            # eleJson["param"+str(i)] = inp.get('name')
                            eleJson[inp.get('name')] = inp.get('value')
                            eleJson["Location"] = "Referer"
                    # self.postreq_list.append(str(form.get('action'))+"=="+str(eleJson))
                    # self.postParamsJson[form.get('action')] = eleJson
                    with open("newPost.txt", 'a') as f:
                        f.write(form.get('action')+"=="+str(eleJson)+"$eof$")
                    # with open("newPost.txt", 'w') as f:
                    #     f.write(json.dumps(self.postParamsJson, sort_keys=True, indent=8))


                if form.get('method').lower() == "get":
                    print "*********************GET*****************************************"
                    formSoup = BeautifulSoup(str(form))
                    inpTag = formSoup.find_all('input')
                    for inp in inpTag:
                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                            # print inp.get('name'), " = ", inp.get('value')
                            eleJson['type'] = "get"
                            # eleJson["param"+str(i)] = inp.get('name')
                            eleJson[inp.get('name')] = inp.get('value')
                            eleJson["Location"] = "Referer"
                    # self.postParamsJson[form.get('action')] = eleJson
                    with open("newPost.txt", 'a') as f:
                        f.write(form.get('action')+"=="+str(eleJson)+"$eof$")
                    # with open("newPost.txt", 'w') as f:
                    #     f.write(json.dumps(self.postParamsJson, sort_keys=True, indent=8))
            # with open("newPost.txt", 'a') as f:
            #     f.write(str(self.postParamsJson))
            # with open("app2Check.txt", 'a') as f:
            #     f.write(str(form))
        ############################################
        duplicateCheck = {}
        # hxs = HtmlXPathSelector(response)
        # links = hxs.select('//a/@href').extract()
        # postLinks = hxs.select('//form/@action').extract()
        links = response.selector.xpath('//a/@href').extract()
        postLinks = response.selector.xpath('//form/@action').extract()

        ######---form links

        for form in forms:
            eleJsonParams = {}
            if form.get('method') is not None:
                if form.get('method').lower() == "post":
                    # formsoup = BeautifulSoup(form)
                    formurl = form.get('action')
                    if "://" not in formurl:
                        hiturl = "https://app2.com"+formurl
                    else:
                        hiturl = formurl
                    inpTag = form.find_all('input')
                    for inp in inpTag:
                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                            eleJsonParams[inp.get('name')] = inp.get('value')
                    if duplicateCheck.get(hiturl) != hiturl:
                        print "posting the form"
                        postLinks.append(hiturl)
                        duplicateCheck[hiturl] = hiturl
                        yield Request(url=hiturl, method="POST", body=urllib.urlencode(eleJsonParams), callback=self.parse_page)
                if form.get('method').lower() == "get":
                    # formsoup = BeautifulSoup(form)
                    formurl = form.get('action')
                    if "://" not in formurl:
                        hiturl = "https://app2.com"+formurl
                    else:
                        hiturl = formurl
                    inpTag = form.find_all('input')
                    for inp in inpTag:
                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                            eleJsonParams[inp.get('name')] = inp.get('value')
                    if duplicateCheck.get(hiturl) != hiturl:
                        print "posting the form"
                        postLinks.append(hiturl)
                        duplicateCheck[hiturl] = hiturl
                        yield Request(url=hiturl, method="GET", body=urllib.urlencode(eleJsonParams), callback=self.parse_page)
        #####

        if not postLinks:
            print "empty"
        else:
            for postLink in postLinks:
                with open("newpostLinks.txt", 'a') as f:
                    f.write(postLink+"\n")


        for link in links:
            # print link
            #only process external/full link
            if "https://app2.com" in link and "https://app2.com/calendar/" not in link and "logout.php" not in link:
                splitlink = link.split("?")
                if duplicateCheck.get(splitlink[0]) != splitlink[0]:
                    duplicateCheck[splitlink[0]] = splitlink[0]
                    with open("newgetLinks.txt", 'a') as f:
                        f.write(link+"\n")
                    yield Request(url=link, callback=self.parse_page)

        # jsonString = json.dumps(self.postParamsJson, sort_keys=True, indent=8)
        # with open("newPost.JSON", 'a') as f:
        #     f.write(jsonString)

class App10Spider(CrawlSpider):
    name = 'app10'
    start_urls = ['https://app10.com']

    def parse(self, response):
        try:
            os.remove("newpostLinks.txt")
            os.remove("newgetLinks.txt")
        except OSError:
            pass
        yield Request(url=response.url, callback=self.parse_page)

    def parse_page(self, response):
        """ Scrape useful stuff from page, and spawn new requests
        """
        ############################################
        soup = BeautifulSoup(response.body)
        forms = soup.find_all('form')
        with open("app10Check.txt", 'a') as f:
            f.write(str(forms))
        ############################################

        duplicateCheck = {}
        # hxs = HtmlXPathSelector(response)
        links = response.selector.xpath('//a/@href').extract()
        # links.append(hxs.select('//form/@action').extract())
        postLinks = response.selector.xpath('//form/@action').extract()
        # links.append(postLinks)
        if not postLinks:
            print "empty"
        else:
            for postLink in postLinks:
                with open("newpostLinks.txt", 'a') as f:
                    f.write(postLink+"\n")


        for link in links:
            # print link
            #only process external/full link
            if "//app10.com" in link:
                if duplicateCheck.get(link) != link:
                    duplicateCheck[link] = link
                    with open("newgetLinks.txt", 'a') as f:
                        f.write(link+"\n")
                    yield Request(url=link, callback=self.parse_page)




# #independent checks
# class AppSpider(CrawlSpider):
#     name = 'app2-check'
#     start_urls = ['https://app2.com/login/index.php']
#
#     # 'log' and 'pwd' are names of the username and password fields
#     # depends on each website, you'll have to change those fields properly
#     # one may use loginform lib https://github.com/scrapy/loginform to make it easier
#     # when handling multiple credentials from multiple sites.
#     def parse(self, response):
#         return FormRequest.from_response(
#             response,
#             formdata={'username': 'admin', 'password': 'AdminAdmin1!'},
#             callback=self.after_login
#         )
#
#
#     def after_login(self, response):
#         # check login succeed before going on
#         if "Invalid login" in response.body:
#             self.log("Login failed", level=log.ERROR)
#             return
#
#         # continue scraping with authenticated session...
#         else:
#             self.log("Login succeed!", level=log.DEBUG)
#             return Request(url="https://app2.com/backup/restorefile.php?contextid=20",
#                            callback=self.parse_page)
#
#     # example of crawling all other urls in the site with the same
#     # authenticated session.
#     def parse_page(self, response):
#         """ Scrape useful stuff from page, and spawn new requests
#         """
#         # hxs = HtmlXPathSelector(response)
#         # links = hxs.select('//a/@href').extract()
#         # print links
#         with open("app2Check.txt", 'w') as f:
#             f.write(response.body)
#             # for link in links:
#             #     f.write(link)