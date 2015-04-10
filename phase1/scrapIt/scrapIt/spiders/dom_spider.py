from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import scrapy
from scrapy.http import FormRequest
from scrapy import log
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup

class ExampleSpider(CrawlSpider):
    name = 'app2'
    start_urls = ['https://app2.com/login/index.php']

    def parse(self, response):
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
        with open("app2Check.txt", 'a') as f:
            f.write(str(forms))
        ############################################

        duplicateCheck = {}
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//a/@href').extract()
        # links.append(hxs.select('//form/@action').extract())
        postLinks = hxs.select('//form/@action').extract()
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
            if "https://app2.com" in link and "https://app2.com/calendar/" not in link:
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