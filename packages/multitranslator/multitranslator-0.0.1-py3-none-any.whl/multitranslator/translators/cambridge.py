from bs4 import BeautifulSoup


class Cambridge(Translator):
    """Download the meaning of WORD from http://dictionary.cambridge.org/dictionary/english/ """

    def __init__(self):
        super().__init__(self, word)
        self.name = "cambridge"
        self.url = "http://dictionary.cambridge.org/dictionary/english/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        }
        self.results = {
                'Pronunciation': '', 'Definition': 'Not Found',
                'Part of speech': 'Not Found',
                }

    def parse_data(self, word):
        response = self._get_data(word)
        if response:
            soup = BeautifulSoup(response, 'lxml')

            part_of_speech = soup.find_all('span', {'class': 'pos'})[0].getText()
            if part_of_speech == 'idiom':
                # idiom means cambridge can't translate this word
                return {}

            elif part_of_speech == 'noun':
                countable = soup.find_all('span', {'class': 'gcs'})
                #part_of_speech = ""
                if countable:
                    part_of_speech += ' [%s]' % (countable[0].getText())

            uk_phonetic = soup.find_all('span', {'class': 'pron'})[0].getText()  # extract pronunciation
            us_phonetic = soup.find_all('span', {'class': 'pron'})[1].getText()  # extract pronunciation
            voices = soup.select('span[data-src-mp3]')  # get voice of us and uk accent

            if voices:
                #uk_audio = voices[0].attrs['data-src-mp3']
                us_audio = voices[1].attrs['data-src-mp3']
                #uk_voice =  self._save_binaries(uk_audio)
                us_voice =  self._save_binaries(word + '.mp3', us_audio)
                #self.results['uk-voice'] = uk_voice
            definition = soup.find_all('b', {'class': 'def'})[0].getText()\
                .replace('  ', ' ').title()
            self.results['Part of speech'] = part_of_speech
            self.results['Pronunciation'] = us_phonetic
            self.results['Definition'] = definition.replace(':', '')
            return self.results
        return {}
