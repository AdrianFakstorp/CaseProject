
class APIError(Exception):
    #pass
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "Status {}. Please double check your key is correct".format(self.status)

def throws():
    raise APIError(Exception)

throws()
