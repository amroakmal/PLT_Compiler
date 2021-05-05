

class Keywords:
    def __init__(self, keywords: str):
        # holds keywords separated by space
        self.keywords = keywords.split(" ")

    def addRule(self, store):
        for keyword in self.keywords:
            if keyword != "":
                store.addKeyword(keyword)
