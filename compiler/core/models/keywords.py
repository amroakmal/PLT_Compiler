

class Keywords:
    def __init__(self, keywords: str):
        # holds keywords separated by space
        self.keywords = keywords.split(" ")

    def add_rule(self, store):
        for keyword in self.keywords:
            if keyword != "":
                store.add_keyword(keyword)
