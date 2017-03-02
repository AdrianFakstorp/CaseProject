# -*- coding: utf-8 -*-
import requests
import json
import config as cfg
import time
import os.path


#Functions Defined ---------

#Error Return Functions
def checkCaseListfromJson():
    existCheck = os.path.exists("%s/List of Cases.json" % cfg.jsonSource)
    if existCheck != True:
        print "\"List of Cases\" could not be found in the \"%s\" folder of your directory. Please check your config file." % cfg.jsonSource
        return False

checkCaseListfromJson()

#Main Functions
def getCaseListfromJson():
    caseListLocation = "%s/List of Cases.json" % cfg.jsonSource
    with open(caseListLocation, "r") as case_list:
        caseList = json.load(case_list)
    return caseList

def putCaseNameinList():
    NameList = []
    for caseDataIterated in caseData["List"]:
        caseName = caseDataIterated["Name"]
        NameList.append(caseName)
    return NameList

def getSkinsinCase(CaseName):
    ListofSkinNames = []
    desiredCase = "%s/%s.json" % (cfg.jsonSource,CaseName)
    with open(desiredCase, "r") as SkinsinCase:
        ListofSkinsinCase = json.load(SkinsinCase)
    ListofSkinsinCase = ListofSkinsinCase[CaseName]
    for SkinName in ListofSkinsinCase:
        SkinName = SkinName.encode('utf-8')
        ListofSkinNames.append(SkinName)
    return ListofSkinNames

def formatListofSkinNames(ListofSkinNames):
    jsontoPost = {}
    items = []
    for SkinName in ListofSkinNames:
        temp_dict = {}
        temp_dict['market_name'] = SkinName
        items.append(temp_dict)
    jsontoPost['items'] = items
    return jsontoPost

def postListofSkinNamestoPricingAPI(FormattedListofSkinNames):
    url = cfg.API_KEY
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(FormattedListofSkinNames), headers=headers)
    #print(response.status_code)
    #print(response.json())
    API_Response = response.json()
    return API_Response['data']

def caseDataUpdate_Formatting(PricedSkins, CaseName):
    caseBase = {}
    caseComplete = {}
    #Name & Date of Case
    Date = {"Date" : (time.strftime("%d/%m/%Y")), "Time": (time.strftime("%H:%M:%S"))}
    caseComplete["Last Update"] = Date
    #Skins with Price
    for Skin in PricedSkins:
        caseBase[Skin['market_name']] = Skin['price']
    caseComplete[CaseName] = caseBase
    return caseComplete

def caseDataUpdate_Write(CaseJSONFormatted, CaseName):
    jsonName = "%s/%s.json" % (cfg.jsonSource,CaseName)
    with open (jsonName, 'w') as outfile:
        json.dump(CaseJSONFormatted, outfile)

def CaseUpdateAll(caseNameList):
    for CaseName in caseNameList:
        print "%s parsing..." % CaseName
        ListofSkinNames = getSkinsinCase(CaseName)
        FormattedListofSkinNames = formatListofSkinNames(ListofSkinNames)
        PricedSkins = postListofSkinNamestoPricingAPI(FormattedListofSkinNames)
        CaseJSONFormatted = caseDataUpdate_Formatting(PricedSkins,CaseName)
        caseDataUpdate_Write(CaseJSONFormatted,CaseName)
        print "%s updated \n" % CaseName

#Main Functions Called
caseData = getCaseListfromJson()
caseNameList = putCaseNameinList()
CaseUpdateAll(caseNameList)
