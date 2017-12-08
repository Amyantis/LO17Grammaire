from src import logger
from src.Lexicon import Lexicon


class StopList:
    def __init__(self) -> None:
        self.stoplist = StopList.get_stoplist()

    def apply_stoplist(self, s):
        return " ".join(word for word in s.split(" ") if word not in self.stoplist)

    @staticmethod
    def get_stoplist():
        with open('ressources/stoplist.txt') as fdesc:
            stoplist = set(fdesc.read().split('\n'))
        return stoplist


class Preformatter:
    def __init__(self) -> None:
        self.stoplist = StopList()
        self.lexicon = Lexicon()

        self.request_struct_dict = Preformatter.get_request_struct_dict()
        self.request_param_dict = Preformatter.get_request_param_dict()

    def preformat(self, natural_request):
        logger.debug("Natural input request:\n\t%s", natural_request)

        pref_req = natural_request.lower()
        pref_req = pref_req.replace("'", " ")
        pref_req = pref_req.replace("’", " ")
        pref_req = pref_req.replace(".", " ")
        pref_req = pref_req.replace("?", " ")
        pref_req = pref_req.replace("!", " ")
        pref_req = pref_req.replace("-", " ")
        pref_req.strip()

        pref_req = self.stoplist.apply_stoplist(pref_req)
        logger.debug("Stoplisted natural input request:\n\t%s", pref_req)

        pref_req, lemmas_choices = self.clean_expression(pref_req)
        logger.debug("Stoplisted and lemmatisated natural input request:\n\t%s", pref_req)

        return pref_req, lemmas_choices

    def clean_expression(self, natural_request):
        has_found_structure_word = set()

        lemmas_choices = {}

        l = []
        for word in natural_request.split(" "):
            tmp_word = word

            if tmp_word in self.request_param_dict:
                continue

            if tmp_word in self.request_struct_dict:
                word_found = self.request_struct_dict[tmp_word]
                if word_found not in has_found_structure_word:
                    tmp_word = word_found
                    has_found_structure_word.add(word_found)
            else:
                tmp_word = self.lemmatisate_word(tmp_word)
                if isinstance(tmp_word, list):
                    if word in tmp_word:
                        lemmas_choices[word].append(tmp_word)
                    else:
                        lemmas_choices[word] = tmp_word
                    tmp_word = tmp_word[0]

                if tmp_word in self.request_struct_dict:
                    word_found = self.request_struct_dict[tmp_word]
                    if word_found not in has_found_structure_word:
                        tmp_word = word_found
                        has_found_structure_word.add(tmp_word)
            l.append(tmp_word)

        return " ".join(l), lemmas_choices

    def lemmatisate_word(self, word, choice=False):
        lemma = self.lexicon.get(word)
        if lemma is None:
            return word
        if choice and isinstance(lemma, list):
            # let the user choose the lemma he wants
            while True:
                s = "Select a word in the following list of lemmas for word %s:\n\t%s\n"
                choice = input(s % (word, lemma))
                choice.strip()
                choice.lower()
                for l in lemma:
                    if choice == l:
                        return l
                print("Unknown choice", choice)
        return lemma

    @staticmethod
    def get_request_struct_dict():
        with open("ressources/structure_lexique.txt") as fdesc:
            structure_words = [line.replace("\n", "").split(" ") for line in fdesc.readlines()]
            d = {}
            for list_of_words in structure_words:
                for word in list_of_words:
                    d[word] = list_of_words[0]
        return d

    @staticmethod
    def get_request_param_dict():
        with open('ressources/known_param_lexique.txt') as fdesc:
            known_param = set(fdesc.read().split('\n'))
        return known_param


if __name__ == "__main__":
    # Testing the Preformatter with some requests
    requests = [
        # "Afficher les articles plus vieux que 2013.",
        # "Articles parlant d'innovation.",
        # "Donner les articles parus en 2011.",
        # "Donnez moi les articles sur le diabète",
        "Je veux les articles qui parlent de « l’innovation ».",
        "Je veux les articles qui parlent de Zuckerberg.",
        "Je veux les articles qui ont été écrits en mai 2011.",
    ]

    preformatter = Preformatter()

    for r in requests:
        s = preformatter.preformat(r)
        print(r, s, sep="\n")
        print()
