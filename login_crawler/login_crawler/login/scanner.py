__author__ = 'Vignesh Prakasam'

import json
import os
from bs4 import BeautifulSoup
import requests
import ast
from urlparse import urlparse, parse_qs


############################################---Phase 1 (START)-----###############################################
# key = ""

def getParams():
    getParamsJson=dict()
    try:
        with open("newgetLinks.txt", 'r') as f:
            content = f.readlines()
        for link in content:
            nlink = link.split("\n")
            link = nlink[0]
            eleJson = {}
            if "?" in link:
                splitLink = link.split("?")
                str1 = splitLink[1].split("&")
                for parList in str1:
                    # param, value = parList.split("=")
                    param_value = parList.split("=")
                    if param_value[0] is not None and param_value[1] is not None:
                        eleJson[param_value[0]] = param_value[1]
                    elif param_value[0] is not None:
                        eleJson[param_value[0]] = ""
                    else:
                        pass
                eleJson["Location"] = "Referer"
                eleJson["type"] = "get"
                # getParamsJson[splitLink[0]] = eleJson
                key = splitLink[0]
                if key in getParamsJson.keys():
                    allVals = getParamsJson.get(key)
                    if eleJson in allVals:
                        getParamsJson[key].append(eleJson)
                else:
                    getParamsJson[key] = [eleJson]
    except IOError:
        pass
    return getParamsJson

def post_params():
    postreq_dict = dict()
    try:
        with open("newPost.txt", 'r') as f:
            # postreq_content = f.readlines()
            forloop = f.readlines()
        # print postreq_content
        # forloop = postreq_content.split("$eof$")
        # forloop.pop()
        for eachpost in forloop:
            postreq_split = eachpost.split("=!=")
            temp_str = postreq_split[1]
            evalStr = ast.literal_eval(temp_str)
            key = postreq_split[0]
            # postreq_dict.setdefault(key, [])
            if key in postreq_dict.keys():
                allVals = postreq_dict.get(key)
                if evalStr not in allVals:
                    postreq_dict[key].append(evalStr)
            else:
                postreq_dict[key] = [evalStr]
    except IOError:
        pass
    return postreq_dict

###################################----Phase 1 (END)--------########################################################

###################################----Phase 2 (START)--------########################################################
# phase2json = {"redirectTo": "https://www.google.com", "base64redirection": "aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbQ=="}
with open("phase2JSON.JSON") as f:
        phase2json = json.load(f)
###################################----Phase 2 (END)--------########################################################

###################################----Phase 3 (START)--------########################################################

def phase3():

    with open("input.json")as fs:
        inputjson = json.load(fs)
    dynamic_param = inputjson.get("dynamic_param")
    label = inputjson.get("label")
    sessK = ""
    phase3json = dict()

    with open("phase1JSON.JSON") as f:
        postGetJson = json.load(f)

    allLinks = postGetJson.keys()
    # allLinks = ["https://app2.com/user/files.php"]
    # print allLinks
    '''-----for each link login and then hit the link----'''

    for eachLink in allLinks:
        '''Fix for url without origin'''
        if "://" not in eachLink:
            #generalize this
            actionLink = origin+eachLink
            # actionLink = "https://app10.com/"+eachLink
        else:
            actionLink = eachLink

        payloadlist = postGetJson.get(eachLink)
        for payload in payloadlist:

            # Fill in your details here to be posted to the login form.
            formPayload = {form_username_name: form_username_value, form_password_name: form_password_value}

            # Use 'with' to ensure the session context is closed after use.
            with requests.Session() as s:
                #specific to app2 (generalize this)
                if login == "True":
                    p = s.post(login_page, data=formPayload, verify=False)
                    # p = s.post('https://app10.com', verify=False)

                    # print the html returned or something more intelligent to see if it's a successful login page.
                    # print p.text
                    #-------------------------------only for app2 - to get sess key (START)-------------------------------
                    # soup = BeautifulSoup(p.text)
                    # allA = soup.find_all('a')
                    # for indA in allA:
                    #     if indA.get('href') is not None:
                    #         if 'https://app2.com/login/logout.php?sesskey=' in indA.get('href'):
                    #             valA = indA.get('href').split('?')
                    #             print valA
                    #             if valA[0] == 'https://app2.com/login/logout.php':
                    #                 sessKsplit = valA[1].split('=')
                    #                 sessK = sessKsplit[1]
                    #                 break
                    if dynamic_param == "True":
                        soup = BeautifulSoup(p.text)
                        allA = soup.find_all('a')
                        for indA in allA:
                            if indA.get('href') is not None:
                                if label in indA.get('href'):
                                    u = indA.get('href')
                                    o = urlparse(u)
                                    paramdict = parse_qs(o.query)
                                    sessK = paramdict[label][0]
                                    print sessK
                                    break

                #-------------------------------only for app2 - to get sess key (END)-------------------------------
                '''*****************************get urls**************************'''
                if payload.get('type') == 'get':
                    # fuzzing the payload
                    for p in payload.keys():
                        temp = payload.get(p)
                        ##base64change##
                        vals = phase2json.values()
                        for redir in vals:
                            try:
                                falseCheck = payload.get(p)
                                if falseCheck is not None:
                                    if falseCheck.startswith("https://www.google"):
                                        pass
                                    else:
                                        payload[p] = redir
                                else:
                                    payload[p] = redir
                                #payload[p] = redir
                            ###
                                # payload[p] = phase2json.get("redirectTo")
                                #changing the session key
                                if label in payload.keys():
                                    payload[label] = sessK
                                payload.pop('type', None)
                                payload.pop('Location', None)
                                print "----------------------------------------------------------"
                                print eachLink, payload
                                # An authorised request
                                r = s.get(actionLink, params=payload, verify=False)
                                print r.url
                                #checking if its hitting google.com
                                if r.url.startswith("https://www.google.com"):
                                    payload["type"] = "get"
                                    # phase3json[actionLink] = dict(payload)
                                    key = actionLink
                                    if key in phase3json.keys():
                                        phase3json[key].append(dict(payload))
                                    else:
                                        phase3json[key] = [dict(payload)]
                                    ###
                                    with open("tempPhase3json.json", "w")as f:
                                        tempPhase3jsonString = json.dumps(phase3json, sort_keys=True, indent=8)
                                        f.write(tempPhase3jsonString)
                                    ###
                                payload[p] = temp
                            except Exception, e:
                                print e
                                continue

                    #for referer redirects
                    payload.pop('type', None)
                    payload.pop('Location', None)
                    print "---------------------------get - Referrer-------------------------------"
                    print eachLink, payload
                    # An authorised request
                    s.headers.update({"Referer": phase2json.get("redirectTo")})
                    if "page.php" in actionLink:
                        r = s.post(actionLink, data=payload, verify=False)
                    else:
                        r = s.get(actionLink, params=payload, verify=False)
                    print r.url
                    #checking if its hitting google.com
                    if r.url.startswith("https://www.google.com"):
                        payload["type"] = "get"
                        payload["Referer"] = phase2json.get("redirectTo")
                        # phase3json[actionLink] = dict(payload)
                        key = actionLink
                        if key in phase3json.keys():
                            phase3json[key].append(dict(payload))
                        else:
                            phase3json[key] = [dict(payload)]
                        ###
                        with open("tempPhase3json.json", "w")as f:
                            tempPhase3jsonString = json.dumps(phase3json, sort_keys=True, indent=8)
                            f.write(tempPhase3jsonString)
                        ###
                    s.headers.update({"Referer": None})

                '''***********************post urls***********************************'''
                if payload.get('type') == 'post':
                    #fuzzing the payload
                    for p in payload.keys():
                        temp = payload.get(p)
                        ##base64change##
                        vals = phase2json.values()
                        for redir in vals:
                            try:
                                falseCheck = payload.get(p)
                                if falseCheck is not None:
                                    if falseCheck.startswith("https://www.google"):
                                        pass
                                    else:
                                        payload[p] = redir
                                else:
                                    payload[p] = redir
                                #payload[p] = redir
                            ###
                                # payload[p] = phase2json.get("redirectTo")
                                #changing the session key
                                if label in payload.keys():
                                    payload[label] = sessK
                                payload.pop('type', None)
                                payload.pop('Location', None)
                                print "----------------------------------------------------------"
                                print eachLink, payload
                                # An authorised request
                                r = s.post(actionLink, data=payload, verify=False)
                                print r.url, payload
                                #checking if its hitting google.com
                                if r.url.startswith("https://www.google.com"):
                                    payload["type"] = "post"
                                    # phase3json[actionLink] = dict(payload)
                                    key = actionLink
                                    if key in phase3json.keys():
                                        phase3json[key].append(dict(payload))
                                    else:
                                        phase3json[key] = [dict(payload)]
                                    ###
                                    with open("tempPhase3json.json", "w")as f:
                                        tempPhase3jsonString = json.dumps(phase3json, sort_keys=True, indent=8)
                                        f.write(tempPhase3jsonString)
                                    ###
                                payload[p] = temp
                            except Exception, e:
                                print e
                                continue

                    #for referer redirects
                    payload.pop('type', None)
                    payload.pop('Location', None)
                    print "---------------------------post - Referrer-------------------------------"
                    print eachLink, payload
                    # An authorised request
                    s.headers.update({"Referer": phase2json.get("redirectTo")})
                    p = s.post(actionLink, data=payload, verify=False)
                    print p.url
                    #checking if its hitting google.com
                    if p.url.startswith("https://www.google.com"):
                        payload["type"] = "post"
                        payload["Referer"] = phase2json.get("redirectTo")
                        # phase3json[actionLink] = dict(payload)
                        key = actionLink
                        if key in phase3json.keys():
                            phase3json[key].append(dict(payload))
                        else:
                            phase3json[key] = [dict(payload)]
                        ###
                        with open("tempPhase3json.json", "w")as f:
                            tempPhase3jsonString = json.dumps(phase3json, sort_keys=True, indent=8)
                            f.write(tempPhase3jsonString)
                        ###
                    s.headers.update({"Referer": None})

                # #for referer redirects
                # payload.pop('type', None)
                # payload.pop('Location', None)
                # print "---------------------------get - Referrer-------------------------------"
                # print eachLink, payload
                # # An authorised request
                # s.headers.update({"Referer": phase2json.get("redirectTo")})
                # r = s.get(actionLink, params=payload, verify=False)
                # p = s.post(actionLink, data=payload, verify=False)
                # print r.url
                # print p.url
                # #checking if its hitting google.com
                # if r.url.startswith("https://www.google.com") or p.url.startswith("https://www.google.com"):
                #     payload["type"] = "get"
                #     payload["Referer"] = phase2json.get("redirectTo")
                #     # phase3json[actionLink] = dict(payload)
                #     key = actionLink
                #     if key in phase3json.keys():
                #         phase3json[key].append(dict(payload))
                #     else:
                #         phase3json[key] = [dict(payload)]
                # s.headers.update({"Referer": None})


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
        # p = s.post('https://app2.com/login/index.php', data=formPayload, verify=False)
        # soup = BeautifulSoup(p.text)
        # allA = soup.find_all('a')
        # for indA in allA:
        #     if indA.get('href') is not None:
        #         valA = indA.get('href').split('?')
        #         if valA[0] == 'https://app2.com/login/logout.php':
        #             sessKsplit = valA[1].split('=')
        #             sessK = sessKsplit[1]
        #             break

        print sessK
        payload = {
                        "AXSRF_token": "",
                        "Referer": "https://www.google.com",
                        "cmd": "send",
                        "contact_us": "0",
                        "email": "",
                        "friend_email": "",
                        "friend_name": "",
                        "item_id": "0",
                        "name": "",
                        "type": "post",
                        "visual": ""
                }
        s.headers.update({"Referer":"https://www.google.com"})
        r = s.post('http://app10.com/tell.php', data=payload, verify=False, allow_redirects=True)
        print r.text
        print r.url



def app10TestUnit():
    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        para = {
                        "Location": "Referer",
                        "dest": "",
                        "name": "",
                        "type": "post"
                }
        para.pop("Referer", None)
        para.pop("type", None)
        s.headers.update({"Referer": "https://www.google.com"})
        r = s.get("http://bm1.com/test1.php", params=para)
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
    with open("phase1JSON.JSON", 'w') as f:
        f.write(postreq_json)

    print postreq_json
    with open("phase1JSON.JSON") as f:
        postGetJson = json.load(f)
    # val = postGetJson["https://app2.com/tag/manage.php"]




    # postreq_json = postreq_json
    # print json.dumps(postreq_json, sort_keys=True, indent=8)


def phase1test():
    print "here"
    postreq_dict = dict()
    with open("newPost.txt", 'r') as f:
        # postreq_content = f.readlines()
        forloop = f.readlines()
    # print postreq_content
    # forloop = postreq_content.split("$eof$")
    # forloop.pop()
    for eachpost in forloop:
        postreq_split = eachpost.split("=!=")
        temp_str = postreq_split[1]
        evalStr = ast.literal_eval(temp_str)
        key = postreq_split[0]
        # postreq_dict.setdefault(key, [])
        if key in postreq_dict.keys():
            postreq_dict[key].append(evalStr)
        else:
            postreq_dict[key] = [evalStr]
    jsonString = json.dumps(postreq_dict, sort_keys=True, indent=8)
    print jsonString

###############################----test units(END)------#################################################

def phase1():
    json1 = getParams()
    json2 = post_params()
    z = json1.copy()
    z.update(json2)
    jsonString = json.dumps(z, sort_keys=True, indent=8)
    try:
        if os.path.exists("phase1JSON.JSON"):
            os.remove("phase1JSON.JSON")
    except OSError:
            pass
    with open("phase1JSON.JSON", 'w') as f:
        f.write(jsonString)
    print jsonString


##########################--Main(start)---###############################################

if __name__ == '__main__':
    with open("input.json")as f:
        inputjson = json.load(f)
    origin = inputjson.get("origin") #please provide the "/" (forward slash) at the end
    login_page = inputjson.get("login_page")
    #form parameters
    form_username_name = inputjson.get("form_username_name")
    form_username_value = inputjson.get("form_username_value")
    form_password_name = inputjson.get("form_password_name")
    form_password_value = inputjson.get("form_password_value")
    login = inputjson.get("login") #False - if login not needed (for app10.com - login not required)

    phase1()
    phase3()

##########################--Main(end)----###############################################
