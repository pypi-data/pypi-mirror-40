class FastDic(Translator):
    """Download the meaning of WORD from http://fastdic.com/word"""
    def __init__(self, word):
        super().__init__(self, word)
        self.name = "FastDic"
        self.url = "https://fastdic.com/word/"

    def parse_data(self, word):
        response = self._get_data(word)
        if response:
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
        return {}

