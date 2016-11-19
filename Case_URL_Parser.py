# -*- coding: utf-8 -*-
import requests
import urllib2
import json
from pprint import pprint
import sys
import time
import re
import config as cfg

tracer = "var g_rgAssets ="
tracer_name = "market_listing_item_name"
pipe   = "|"
wears  = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn']
case_list = []
case_complete = {}


def case_input():
    case_input = raw_input("Please enter the link of the case you wish to add: ")
    switch = False
    while switch == False:
        if case_input.startswith("https://steamcommunity.com/market/listings/730/"):
            switch = True
            return case_input
        else:
            case_input = raw_input("It seems that the URL you entered is not correct. Please try again and make sure it is a Steam link: ")
            switch = False

URL = case_input()



# run via
# python lines.py https://steamcommunity.com/market/listings/730/Huntsman%20Weapon%20Case

#Grabbins Skins and putting into array
def grab_name():
    response = urllib2.urlopen(URL.strip())
    page_source = response.read()
    page_source = page_source.strip()

    result = re.search('<span class="market_listing_item_name" style="">(.+)<\/span><br\/>', page_source)
    if result == None:
        print "The name of the case cannot be found. The source code may have changed. Please contact the program owner."
        quit()
    else:
        name = result.group(1)
        print "You have entered the URL for %s" % name
        return name


name = grab_name()


def skin_grab():
    response = urllib2.urlopen(URL.strip())
    page_source = response.read()
    page_source = page_source.strip()
    check = False
    temp_dict = {}
    skins_list = []
    json_list = {}

    for line in page_source.splitlines():
        if tracer in line.strip():
            # pprint("{" + line[line.find('"descriptions":[')  : line.find(']') + 1] + "}") # DEBUG
            data = json.loads("{" + line[line.find('"descriptions":[')  : line.find(']') + 1] + "}")

            for description in data['descriptions']:
                if pipe in description['value']:
                    for wear in wears :
                        stattrak = ("StatTrak™ ").decode('utf-8')
                        nonstattrak = ""
                        classifications = [nonstattrak,stattrak]
                        for types in classifications:
                            if types == nonstattrak:
                                case_list.append(description['value'] + " (" + wear + ")")
                                temp_dict["market_name"] = (description["value"] + " (" + wear + ")")
                                skins_list.append(temp_dict)
                                temp_dict = {}
                            elif types == stattrak:
                                case_list.append(description['value'] + " (" + wear + ")")
                                temp_dict["market_name"] = (stattrak + description["value"] + " (" + wear + ")")
                                skins_list.append(temp_dict)
                                temp_dict = {}
            check = True

    json_list["items"] = skins_list
    return json_list
    if check == False:
        print "The skins cannot be found. The source code may have changed. Please contact the program owner."




json_list = skin_grab()

def pricing_post():
    url = cfg.API_KEY
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(json_list), headers=headers)
    #print(response.status_code)
    #print(response.json())
    API_Response = response.json()
    return API_Response['data']

API_Response = pricing_post()
#print API_Response
#b = pricing_response.request
#print b.body

def case_creation():
    case = {}
    for skin in API_Response:
        case[skin['market_name']] = skin['price']
    return case

case = case_creation()
case_complete[name] = case
case_complete["Last Update"] = {"Date" : (time.strftime("%d/%m/%Y")), "Time": (time.strftime("%H:%M:%S"))}
#print case_complete

def case_json():

    json_name = "%s/%s.json" % (cfg.jsonSource,name)
    json_lists = (case_complete)
    with open(json_name, 'w') as outfile:
        json.dump(case_complete, outfile)
    #text = open(json_name, "w")
    #text
    #text.write("%s" % json_lists)

case_json()

####################################################################Creating List of Cases

def case_list_check(name):
    json_name = "%s/%s" % (cfg.jsonSource,cfg.caseList)
    with open(json_name, 'r') as json_file:
        list_of_cases = json.load(json_file)
    deep_list = list_of_cases["List"]
    check = 1
    for cases in deep_list:
        if name == cases:
            # print name
            # print case
            check = 0
        else:
            check = 1
    if check == 1:
        deep_list.append(name)
        print deep_list
        with open(json_name, 'w') as outfile:
            json.dump(list_of_cases, outfile)


case_list_check(name)
