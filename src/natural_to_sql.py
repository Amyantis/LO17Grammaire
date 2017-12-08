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

    return sql_listener.sql_request_tree.sql_request()


def main():
    # Small too to try natural requests
    preformatter = Preformatter()
    db = DataBase()

    while True:
        request_natural = input("Question en langage naturel:\n")
        preformatted_request = preformatter.preformat(request_natural)
        sql = convert_natural_to_sql(preformatted_request)
        print(sql)

        s = None
        while s not in {'yes', 'no'}:
            s = input("Apply query? (yes|no)\n").strip()

        if s == 'yes':
            i = 0
            for row in db.execute(sql):
                print(row)
                i += 1
                if i > 3:
                    print("...")
                    break
            if i == 0:
                "Nothing found!"
                continue

            s = None
            while s not in {'yes', 'no'}:
                s = input("Are you happy with that result? (yes|no)\n").strip()

            if s == 'yes':
                with open("success.txt", "a+") as fdesc:
                    fdesc.write(request_natural)
                    fdesc.write("\n")
                    fdesc.write(sql)
                    fdesc.write("\n")
if __name__ == '__main__':
    main()
