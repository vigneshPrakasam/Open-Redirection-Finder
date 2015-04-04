__author__ = 'Vignesh Prakasam'

import json, os
from bs4 import BeautifulSoup


def injectionsPoints():
    rawGetDictionary = getParams()
    allKeys = rawGetDictionary.keys()
    allVals = rawGetDictionary.values()
    jsonPhase1 = {}
    eleJson = {}
    i = 0
    # print allKeys
    # print allVals
    tot = zip(allKeys, allVals)
    for url, paramValue in tot:
        # print url
        # print paramValue
        i = 0
        eleJson["type"] = "get"
        for val in paramValue:
            eleJson["param"+str(i)] = val
            i += 1
        jsonPhase1[url] = eleJson
        eleJson = {}
    jsonString = json.dumps(jsonPhase1, sort_keys=True, indent=8)
    print jsonString


def getParams():
    alreadyCrawled = {}
    filepath = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
    filepath = filepath + "\scrapIt\getLinks.txt"
    with open(filepath, 'r') as f:
        content = f.readlines()
    for link in content:
        if "?" in link:
            splitLink = link.split("?")
            # print splitLink[0]
            # print splitLink[1]
            if alreadyCrawled.get(link) == splitLink[1]:
                pass
            else:
                params = []
                str1 = splitLink[1].split("=")
                for p in str1:
                    if "&" in p:
                        str2 = p.split("&")
                        params.append(str2[1])
                    else:
                        params.append(p)
                params.pop()
                alreadyCrawled[link] = params
            splitLink = []

    return alreadyCrawled


# injectionsPoints()
# filepath = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
# print filepath+"\scrapIt\getLinks.txt"
filepath1 = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
filepath1 = filepath1 + "\scrapIt\\app2Check.txt"
with open(filepath1, 'r') as f:
    content = f.read()
soup = BeautifulSoup(content)
forms = soup.find_all('form')
filepath2 = os.path.dirname(os.path.abspath(__file__)).strip("\scrapIt")
filepath2 = filepath2 + "\scrapIt\\check.txt"
for form in forms:
    # with open(filepath2, 'a') as f:
    #     f.write(str(form))
    print form.get('action')
    formSoup = BeautifulSoup(str(form))
    inpTag = formSoup.find_all('input')
    for inp in inpTag:
        print inp.get('name'), " = ", inp.get('value')
