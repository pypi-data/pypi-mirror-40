from . import Cambridge, Fastdict


class MultiTranslator:
    def __init__(self, word):
        self.dictionaries = [
            Cambridge,
            Fastdict,
        ]

    def search(self, word):
        word = word.lower()
        data_from_db = db_api.load_form_db(word)
        results = {}
        for dictionary in self.dictionaries:
            results = self._translate(dictionary, word, results) 
        return results

    def _translate(self, dictionary, word, results):
        results[my_dict.name] = my_dict.parse_data(word)
        return results
