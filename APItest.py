#OPSkins Test API
#https://opskins.com/api/user_api.php?request=GetActiveSales&key=abcde
#OPSkins API Documentations v1 = https://opskins.com/?loc=api_docs
#OPSkins API Documentation v2 = https://opskins.com/kb/api-v2

import requests
import sys
import config as cfg
import json


OPSkins_APIKey = cfg.OPSkins_APIKey




OPSkinsAPIKeyTest = "https://opskins.com/api/user_api.php?request=test&key=%s" % OPSkins_APIKey
response = requests.get(OPSkinsAPIKeyTest)



class APIError(Exception):
    #pass
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "Status {}: \"{}\". Please double check your key is correct".format(self.status,ErrorMessage)

def throws():
    raise APIError(response.status_code)

def main():
    try:
        throws()
        return 0
    except Exception,err:
        if response.status_code != 200:
            if response.status_code == 401:
                ErrorMessage = response.json()['result']['error']
            sys.stderr.write(str(err))
            return 1
        else:
            print response.status_code
#
# def APIKeyTest():
#     response = requests.get(OPSkinsAPIKeyTest)
#     status_code = response.status_code
#     print response.status_code
#     # print response.headers
#     if response.status_code != 200:
#         raise APIError(status_code)
#
# APIKeyTest()
if __name__ == '__main__':
    sys.exit(main())
