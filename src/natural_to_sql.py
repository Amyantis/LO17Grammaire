from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker

from gen.GrammaireSQLLexer import GrammaireSQLLexer
from gen.GrammaireSQLParser import GrammaireSQLParser
from src.Database import DataBase
from src.GrammaireSQLListener import GrammaireSQLListener
from src.Preformatter import Preformatter


def convert_natural_to_sql(request_natural: str):
    input_stream = InputStream(request_natural)
    lexer = GrammaireSQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammaireSQLParser(stream)
    tree = parser.requete()

    sql_listener = GrammaireSQLListener()
    walker = ParseTreeWalker()
    walker.walk(sql_listener, tree)

    return sql_listener.sql_request


def main():
    preformatter = Preformatter()
    db = DataBase()

    while True:
        request_natural = input("Question en langage naturel:")
        preformatted_request = preformatter.preformat(request_natural)
        sql = convert_natural_to_sql(preformatted_request)
        print(sql)
        if bool(input("Apply query?")):
            db.execute(sql)


if __name__ == '__main__':
    main()
