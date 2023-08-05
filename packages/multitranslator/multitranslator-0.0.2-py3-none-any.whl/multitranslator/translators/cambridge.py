import os

from bs4 import BeautifulSoup

from .translator import Translator


class Cambridge(Translator):
    """Download the Definition of a word from http://dictionary.cambridge.org/dictionary/english/ """
    def __init__(self, params={}, headers={}):
        super().__init__(params, headers)
        self.name = "cambridge"
        self.base_url = "http://dictionary.cambridge.org"

    def initialize_url(self):
        self.new_url = os.path.join(self.base_url, 'dictionary/english', self.text)

    def parse_data(self):
        self.result = {}
        if self.data is None:
            return {}
        soup = BeautifulSoup(self.data, 'lxml')
        part_of_speech = soup.find_all('span', {'class': 'pos'})[0].getText()
        if part_of_speech == 'idiom':
            return {} # idiom means cambridge can't translate this word
        elif part_of_speech == 'noun':
            countable = soup.find_all('span', {'class': 'gcs'})
            #part_of_speech = ""
            if countable:
                part_of_speech += ' [%s]' % (countable[0].getText())
        uk_phonetic = soup.find_all('span', {'class': 'pron'})[0].getText()
        us_phonetic = soup.find_all('span', {'class': 'pron'})[1].getText()

        voices = soup.select('span[data-src-mp3]')  # get voice of us and uk accent
        if voices:
            uk_audio = self.base_url + voices[0].attrs['data-src-mp3']
            us_audio = self.base_url + voices[1].attrs['data-src-mp3']
            self.result['uk_voice'] = uk_audio
            self.result['us_voice'] = us_audio
        definition = soup.find_all('b', {'class': 'def'})[0].getText() .replace('  ', ' ').title()
        self.result['part_of_speech'] = part_of_speech
        self.result['pronunciation'] = us_phonetic
        self.result['definition'] = definition.replace(':', '')
