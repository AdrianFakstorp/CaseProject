import json
import config as cfg
import pprint
pp = pprint.PrettyPrinter(indent=4)


case = "Chroma Case"

case_path = "%s/%s.json" % (cfg.jsonSource,case)

def caseUpdater(case_path):
    with open(case_path, "r") as case_json:
        active_case = json.load(case_json)
    for skin in active_case[case]:
        skin = skin.encode('utf-8')
        print skin

pp.pprint(caseUpdater(case_path))
