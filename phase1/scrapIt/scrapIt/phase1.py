__author__ = 'Vignesh Prakasam'

import json, os
from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
import urllib2
# import requests.packages.urllib3.contrib.pyopenssl
# requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()

def getParams(getParamsJson):
    filepath = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
    filepath = filepath + "\scrapIt\\newgetLinks.txt"
    with open(filepath, 'r') as f:
        content = f.readlines()
    for link in content:
        nlink = link.split("\n")
        link = nlink[0]
        eleJson = {}
        if "?" in link:
            splitLink = link.split("?")
            str1 = splitLink[1].split("&")
            for parList in str1:
                param, value = parList.split("=")
                eleJson[param] = value
            eleJson["type"] = "get"
            getParamsJson[splitLink[0]] = eleJson
    return getParamsJson

def postParams(phase1json):
    postParamsJson = phase1json
    filepath = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
    filepath = filepath + "\scrapIt\\app2Check.txt"
    with open(filepath, 'r') as f:
        content = f.read()
    soup = BeautifulSoup(content)
    forms = soup.find_all('form')
    for form in forms:
        eleJson = {}
        if form.get('method') is not None:
            if form.get('method').lower() == "post":
                print "******************POST*******************************************"
                i = 0
                # print form.get('action')
                formSoup = BeautifulSoup(str(form))
                inpTag = formSoup.find_all('input')
                for inp in inpTag:
                    if inp.get('type') == "hidden" or inp.get('type') == "text":
                        # print inp.get('name'), " = ", inp.get('value')
                        eleJson['type'] = "post"
                        # eleJson["param"+str(i)] = inp.get('name')
                        eleJson[inp.get('name')] = inp.get('value')
                        i += 1
                postParamsJson[form.get('action')] = eleJson

            if form.get('method').lower() == "get":
                print "*********************GET*****************************************"
                i = 0
                # print form.get('action')
                formSoup = BeautifulSoup(str(form))
                inpTag = formSoup.find_all('input')
                for inp in inpTag:
                    if inp.get('type') == "hidden" or inp.get('type') == "text":
                        # print inp.get('name'), " = ", inp.get('value')
                        eleJson['type'] = "get"
                        # eleJson["param"+str(i)] = inp.get('name')
                        eleJson[inp.get('name')] = inp.get('value')
                        i += 1
                postParamsJson[form.get('action')] = eleJson
    return postParamsJson

def test():
    sessK = ""

    with open("postGetJSON.JSON") as f:
        postGetJson = json.load(f)

    allLinks = postGetJson.keys()
    print allLinks
    '''-----for each link login and then hit the link----'''

    for eachLink in allLinks:
        '''Fix for url without origin'''
        if "https://" not in eachLink:
            actionLink = "https://app2.com/"+eachLink
        else:
            actionLink = eachLink

        payload = postGetJson.get(eachLink)

        # Fill in your details here to be posted to the login form.
        formPayload = {'username': 'admin', 'password': 'AdminAdmin1!'}

        # Use 'with' to ensure the session context is closed after use.
        with requests.Session() as s:
            p = s.post('https://app2.com/login/index.php', data=formPayload, verify=False)
            # print the html returned or something more intelligent to see if it's a successful login page.
            # print p.text
            soup = BeautifulSoup(p.text)
            allA = soup.find_all('a')
            for indA in allA:
                if indA.get('href') is not None:
                    valA = indA.get('href').split('?')
                    if valA[0] in 'https://app2.com/login/logout.php':
                        sessKsplit = valA[1].split('=')
                        sessK = sessKsplit[1]
                        break

            '''*****************************get urls**************************'''

            if payload.get('type') == 'get':
                if 'returnurl' in payload.keys():
                    payload['returnurl'] = "https://www.google.com"
                if 'sesskey' in payload.keys():
                    payload['sesskey'] = sessK
                payload.pop('type', None)
                print "----------------------------------------------------------"
                print eachLink, payload
                # An authorised request
                r = s.get(actionLink, params=payload)
                print r.url

            '''***********************post urls***********************************'''
            if payload.get('type') == 'post':
                if 'returnurl' in payload.keys():
                    payload['returnurl'] = "https://www.google.com"
                if 'sesskey' in payload.keys():
                    payload['sesskey'] = sessK
                payload.pop('type', None)
                print "----------------------------------------------------------"
                print eachLink, payload
                # An authorised request
                r = s.post(actionLink, data=payload)
                print r.url

        # with open("postGetJSON.JSON") as f:
        #     postGetJson = json.load(f)
        #
        # allLinks = postGetJson.keys()
        # print allLinks
        #
        # for eachLink in allLinks:
        #     payload = postGetJson.get(eachLink)
        #     if payload.get('type') == 'get':
        #         if 'returnurl' in payload.keys():
        #             payload['returnurl'] = "https://www.google.com"
        #         if 'sesskey' in payload.keys():
        #             payload['sesskey'] = sessK
        #         payload.pop('type', None)
        #         print "----------------------------------------------------------"
        #         print eachLink, payload
        #         # An authorised request
        #         r = s.get(eachLink, params=payload)
        #         print r.url

        # payload = {
        #         "id": "2",
        #         "returnurl": "https://www.google.com",
        #         "sesskey": sessK,
        #         "switchrole": "0",
        #         "type": "get"
        # }
        # r = s.get('https://app2.com/course/switchrole.php', params=payload)
        # print r.url

def postTest():
    sessK = ""

    # Fill in your details here to be posted to the login form.
    formPayload = {'username': 'admin', 'password': 'AdminAdmin1!'}

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        p = s.post('https://app2.com/login/index.php', data=formPayload, verify=False)
        soup = BeautifulSoup(p.text)
        allA = soup.find_all('a')
        for indA in allA:
            if indA.get('href') is not None:
                valA = indA.get('href').split('?')
                if valA[0] in 'https://app2.com/login/logout.php':
                    sessKsplit = valA[1].split('=')
                    sessK = sessKsplit[1]
                    break

        payload = {
                "coursetag_new_tag": "",
                "coursetag_sug_keyword": "",
                "entryid": "2",
                "returnurl": "https://app2.com/course/view.php?id=2",
                "sesskey": sessK,
                "type": "post",
                "userid": "2"
        }
        r = s.post('https://app2.com/tag/coursetags_add.php', data=payload)
        print r.url

# json1 = {}
# json2 = getParams(json1)
# phase1json = postParams(json2)
# jsonString = json.dumps(phase1json, sort_keys=True, indent=8)
# with open("postGetJSON.JSON", 'w') as f:
#     f.write(jsonString)
# print jsonString

test()