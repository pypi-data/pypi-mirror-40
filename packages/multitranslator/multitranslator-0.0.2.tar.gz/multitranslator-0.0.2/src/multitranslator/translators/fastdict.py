import os

from .translator import Translator


class Fastdict(Translator):
    """Download the meaning of WORD from http://fastdic.com/word"""
    def __init__(self, params={}, headers={}):
        super().__init__(params, headers)
        self.name = "fastdic"
        self.base_url = "https://fastdic.com"

    def initialize_url(self):
        self.new_url = os.path.join(self.base_url, 'word', word)

    def parse_data(self, word):
        if response is None:
            return {}
        soup = BeautifulSoup(response, 'lxml')
        meaning = soup.find_all('ul', {'class': ['result', 'js-result']})
        if meaning:
            meaning = BeautifulSoup(str(meaning), 'lxml')
            for span in meaning.find_all('span'):
                span.extract()
            meaning = meaning.select('li')[0].getText()
            meaning = str(meaning).strip().split('\n')
            mean = str(meaning[0]).split('،')
            return {'Persian_Mean': mean}
