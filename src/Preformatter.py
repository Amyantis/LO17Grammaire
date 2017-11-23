from src import logger
from src.check_spell import Lexicon


class StopList:
    def __init__(self) -> None:
        self.stoplist = StopList.get_stoplist()

    def apply_stoplist(self, s):
        return " ".join(word for word in s.split(" ") if word not in self.stoplist)

    @staticmethod
    def get_stoplist():
        with open('../ressources/stoplist.txt') as fdesc:
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
        pref_req = " ".join(pref_req.split("'"))
        pref_req = " ".join(pref_req.split("’"))

        pref_req = self.stoplist.apply_stoplist(pref_req)
        logger.debug("Stoplisted natural input request:\n\t%s", pref_req)

        pref_req = self.clean_expression(pref_req)
        logger.debug("Stoplisted and lemmatisated natural input request:\n\t%s", pref_req)

        return pref_req

    def clean_expression(self, natural_request):
        has_found_structure_word = False

        l = []
        for word in natural_request.split(" "):
            if word in self.request_param_dict:
                continue
            if not has_found_structure_word and word in self.request_struct_dict:
                word = self.request_struct_dict[word]
                has_found_structure_word = True
            else:
                word = self.lemmatisate_word(word)
                if not has_found_structure_word and word in self.request_struct_dict:
                    word = self.request_struct_dict[word]
                    has_found_structure_word = True
            l.append(word)

        return " ".join(l)

    def lemmatisate_word(self, word):
        lemma = self.lexicon.get(word)
        if lemma is None:
            return word
        if isinstance(lemma, list):
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
        with open("../ressources/structure_lexique.txt") as fdesc:
            structure_words = [line.split(" ") for line in fdesc.readlines()]
            d = {}
            for list_of_words in structure_words:
                for word in list_of_words:
                    d[word] = list_of_words[0]
        return d

    @staticmethod
    def get_request_param_dict():
        with open('../ressources/known_param_lexique.txt') as fdesc:
            known_param = set(fdesc.read().split('\n'))
        return known_param


if __name__ == "__main__":
    # Testing the Preformatter with some requests
    requests = [
        "Afficher les articles plus vieux que 2013.",
        "Articles parlant d'innovation.",
        "Donner les articles parus en 2011.",
        "Donnez moi les articles sur le diabète",
    ]

    preformatter = Preformatter()

    for r in requests:
        s = preformatter.preformat(r)
        print(r, s, sep="\n")
        print()
