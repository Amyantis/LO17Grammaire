from antlr4 import CommonTokenStream, InputStream

from gen.GrammaireSQLLexer import GrammaireSQLLexer
from gen.GrammaireSQLParser import GrammaireSQLParser
from src.check_spell import Lexicon, get_lexicon
from src.sql_request import DataBase


def make_sql_request(tree):
    if tree.SELECT():
        sql = 'SELECT DISTINCT * FROM'.split(' ')
    if tree.COUNT():
        sql = 'SELECT COUNT(*) FROM'.split(' ')
    if tree.ARTICLE() is not None:
        sql.append('titre')
    if tree.BULLETIN() is not None:
        sql.append('numero')
    if tree.MOT() or tree.WHEN():
        sql.append('WHERE')
    if tree.MOT() and tree.ps:
        sql += 'mot LIKE'.split(' ')
        if tree.ps.par1 is not None:
            sql.append("'%" + tree.ps.par1.a.text + "%'")
        if tree.ps.par2 is not None:
            conj = str(tree.ps.CONJ()[0])
            if conj == 'et':
                sql.append('AND')
            if conj == 'ou':
                sql.append('OR')
            sql.append("'%" + tree.ps.par2.a.text + "%'")
    if tree.WHEN():
        if tree.te.year_ is not None:
            digits = [tree.te.year_.digit1.text, tree.te.year_.digit2.text, tree.te.year_.digit3.text,
                      tree.te.year_.digit4.text]
            year = int("".join(digits))
            sql.append('year(annee)=%d' % year)
            # TODO: add other time of date
    sql.append(';')

    return ' '.join(sql)


def convert_natural_to_sql(request_natural: str):
    input_stream = InputStream(request_natural)
    lexer = GrammaireSQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammaireSQLParser(stream)
    tree = parser.requete()
    sql_request = make_sql_request(tree)
    return sql_request


def apply_stoplist(stoplist, s):
    return " ".join(word for word in s.split(" ") if word not in stoplist)


def lemmatisate_word(lexicon, word):
    lemma = lexicon.get(word)
    if lemma is None:
        return word
    if isinstance(lemma, list):
        # let the user choose the lemma he wants
        while True:
            s = "Select a word in the following list of lemmas for word %s:\n\t%s"
            choice = input(s % (word, lemma))
            choice.strip()
            choice.lower()
            for l in lemma:
                if choice == l:
                    return l
            print("Unknown choice", choice)
    return lemma


def clean_expression(lexicon, structure_lexicon, known_param_lexicon, expression):
    has_found_structure_word = False

    l = []
    for word in expression.split(" "):
        if word in known_param_lexicon:
            continue
        if not has_found_structure_word and word in structure_lexicon:
            word = structure_lexicon[word]
            has_found_structure_word = True
        else:
            word = lemmatisate_word(lexicon, word)
            if not has_found_structure_word and word in structure_lexicon:
                word = structure_lexicon[word]
                has_found_structure_word = True
        l.append(word)

    return " ".join(l)


def get_structure_lexicon():
    with open("structure_lexique.txt") as fdesc:
        structure_words = [line.split(" ") for line in fdesc.readlines()]
        d = {}
        for list_of_words in structure_words:
            for word in list_of_words:
                d[word] = list_of_words[0]
    return d


def get_stoplist():
    with open('stoplist.txt') as fdesc:
        stoplist = set(fdesc.read().split('\n'))
    return stoplist


def get_known_param_lexicon():
    with open('known_param_lexique.txt') as fdesc:
        known_param = set(fdesc.read().split('\n'))
    return known_param


def main():
    stoplist = get_stoplist()

    lexicon = Lexicon(get_lexicon())

    structure_lexicon = get_structure_lexicon()

    known_param_lexicon = get_known_param_lexicon()

    db = DataBase()

    while True:
        request_natural = input("Question en langage naturel:")
        print("Natural input request:\n\t", request_natural)

        request_natural = request_natural.lower()
        request_natural = " ".join(request_natural.split("'"))
        request_natural = " ".join(request_natural.split("’"))

        request_natural = apply_stoplist(stoplist, request_natural)
        print("Stoplisted natural input request:\n\t", request_natural)

        request_natural = clean_expression(lexicon, structure_lexicon, known_param_lexicon, request_natural)
        print("Stoplisted and lemmatisated natural input request:\n\t", request_natural)

        sql = convert_natural_to_sql(request_natural)
        print(sql)
        if bool(input("Apply query?")):
            db.execute(sql)


if __name__ == '__main__':
    main()
