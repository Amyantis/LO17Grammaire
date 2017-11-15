from antlr4 import CommonTokenStream, InputStream

from gen.GrammaireSQLLexer import GrammaireSQLLexer
from gen.GrammaireSQLParser import GrammaireSQLParser
from src.check_spell import Lexicon, get_lexicon


def make_sql_request(tree):
    if tree.SELECT():
        sql = 'SELECT DISTINCT * FROM'.split(' ')
    if tree.COUNT():
        sql = 'SELECT COUNT(*) FROM'.split(' ')
    if tree.ARTICLE() is not None:
        sql.append('article')
    if tree.BULLETIN() is not None:
        sql.append('bulletin')
    if tree.MOT() and tree.ps:
        sql += 'WHERE titre LIKE'.split(' ')
        if tree.ps.par1 is not None:
            sql.append('"%' + tree.ps.par1.a.text + '%"')
        if tree.ps.par2 is not None:
            conj = str(tree.ps.CONJ()[0])
            if conj == 'et':
                sql.append('AND')
            if conj == 'ou':
                sql.append('OR')
            sql.append('"%' + tree.ps.par2.a.text + '%"')
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
        # todo let user should which lemma use?
        return lemma[0]
    return lemma


def lemmatisate_expression(lexicon, expression):
    return " ".join(lemmatisate_word(lexicon, word) for word in expression.split(" "))


if __name__ == '__main__':
    with open('stoplist.txt') as fdesc:
        stoplist = set(fdesc.read().split('\n'))

    lexicon = Lexicon(get_lexicon())

    request_natural = "Combien d'articles parlent de la chine"
    print("Natural input request:\n\t", request_natural)

    request_natural = request_natural.lower()
    request_natural = " ".join(request_natural.split("'"))

    request_natural = apply_stoplist(stoplist, request_natural)
    print("Stoplisted natural input request:\n\t", request_natural)
    request_natural = lemmatisate_expression(lexicon, request_natural)
    print("Stoplisted and lemmatisated natural input request:\n\t", request_natural)

    sql = convert_natural_to_sql(request_natural)
    print(sql)
