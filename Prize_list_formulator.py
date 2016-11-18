# -*- coding: utf-8 -*-
import json
import pprint
import random
import sys
import re
pp = pprint.PrettyPrinter(indent=4)


#TO Do List:
# -option to try a different iteration
# -consider having knife json


with open("jsonCase Storage/List of Cases.json", "r") as case_list:
    caseList = json.load(case_list)

with open("jsonCase Storage/price_ranking.json", "r") as price_list:
    listPrizeBrackets = json.load(price_list)

def getCaseInput():
    sorted_caseList = sorted(caseList['List'])
    for case in sorted_caseList: #To diplay to user what cases are available for selection
        print case
    caseMatch = False
    while caseMatch == False:
        desiredCase = raw_input("From the list above, please enter which case you would like to use: ")
        if desiredCase == "end":
            print "Ending Program"
            sys.exit()
        for case in sorted_caseList:
            lowerDesired = desiredCase.lower()
            lowerCase = case.lower()
            if lowerCase.startswith(lowerDesired):
                caseMatch = True
                casePrint = case
        if caseMatch == True:
            print "You have selected %s" % casePrint
            return casePrint
        else:
            print "Your input does not match with any of the cases listed."

def getValueInput():
    sortedValueList = listPrizeBrackets["Prizes"]
    for value in sortedValueList:
        print value
    valueMatch = False
    while valueMatch == False:
        desiredValue = raw_input("From the list above, please enter which case you would like to use: ")
        if desiredValue == "end":
            print "Ending Program"
            sys.exit()
        for value in sortedValueList:
            lowerDesired = desiredValue.lower()
            lowerValue = value.lower()
            if lowerValue.startswith(lowerDesired):
                valueMatch = True
                valuePrint = value
        if valueMatch == True:
            print "You have selected %s" % valuePrint
            return valuePrint
        else:
            print "Your input does not match with any of the prizing tiers listed."


case = getCaseInput()
value = getValueInput()
case_path = "jsonCase Storage/%s.json" % case
roomForError = 0.1




with open(case_path, "r") as case_json:
    active_case = json.load(case_json)


active_case = active_case[case]
list_of_prize_brackets = listPrizeBrackets["Prizes"][value][1]["Prize Ranking"]


def getBaseSkin(inputString):
    baseSkin = ""
    check = True
    stattrak = "StatTrak™ "
    inputString = inputString.encode('utf-8')
    while check == True:
        if "(" not in inputString:
            check = False
            return "Invalid Skin"
        if stattrak in inputString:
            inputString = re.sub("{0}".format(stattrak),"",inputString)
        for letter in inputString:
            if letter != "(":
                baseSkin += letter
            elif letter == "(":
                check = False
                return baseSkin

def SuitableSkinSelection(value,roomForError,caseUsed):
    #placement = {u'Rank': u'1', u'Value': 10.5}
    value = value * 100
    valueBottom = int(value - (value * roomForError))
    valueTop = int(value + (value * roomForError))
    SuitableSkins = []
    for skins in caseUsed:
        skinNameandValue = {}
        skinValue = (float(caseUsed[skins])*100)
        if skinValue in range(valueBottom, valueTop):
            skinNameandValue[skins] = skinValue/100
            SuitableSkins.append(skinNameandValue)
    return SuitableSkins

#SuitableSkinSelection = [{u'MAC-10 | Tatter (Factory New)': 1.3}, {u'XM1014 | Heaven Guard (Factory New)': 1.36}]

def interval_increase(value,roomForError,caseUsed):
    roomForError = roomForError
    SuitableSkins_Check = True
    while SuitableSkins_Check == True:
        skin_selection = SuitableSkinSelection(value,roomForError,caseUsed)
        if skin_selection == []:
            roomForError += .05
        else:
            SuitableSkins_Check = False
            return skin_selection
#interval_increase output = [{u'M4A1-S | Atomic Alloy (Factory New)': 9.0}]

def getmasterListSkins(masterList):
    listReturn = []
    #print masterList
    if masterList != []:
        for ranking in masterList:
            #print ranking
            for skin in ranking:
                skinLocale = ranking[skin]
                for name in skinLocale:
                    name = name
                #print skinLocale
                listReturn.append(name)
    else:
        listReturn = []
    return listReturn



def duplicateSkin_check(masterList,caseList):
    new_caseList = dict(caseList)
    masterListSkins = getmasterListSkins(masterList)
    for skin in caseList:
        for chosenSkin in masterListSkins:
            chosenBase = getBaseSkin(chosenSkin)
            chosencaseSkin = getBaseSkin(skin)
            #print skin
            #print chosenBase
            if chosencaseSkin.startswith(chosenBase):
                 del new_caseList[skin]
    return new_caseList




def createPrizeList(list_of_prize_brackets,roomForError,caseUsed):
    masterList = []
    for rankings in list_of_prize_brackets:
        caseUsed = duplicateSkin_check(masterList,caseUsed)
        skinSelected = {}
        rank = rankings['Rank']
        value = rankings['Value']
        ####rankings format= {u'Rank': u'7', u'Value': 2.75}
        interveralChecked_skinSelection = interval_increase(value,roomForError,caseUsed)
        ####totalChecked_skinSelection = duplicateSkin_check(interveralChecked_skinSelection,masterList)
        skinSelected[rank] = random.choice(interveralChecked_skinSelection)
        masterList.append(skinSelected)

    return masterList

def sumPrizeList(masterList):
    sumPrint = 0
    for prizeSet in masterList:
        for rank,skinSet in prizeSet.iteritems():
            for name,value in skinSet.iteritems():
                sumPrint += value
    return sumPrint

URLSymbols = {" ": "%20", "!":"%21", ":":"%3A",";":"%3B","|":"%7C"}

def linkConverter(masterList):
    listConverted = []
    for rankedSkin in masterList:
        for pricedSkin in rankedSkin:
            # pricedSkin = pricedSkin.encode('utf-8')
            for skin in rankedSkin[pricedSkin]:
                tempLetterList = []
                #format = https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Neon%20Revolution%20(Field-Tested) (AK-47 | Neon Revolution)
                for letter in skin:
                    #print letter
                    tempLetterList.append(letter)
                    for symbol in URLSymbols:
                        if letter == symbol:
                            letterIndex = tempLetterList.index(letter)
                            tempLetterList[letterIndex] = URLSymbols[symbol]
        newSkin = "".join(tempLetterList)
        newSkin = newSkin.encode('utf-8')
        listConverted.append(newSkin)
    return listConverted


def outputLinks(listConverted):
    linkList = []
    for skin in listConverted:
        #skin = skin.encode('utf-8')
        skinLink = ("https://steamcommunity.com/market/listings/730/" + skin)
        linkList.append(skinLink)
    return linkList

def writeLinks(masterList,outputLinks):
    file_name = "jsonCase Storage/outputLinks.txt"
    with open(file_name, "w") as file:
        file.write("")
    for skinValue in masterList:
        with open(file_name, 'a') as file:
            file.write("%s + \n" %skinValue)
    with open(file_name, "a") as file:
        file.write("Total Value: %s\n" %prizeSum)
        file.write("\n---------------------------------\n")
    for link in outputLinks:
        with open(file_name, 'a') as file:
            file.write(link + "\n")
    print "This list has been written to %s" %file_name

masterList = createPrizeList(list_of_prize_brackets,roomForError,active_case)
prizeSum = sumPrizeList(masterList)
pp.pprint(masterList)
listConverted = linkConverter(masterList)
outputLinks = outputLinks(listConverted)
writeLinks(masterList,outputLinks)
print "Your cost is %s" % prizeSum
