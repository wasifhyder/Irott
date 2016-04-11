import requests

class Word:
    def __init__(self, word, cefr="UN"):
        self.word = word
        self.cefr = cefr
        self.definitions = []

    def get_info_from_wordsapi(self):
        data = requests.get("https://wordsapiv1.p.mashape.com/words/{}".format(self.word),
                            headers={
                                "X-Mashape-Key": "sx1YoqZFawmshWoLaBGC5HuzdRx4p1UrtDRjsn1RYC97zNwy8K",
                                "Accept": "application/json"
                            })

        data = data.json().get('results')

        if data:
            for definition_data in data:
                self.definitions.append(Definition(definition_data))

    def __repr__(self):
        return "<Word: {:12}>".format(self.word)

class Definition:
    def __init__(self, definition_data):
        self.definition = definition_data.get('definition')
        self.examples = definition_data.get('examples')
        self.synonyms = definition_data.get('synonyms')
        self.antonyms = definition_data.get('antonyms')
        self.also = definition_data.get('also')
        self.entails = definition_data.get('entails')
        self.hasCategories = definition_data.get('hasCategories')
        self.hasInstances = definition_data.get('hasInstances')
        self.hasMembers = definition_data.get('hasMembers'),
        self.hasParts = definition_data.get('hasParts'),
        self.hasSubstances = definition_data.get('hasSubstances'),
        self.hasTypes = definition_data.get('hasTypes'),
        self.hasUsages = definition_data.get('hasUsages'),
        self.inCategory = definition_data.get('inCategory'),
        self.inRegion = definition_data.get('inRegion'),
        self.typeOf = definition_data.get('typeOf'),
        self.instanceOf = definition_data.get('instanceOf'),
        self.partOf = definition_data.get('partOf'),
        self.regionOf = definition_data.get('regionOf'),
        self.pertainsTo = definition_data.get('pertainsTo'),
        self.similarTo = definition_data.get('similarTo'),
        self.substanceOf = definition_data.get('substanceOf'),
        self.usageOf = definition_data.get('usageOf')

    def __repr__(self):
        return "{}".format(self.definition)

if __name__ == "__main__":
    rage = Word("anything")
    rage.get_info_from_wordsapi()
    print(rage.definitions)
    pass
