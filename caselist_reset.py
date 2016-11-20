import json
list_of_cases = {"List":[]}

with open("jsonCase Storage/List of Cases.json", 'w') as json_file:
    json.dump(list_of_cases, json_file)
