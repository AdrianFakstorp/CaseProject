import json

with open("jsonCase Storage/List of Cases.json", "r") as case_list:
    caseList = json.load(case_list)

for i in caseList["List"]:
    print i["Name"]
