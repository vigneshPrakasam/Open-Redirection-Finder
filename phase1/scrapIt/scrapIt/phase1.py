__author__ = 'Vignesh Prakasam'

import json, os
from bs4 import BeautifulSoup
import requests
import copy
import time
from pprint import pprint
import urllib2
import ast
# import requests.packages.urllib3.contrib.pyopenssl
# requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()

############################################---Phase 1 (START)-----###############################################

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
            eleJson["Location"] = "Referer"
            eleJson["type"] = "get"
            getParamsJson[splitLink[0]] = eleJson
    return getParamsJson

def post_params(postreq_dict):
    filepath = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
    #generalize
    filepath = filepath + "\scrapIt\\newPost.txt"
    with open(filepath, 'r') as f:
        postreq_content = f.read()
    forloop = postreq_content.split("$eof$")
    forloop.pop()
    for eachpost in forloop:
        postreq_split = eachpost.split("==")
        temp_str = postreq_split[1]
        evalStr = ast.literal_eval(temp_str)
        postreq_dict[postreq_split[0]] = evalStr
    return postreq_dict

# def postParams(phase1json):
#     postParamsJson = phase1json
#     filepath = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
#     #generalize
#     filepath = filepath + "\scrapIt\\app2Check.txt"
#     # filepath = filepath + "\scrapIt\\app10Check.txt"
#     with open(filepath, 'r') as f:
#         content = f.read()
#     soup = BeautifulSoup(content)
#     forms = soup.find_all('form')
#     for form in forms:
#         print form.get('action')
#         eleJson = {}
#         if form.get('method') is not None:
#             if form.get('method').lower() == "post":
#                 print "******************POST*******************************************"
#                 formSoup = BeautifulSoup(str(form))
#                 inpTag = formSoup.find_all('input')
#                 for inp in inpTag:
#                     if inp.get('type') == "hidden" or inp.get('type') == "text":
#                         # print inp.get('name'), " = ", inp.get('value')
#                         eleJson['type'] = "post"
#                         # eleJson["param"+str(i)] = inp.get('name')
#                         eleJson[inp.get('name')] = inp.get('value')
#                         eleJson["Location"] = "Referer"
#                 postParamsJson[form.get('action')] = eleJson
#
#             if form.get('method').lower() == "get":
#                 print "*********************GET*****************************************"
#                 print form.get('action')
#                 formSoup = BeautifulSoup(str(form))
#                 inpTag = formSoup.find_all('input')
#                 for inp in inpTag:
#                     if inp.get('type') == "hidden" or inp.get('type') == "text":
#                         # print inp.get('name'), " = ", inp.get('value')
#                         eleJson['type'] = "get"
#                         # eleJson["param"+str(i)] = inp.get('name')
#                         eleJson[inp.get('name')] = inp.get('value')
#                         eleJson["Location"] = "Referer"
#                 postParamsJson[form.get('action')] = eleJson
#     return postParamsJson

###################################----Phase 1 (END)--------########################################################

###################################----Phase 2 (START)--------########################################################
phase2json = {"redirectTo": "https://www.google.com"}
###################################----Phase 2 (END)--------########################################################

###################################----Phase 3 (START)--------########################################################

def test():

    phase3json = {}
    sessK = ""

    with open("postGetJSON.JSON") as f:
        postGetJson = json.load(f)

    allLinks = postGetJson.keys()
    print allLinks
    '''-----for each link login and then hit the link----'''

    for eachLink in allLinks:
        '''Fix for url without origin'''
        if "://" not in eachLink:
            #generalize this
            actionLink = "https://app2.com/"+eachLink
            # actionLink = "https://app10.com/"+eachLink
        else:
            actionLink = eachLink

        payload = postGetJson.get(eachLink)

        # Fill in your details here to be posted to the login form.
        formPayload = {'username': 'admin', 'password': 'AdminAdmin1!'}

        # Use 'with' to ensure the session context is closed after use.
        with requests.Session() as s:
            #specific to app2 (generalize this)
            p = s.post('https://app2.com/login/index.php', data=formPayload, verify=False)
            # p = s.post('https://app10.com', verify=False)

            # print the html returned or something more intelligent to see if it's a successful login page.
            # print p.text
            #-------------------------------only for app2 - to get sess key (START)-------------------------------
            soup = BeautifulSoup(p.text)
            allA = soup.find_all('a')
            for indA in allA:
                if indA.get('href') is not None:
                    valA = indA.get('href').split('?')
                    if valA[0] in 'https://app2.com/login/logout.php':
                        sessKsplit = valA[1].split('=')
                        sessK = sessKsplit[1]
                        break
            #-------------------------------only for app2 - to get sess key (END)-------------------------------
            '''*****************************get urls**************************'''
            if payload.get('type') == 'get':
                # fuzzing the payload
                for p in payload.keys():
                    temp = payload.get(p)
                    payload[p] = phase2json.get("redirectTo")
                    #changing the session key
                    if 'sesskey' in payload.keys():
                        payload['sesskey'] = sessK
                    payload.pop('type', None)
                    payload.pop('Location', None)
                    print "----------------------------------------------------------"
                    print eachLink, payload
                    # An authorised request
                    r = s.get(actionLink, params=payload)
                    print r.url
                    #checking if its hitting google.com
                    if r.url.startswith("https://www.google.com"):
                        payload["type"] = "get"
                        phase3json[actionLink] = dict(payload)
                    payload[p] = temp

            '''***********************post urls***********************************'''
            if payload.get('type') == 'post':
                #fuzzing the payload
                for p in payload.keys():
                    temp = payload.get(p)
                    payload[p] = phase2json.get("redirectTo")
                    #changing the session key
                    if 'sesskey' in payload.keys():
                        payload['sesskey'] = sessK
                    payload.pop('type', None)
                    payload.pop('Location', None)
                    print "----------------------------------------------------------"
                    print eachLink, payload
                    # An authorised request
                    r = s.post(actionLink, data=payload)
                    print r.url, payload
                    #checking if its hitting google.com
                    if r.url.startswith("https://www.google.com"):
                        payload["type"] = "post"
                        phase3json[actionLink] = dict(payload)
                    payload[p] = temp

            #for referer redirects
            payload.pop('type', None)
            payload.pop('Location', None)
            print "----------------------------------------------------------"
            print eachLink, payload
            # An authorised request
            s.headers.update({"Referer": phase2json.get("redirectTo")})
            r = s.get(actionLink, params=payload)
            print r.url
            #checking if its hitting google.com
            if r.url.startswith("https://www.google.com"):
                payload["type"] = "get"
                payload["Referer"] = phase2json.get("redirectTo")
                phase3json[actionLink] = dict(payload)
            s.headers.update({"Referer": None})


    jsonphase3String = json.dumps(phase3json, sort_keys=True, indent=8)
    with open("phase3JSON.JSON", 'w') as f:
        f.write(jsonphase3String)
    print jsonphase3String

###################################----Phase 3 (END)--------########################################################



##################################------test units(start)--------########################################################
def phase3TestUnit():
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



def app10TestUnit():
    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        para = {
                "Referer": "https://www.google.com",
                "cmd": "xe",
                "type": "get",
                "xe": "4"
        }
        para.pop("Referer", None)
        para.pop("type", None)
        s.headers.update({"Referer": "https://www.google.com"})
        r = s.get("http://app10.com/index.php", params=para, verify=False)
        print r.url

def testgig():
    filepath = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
    #generalize
    filepath = filepath + "\scrapIt\\newPost.txt"
    # filepath = filepath + "\scrapIt\\app10Check.txt"
    # with open(filepath, 'r') as f:
    #     content = f.read()
    # postreq_json = {}
    with open(filepath, 'r') as f:
        postreq_content = f.read()

    postreq_dict = {}
    forloop = postreq_content.split("$eof$")
    forloop.pop()
    eleJson = {}
    for eachpost in forloop:
        postreq_split = eachpost.split("==")
        temp_str = postreq_split[1]
        # print temp_str
        evalStr = ast.literal_eval(temp_str)
        # eleJson = temp_str[1:len(temp_str)-1]
        postreq_dict[postreq_split[0]] = evalStr

    # print postreq_json
    postreq_json = json.dumps(postreq_dict, sort_keys=True, indent=8)
    with open("postGetJSON.JSON", 'w') as f:
        f.write(postreq_json)

    print postreq_json
    with open("postGetJSON.JSON") as f:
        postGetJson = json.load(f)
    # val = postGetJson["https://app2.com/tag/manage.php"]




    # postreq_json = postreq_json
    # print json.dumps(postreq_json, sort_keys=True, indent=8)



###############################----test units(END)------#################################################

# json1 = {}
# json2 = getParams(json1)
# phase1json = post_params(json2)
# jsonString = json.dumps(phase1json, sort_keys=True, indent=8)
# try:
#     os.remove("postGetJSON.JSON")
# except OSError:
#         pass
# with open("postGetJSON.JSON", 'w') as f:
#     f.write(jsonString)
# print jsonString

test()
# app10TestUnit()
# testgig()