__author__ = 'Vignesh Prakasam'

import json, os
from bs4 import BeautifulSoup

def getParams(getParamsJson):
    # alreadyCrawled = {}
    # getParamsJson = {}
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
            # print splitLink[0]
            # print splitLink[1]
            str1 = splitLink[1].split("&")
            for parList in str1:
                param, value = parList.split("=")
                eleJson[param] = value
            eleJson["type"] = "get"
            getParamsJson[splitLink[0]] = eleJson
    # jsonString = json.dumps(getParamsJson, sort_keys=True, indent=8)
    # print jsonString
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
                print form.get('action')
                formSoup = BeautifulSoup(str(form))
                inpTag = formSoup.find_all('input')
                for inp in inpTag:
                    if inp.get('type') == "hidden" or inp.get('type') == "text":
                        print inp.get('name'), " = ", inp.get('value')
                        eleJson['type'] = "post"
                        # eleJson["param"+str(i)] = inp.get('name')
                        eleJson[inp.get('name')] = inp.get('value')
                        i += 1
                postParamsJson[form.get('action')] = eleJson

            if form.get('method').lower() == "get":
                print "*********************GET*****************************************"
                i = 0
                print form.get('action')
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
    # jsonString = json.dumps(postParamsJson, sort_keys=True, indent=8)
    # print jsonString
    return postParamsJson

json1 = {}
json2 = getParams(json1)
phase1json = postParams(json2)
jsonString = json.dumps(phase1json, sort_keys=True, indent=8)
print jsonString
# injectionsPoints()