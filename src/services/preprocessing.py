
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.stem import SnowballStemmer
import nltk
import spacy
import unicodedata


class Preprocessor():
    def __init__(self, language='english', language_code='en', bad_list=[], bad_root_list=[]):
        self.__stopwords = stopwords.words(language)
        self.__stemmer = SnowballStemmer(language)
        self.__lemm = spacy.blank(language_code)
        self.__bad_list = bad_list
        self.__bad_root = bad_root_list
        self.__tokens = []

    def set_text(self, text):
        self.__tokens = wordpunct_tokenize(text if text else '')
        return self

    def remove_accents(self):
        text = self.get_text()
        text = unicodedata.normalize(
            'NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        self.set_text(text)
        return self

    def standardize(self):
        self.__tokens = [word.lower() for word in self.__tokens if (
            word.isalnum() and not word.isnumeric())]
        self.__tokens = [
            word for word in self.__tokens if word not in self.__bad_list]
        return self

    def remove_stop_words(self):
        self.__tokens = [word for word in self.__tokens
                         if not word in self.__stopwords]
        return self

    def stemming(self):
        self.__tokens = [self.__stemmer.stem(
            word) for word in self.__tokens]
        return self

    def lemmatization(self):
        self.__tokens = [tokens.lemma_ for tokens in self.__lemm(
            ' '.join(word for word in self.__tokens))]
        return self

    def pipeline(self):
        self.standardize().remove_stop_words().lemmatization()
        return self

    def stemming_pipeline(self):
        self.standardize().remove_stop_words().stemming()
        return self

    def get_text(self):
        return ' '.join(word for word in self.__tokens if word not in self.__bad_root)

    def get_tokens(self):
        return self.__tokens
