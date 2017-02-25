import json

def caseList():
    caseListLocation = "jsonCase Storage/List of Cases.json"
    with open(caseListLocation, "r") as case_list:
        caseList = json.load(case_list)
    return caseList

caseList = caseList()

def caseListName():
    NameList = []
    for caseData in caseList["List"]:
        caseName = caseData["Name"]
        NameList.append(caseName)
    return NameList

caseListName = caseListName()
