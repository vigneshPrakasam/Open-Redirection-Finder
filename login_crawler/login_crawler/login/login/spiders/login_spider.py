from scrapy.spider import Spider
from scrapy.http import FormRequest
from loginform import fill_login_form
from urlparse import urljoin
from bs4 import BeautifulSoup
import scrapy
from scrapy.http import Request
import os
class LoginSpider(Spider):
    name = "login"
    start_urls = [
    #"http://zencart.com/index.php?main_page=login"
    #"http://192.168.56.102/phpScheduleIt/" #phpScheduleit
    #"http://192.168.56.106/index.php/customer/account/login/" #Magneto"
    #"http://192.168.56.101/profile.php?action=login" #Astrospaces
    #"http://192.168.56.102/CubeCart/index.php?_a=login"#Cubecart
    #"http://192.168.56.103/dokeos/index.php" #Dokeos
    #"http://192.168.56.104/efront/www/index.php?" #eFront
    #"http://192.168.56.105/elgg/" #Elgg
    #"http://192.168.56.107/owncloud/" #owncloud
    #"http://192.168.56.108/index.php?route=account/login" #opencart
    #"http://192.168.56.109/index.php/site/login" #x2crm
    #"http://192.168.56.110/src/login.php" #squirrelmail
    #"http://192.168.56.101/catalog/login.php" #osCommerce
    #"http://192.168.56.103/piwigo-2.0.0/identification.php" #piwigo
    #"http://192.168.56.102/login.php" #Phorum
    #"http://192.168.56.109/prestashop/authentication.php" #PrestaShop
    # "http://192.168.56.106/cpg/login.php?referer=index.php" #Gallery
    "https://app2.com/login/index.php" #moodle-app2
    # "https://app8.com/upload/index.php?route=account/login"
    ]
    
    credentials = {
        "http://zencart.com/index.php?main_page=login":['student@student.com','student'], #zencart
        "http://192.168.56.102/phpScheduleIt/":['student@email.com','student'], #phpscheduleit
        "http://192.168.56.106/index.php/customer/account/login/":['student@student.com','student'], #magneto
        "http://192.168.56.101/profile.php?action=login": ['student@student.com','student'], #Astrospaces
        "http://192.168.56.102/CubeCart/index.php?_a=login" : ['student@student.com','student'], #Cubecart
        "http://192.168.56.103/dokeos/index.php":['student','student'], #Dokeos
        "http://192.168.56.104/efront/www/index.php?":['student','student'], #eFront
        "http://192.168.56.105/elgg/":['student','student'], #Elgg
        "http://192.168.56.107/owncloud/":['student','student'], #owncloud
        "http://192.168.56.108/index.php?route=account/login":['student@student.com','student'], #opencart
        "http://192.168.56.109/index.php/site/login":['student','student'], #x2crm
        "http://192.168.56.110/src/login.php":['student','student'], #squirrelmail
        "http://192.168.56.101/catalog/login.php":['student@student.com','student'], #osCommerce
        "http://192.168.56.103/piwigo-2.0.0/identification.php":['student','student'], #Piwigo
        "http://192.168.56.102/login.php":['student','student'], #Phorum
        "http://192.168.56.109/prestashop/authentication.php":['student@student.com','student'], #PrestaShop
        "http://192.168.56.106/cpg/login.php?referer=index.php":['student','student'], #Gallery
        "https://app2.com/login/index.php":['admin','AdminAdmin1!'], #moodle-app2
        "https://app8.com/upload/index.php?route=account/login":['admin','AdminAdmin1!']
    }

    origin = "https://app2.com/" #Please provide the origin of the application so that the crawler doesn't go out of the application while scraping
    logout_link = "https://app2.com/login/logout.php" #Please provide logout link of your application so that the crawler doesn't come out of the user session and stop crawling
    seen_list = {} #Dictionary to find duplicate requests
    
    def parse(self,response):
        #deleting files:
        try:
            if os.path.exists("newPost.txt"):
                os.remove("newPost.txt")
            if os.path.exists("newgetLinks.txt"):
                os.remove("newgetLinks.txt")
            if os.path.exists("scrappedurls.txt"):
                os.remove("scrappedurls.txt")
        except:
            pass
        #print "Status:",response.status       
        #print "Request Headers"
        #print response.request.headers.items()
        #print "\n\n"
        #print "Response Headers"
        #print response.headers.items()
        #print "\n\n"
          
        login_user = self.credentials[response.request.url][0]
        print login_user
        login_pass = self.credentials[response.request.url][1]
        print login_pass
        args, url, method, name , number = fill_login_form(response.url, response.body, login_user, login_pass)

        if name:
                yield FormRequest.from_response(response, method=method, formdata=args, formname=name, callback=self.after_login)
        else:
                yield FormRequest.from_response(response, method=method, formdata=args, formnumber=number, callback=self.after_login)
        
                         
     
    def after_login(self, response):
                #print "Login Request Headers"
                #print response.request.headers
                #print "\n\n"
                #print "Login Response Headers"
                #print response.headers
                #print "\n\n"
                print "After Login Attempt"
                
                #print response.headers
                #print response.body
                if response.headers.get('Refresh'):
                
                        new_url = urljoin(response.url,response.headers.get('Refresh').split(';')[1].split("=")[1])
                        yield scrapy.Request(new_url,callback=self.after_login1)
                
                elif response.headers.get('Location'):
                        print "Have to make another request" 
                               
                else:
                        if "Log Out" in response.body or "Logout" in response.body or "Log out" in response.body or "Log Off" in response.body: 
                                print "hereYes!!!"
                                #Crawl from here!!
                                ############################################
                                with open("scrappedurls.txt", 'a') as f:
                                    f.write(response.url+"\n")
                                    # if response.url == "https://app2.com/user/files.php":
                                    #     f.write(response.body+"\n")

                                soup = BeautifulSoup(response.body)
                                forms = soup.find_all('form')
                                for form in forms:
                                    eleJson = {}
                                    if form.get('method') is not None:
                                        if form.get('method').lower() == "post":
                                            formSoup = BeautifulSoup(str(form))
                                            inpTag = formSoup.find_all('input')
                                            for inp in inpTag:
                                                if inp.get('type') == "hidden" or inp.get('type') == "text":
                                                    eleJson['type'] = "post"
                                                    eleJson[inp.get('name')] = inp.get('value')
                                                    eleJson["Location"] = "Referer"
                                            with open("newPost.txt", 'a') as f:
                                                if form.get('action') is not None:
                                                    f.write(form.get('action')+"=!="+str(eleJson)+"\n")
                                                else:
                                                    f.write(""+"=!="+str(eleJson)+"\n")

                                        if form.get('method').lower() == "get":
                                            formSoup = BeautifulSoup(str(form))
                                            inpTag = formSoup.find_all('input')
                                            for inp in inpTag:
                                                if inp.get('type') == "hidden" or inp.get('type') == "text":
                                                    eleJson['type'] = "get"
                                                    eleJson[inp.get('name')] = inp.get('value')
                                                    eleJson["Location"] = "Referer"
                                            with open("newPost.txt", 'a') as f:
                                                if form.get('action') is not None:
                                                    f.write(form.get('action')+"=!="+str(eleJson)+"\n")
                                                else:
                                                    f.write(""+"=!="+str(eleJson)+"\n")
                                ############################################

                                get_links_list = response.selector.xpath('//a/@href').extract()
                                forms_inpage = response.selector.xpath('//form').extract()
                                num_of_forms = len(forms_inpage)


                                for n in xrange(0, num_of_forms):
                                    print "####################--"+str(n)
                                    yield FormRequest.from_response(response, formnumber=n, callback=self.after_login)


                                #only process external/full link
                                for link in get_links_list:
                                    if "?" in link:
                                        link_split = link.split("?")
                                        str1 = link_split[0]
                                        str2 = link_split[1].split("&")
                                        parameters = ""
                                        for para_list in str2:
                                            parameters = para_list.split("=")[0]
                                        seen = str1+parameters
                                    else:
                                        seen = link
                                    if self.origin in link and self.logout_link not in link and self.seen_list.get(seen) is None:
                                            self.seen_list[seen] = seen
                                            with open("newgetLinks.txt", 'a') as f:
                                                f.write(link+"\n")
                                            yield Request(url=link, callback=self.after_login)


                        elif "administrator" in response.url: #This is for eFront
                                print "Yes!!!" 
                        elif "webmail.php" in response.url:
                                print "Yes!!"
                        else:        
                                print "Sorry"


    def after_login1(self,response):
                #print response.body
                if "Log Out" in response.body or "Logout" in response.body or "Log out" in response.body:
                        print "Yeess, in"  
                        #crawl from here
                        ############################################
                        with open("scrappedurls.txt", 'a') as f:
                            f.write(response.url+"\n")
                            # if response.url == "https://app2.com/user/files.php":
                            #     f.write(response.body+"\n")

                        soup = BeautifulSoup(response.body)
                        forms = soup.find_all('form')
                        for form in forms:
                            eleJson = {}
                            if form.get('method') is not None:
                                if form.get('method').lower() == "post":
                                    formSoup = BeautifulSoup(str(form))
                                    inpTag = formSoup.find_all('input')
                                    for inp in inpTag:
                                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                                            eleJson['type'] = "post"
                                            eleJson[inp.get('name')] = inp.get('value')
                                            eleJson["Location"] = "Referer"
                                    with open("newPost.txt", 'a') as f:
                                        if form.get('action') is not None:
                                            f.write(form.get('action')+"=!="+str(eleJson)+"\n")
                                        else:
                                            f.write(""+"=!="+str(eleJson)+"\n")

                                if form.get('method').lower() == "get":
                                    formSoup = BeautifulSoup(str(form))
                                    inpTag = formSoup.find_all('input')
                                    for inp in inpTag:
                                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                                            eleJson['type'] = "get"
                                            eleJson[inp.get('name')] = inp.get('value')
                                            eleJson["Location"] = "Referer"
                                    with open("newPost.txt", 'a') as f:
                                        if form.get('action') is not None:
                                            f.write(form.get('action')+"=!="+str(eleJson)+"\n")
                                        else:
                                            f.write(""+"=!="+str(eleJson)+"\n")
                        ############################################

                        get_links_list = response.selector.xpath('//a/@href').extract()
                        forms_inpage = response.selector.xpath('//form').extract()
                        num_of_forms = len(forms_inpage)


                        for n in xrange(0, num_of_forms):
                            print "####################--"+str(n)
                            yield FormRequest.from_response(response, formnumber=n, callback=self.after_login1)


                        #only process external/full link
                        for link in get_links_list:
                            if "?" in link:
                                link_split = link.split("?")
                                str1 = link_split[0]
                                str2 = link_split[1].split("&")
                                parameters = ""
                                for para_list in str2:
                                    parameters = para_list.split("=")[0]
                                seen = str1+parameters
                            else:
                                seen = link
                            if self.origin in link and self.logout_link not in link and self.seen_list.get(seen) is None:
                                    self.seen_list[seen] = seen
                                    with open("newgetLinks.txt", 'a') as f:
                                        f.write(link+"\n")
                                    yield Request(url=link, callback=self.after_login1)


                elif "administrator" in response.url: #This is for eFront
                        print "Yes!!!"
                elif "webmail.php" in response.url:
                        print "Yes!!"
                else:
                        print "Sorry"
######################################################################################################################
class NoLoginSpider(Spider):
    name = "nologin"
    start_urls = [
    "http://bm1.com" #demostore
    ]

    origin = "http://bm1.com/" #Please provide the origin of the application so that the crawler doesn't go out of the application while scraping ('/' is mandatory)
    logout_link = "logout.php" #Please provide logout link of your application so that the crawler doesn't come out of the user session and stop crawling
    seen_list = {} #Dictionary to find duplicate requests

    def parse(self,response):
        #deleting the existing files:
        try:
            if os.path.exists("newPost.txt"):
                os.remove("newPost.txt")
            if os.path.exists("newgetLinks.txt"):
                os.remove("newgetLinks.txt")
            if os.path.exists("scrappedurls.txt"):
                os.remove("scrappedurls.txt")
        except:
            pass
        yield Request(url=response.url, callback=self.after_login1)

    def after_login1(self,response):
        with open("scrappedurls.txt", 'a') as f:
            f.write(response.url+"\n")
            # if response.url == "https://app2.com/user/files.php":
            #     f.write(response.body+"\n")

        soup = BeautifulSoup(response.body)
        forms = soup.find_all('form')
        for form in forms:
            eleJson = {}
            if form.get('method') is not None:
                if form.get('method').lower() == "post":
                    formSoup = BeautifulSoup(str(form))
                    inpTag = formSoup.find_all('input')
                    for inp in inpTag:
                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                            eleJson['type'] = "post"
                            eleJson[inp.get('name')] = inp.get('value')
                            eleJson["Location"] = "Referer"
                    with open("newPost.txt", 'a') as f:
                        if form.get('action') is not None:
                            f.write(form.get('action')+"=!="+str(eleJson)+"\n")
                        else:
                            f.write(""+"=!="+str(eleJson)+"\n")

                if form.get('method').lower() == "get":
                    formSoup = BeautifulSoup(str(form))
                    inpTag = formSoup.find_all('input')
                    for inp in inpTag:
                        if inp.get('type') == "hidden" or inp.get('type') == "text":
                            eleJson['type'] = "get"
                            eleJson[inp.get('name')] = inp.get('value')
                            eleJson["Location"] = "Referer"
                    with open("newPost.txt", 'a') as f:
                        if form.get('action') is not None:
                            f.write(form.get('action')+"=!="+str(eleJson)+"\n")
                        else:
                            f.write(""+"=!="+str(eleJson)+"\n")

        get_links_list = response.selector.xpath('//a/@href').extract()
        forms_inpage = response.selector.xpath('//form').extract()
        num_of_forms = len(forms_inpage)

        for n in xrange(0, num_of_forms):
            print "####################--"+str(n)
            yield FormRequest.from_response(response, formnumber=n, callback=self.after_login1)

        #only process external/full link
        for link in get_links_list:
            if "?" in link:
                link_split = link.split("?")
                str1 = link_split[0]
                str2 = link_split[1].split("&")
                parameters = ""
                for para_list in str2:
                    parameters = para_list.split("=")[0]
                seen = str1+parameters
            else:
                seen = link

            if "://" not in link:
                    print link
                    link = self.origin+link
            if self.origin in link and self.logout_link not in link and self.seen_list.get(seen) is None:
                    self.seen_list[seen] = seen
                    print link
                    with open("newgetLinks.txt", 'a') as f:
                        f.write(link+"\n")
                    yield Request(url=link, callback=self.after_login1)
