from src import logger


class Lexicon():
    def __init__(self, lines=None):
        # word => lemma
        if lines is None:
            lines = Lexicon.get_lexicon()
        self.lexicon = {line[0].strip(): line[1].strip() for line in lines}
        self.proximity_threshold = 80
        self.proximity_letters_threshold = 3
        self.levenshtein_distance_threshold = 1

    def get(self, word):
        lemma = self.lexicon.get(word.lower())

        if lemma is None and len(word) > 2:
            # compute proximities
            candidates = \
                {lemma_: self.proximity(word, lexicon_word)
                 for lexicon_word, lemma_ in self.lexicon.items()}
            candidates = \
                Lexicon.filter_candidates(self.proximity_threshold, candidates)
            if len(candidates) > 0:
                logger.info("Used proximity percentage for `%s`", word)
                return candidates

            # compute levenshtein distance
            candidates = \
                {lemma_: Lexicon.levenshtein_distance(word, lexicon_word)
                 for lexicon_word, lemma_ in self.lexicon.items()}
            candidates = {lemma: dist
                          for lemma, dist in candidates.items() if dist > 0}
            candidates = \
                Lexicon.filter_candidates(self.levenshtein_distance_threshold, candidates, False)
            if len(candidates) > 0:
                logger.info("Used levenshtein for `%s`", word)
                return candidates

        return lemma

    def proximity(self, word1, word2):
        # percent of identical letters
        if len(word1) < self.proximity_letters_threshold and len(
                word2) < self.proximity_letters_threshold:
            return 0
        if abs(len(word1) - len(word2)) > self.proximity_letters_threshold:
            return 0

        i = 0
        while i < min(len(word1), len(word2)) and word1[i] == word2[i]:
            i += 1

        return i * 100 / max(len(word1), len(word2))

    @staticmethod
    def levenshtein_distance(s1, s2, insertion_cost=1, deletion_cost=1, substitution_cost=1, verbose=False):
        if len(s1) < len(s2):
            return Lexicon.levenshtein_distance(s2, s1, insertion_cost, deletion_cost, substitution_cost, verbose)
        # s2 < s1

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))

        for i, c1 in enumerate(s1):
            current_row = [i + 1]

            for j, c2 in enumerate(s2):
                # j+1 instead of j since previous_row and current_row are one character longer than s2
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)

                d1 = insertions * insertion_cost
                d2 = deletions * deletion_cost
                d3 = substitutions * substitution_cost

                current_row.append(min(d1, d2, d3))
            previous_row = current_row

        return previous_row[-1]

    @staticmethod
    def filter_candidates(threshold, candidates, superior=True):
        max_distance = threshold
        lemmas = []
        for lemma_, distance in candidates.items():
            if superior and distance > max_distance:
                max_distance = distance
                lemmas = [lemma_]
            if not superior and distance < max_distance:
                max_distance = distance
                lemmas = [lemma_]
            if distance == max_distance:
                lemmas.append(lemma_)
        return lemmas

    @staticmethod
    def get_lexicon():
        with open('../ressources/filtre_corpus.txt') as fdesc:
            file = fdesc.read()
        return [line.split('\t') for line in file.split('\n') if len(line.split('\t')) == 2]


if __name__ == '__main__':
    lexicon = Lexicon()
    word = None
    while word != '':
        word = input().strip()
        lemma = lexicon.get(word)
        if lemma is None:
            print(word, "inconnu du lexique")
        else:
            print(word, lemma, sep=":\t")
