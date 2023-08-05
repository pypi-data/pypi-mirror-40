from abc import ABCMeta, abstractmethod

import requests


class Translator(metaclass=ABCMeta):
    """ Base Translator class """ 
    def __init__(self, src=None, dst=None, headers={}):
        self.name = ""
        self.url = ""
        self.src = src
        self.dst = dst
        self.headers = headers

    def tranlsate(self, text):
        self.text = text
        self.initialize_url()
        self.get_data()
        self.parse_data()

    @abstractmethod
    def initialize_url(self):
        url = self.url
        self.new_url = self.url + self.word

    @abstractmethod
    def get_data(self, word):
        response = requests.get(self.new_url, headers = self.headers)
        if response.status_code == requests.codes.ok:
            return response.text

    @abstractmethod
    def parse_data(self):
        pass

    def to_dict(self, filename, link):
        pass
