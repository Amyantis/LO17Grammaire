# Generated from GrammaireSQL.g4 by ANTLR 4.5.3
from antlr4 import *
import calendar

# This class defines a complete listener for a parse tree produced by GrammaireSQLParser.
from gen.GrammaireSQLLexer import GrammaireSQLLexer
from gen.GrammaireSQLParser import GrammaireSQLParser


class LeftJoinElement:
    def __init__(self, table, field):
        self.table = table
        self.field = field

    def format_left_join(self, available_columns):
        for c in available_columns:
            column_name = c.split(".")[1]
            if column_name == self.field:
                return \
                    'LEFT JOIN {table} ON {table}.{field} = {joining_field}'. \
                        format(table=self.table, field=self.field, joining_field=c)
        raise Exception("%s not found in %s" % (self.field, available_columns))


class SQLRequestTree:
    def __init__(self):
        self.request_type = None
        self.columns = []
        self.tables = set()
        self.left_join_elements = []
        self.where_elements = []

    def sql_request(self):
        columns_set = set()
        columns_distinct = []

        for column in self.columns:
            column_name = column.split('.')[1]
            if column_name not in columns_set:
                columns_set.add(column_name)
                columns_distinct.append(column)

        if 'fichier' not in [col.split('.')[1] for col in columns_distinct]:
            columns_distinct.append('%s.fichier' % list(self.tables)[0])

        columns = sorted(columns_distinct,
                         key=lambda col: col.split('.')[1])

        columns = ["%s AS %s" % (column, column.split(".")[1])
                   for column in columns]

        if 'date' in {left_join_command.table for left_join_command in self.left_join_elements}:
            columns.append("CONCAT(TRIM(date.jour), ' / ', TRIM(date.mois), ' / ', TRIM(date.annee)) AS date")

        if self.request_type is not None and "COUNT" in self.request_type:
            columns = []

        if len(self.where_elements) > 0:
            where = ["WHERE", " AND ".join(self.where_elements)]
        else:
            where = []

        request_type = self.request_type
        if request_type is None:
            request_type = ""

        tables = self.tables
        for table_name in {col.split('.')[0] for col in columns_distinct}:
            tables.add(table_name)
        tables = sorted(tables)

        args = [
            "SELECT",
            request_type,
            ", ".join(columns),
            "FROM",
            ", ".join(tables),
            *self.format_left_join_commands(),
            *where
        ]
        return " ".join(args)

    def format_left_join_commands(self):
        sql = [left_join.format_left_join(self.columns) for left_join in self.left_join_elements]
        return " ".join(sql).split(" ")


class GrammaireSQLListener(ParseTreeListener):
    def __init__(self) -> None:
        super().__init__()
        self.sql_request_tree = SQLRequestTree()

    # Enter a parse tree produced by GrammaireSQLParser#requete.
    def enterRequete(self, ctx: GrammaireSQLParser.RequeteContext):
        if ctx.COUNT() is not None:
            self.sql_request_tree.request_type = "COUNT(*)"

        if ctx.type_ is None or ctx.SELECT() is not None:
            self.sql_request_tree.request_type = "DISTINCT"

        columns = []
        if ctx.type_ is None or ctx.type_.text == 'article':
            columns += [
                'texte.mot',
                'texte.rubrique',
                'texte.fichier',
                'texte.numero',
            ]
            self.sql_request_tree.tables.add("texte")

        if ctx.type_ is not None and ctx.type_.text == 'rubrique':
            columns += [
                'rubrique.rubrique',
                'rubrique.fichier',
                'rubrique.numero'
            ]
            self.sql_request_tree.tables.add("rubrique")

        if ctx.type_ is not None and ctx.type_.text == 'contact':
            columns += [
                'email.email',
                'email.fichier',
                'email.numero',
            ]
            self.sql_request_tree.tables.add("email")

        self.sql_request_tree.columns = columns

        if ctx.WHEN():
            left_join = LeftJoinElement('date', 'fichier')
            self.sql_request_tree.left_join_elements.append(left_join)

        if ctx.MOT() or len(ctx.params()) > 0:
            if "texte.mot" not in self.sql_request_tree.columns:
                left_join = LeftJoinElement('texte', 'fichier')
                self.sql_request_tree.left_join_elements.append(left_join)

    # Exit a parse tree produced by GrammaireSQLParser#requete.
    def exitRequete(self, ctx: GrammaireSQLParser.RequeteContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#params.
    def enterParams(self, ctx: GrammaireSQLParser.ParamsContext):
        s = ["texte.mot LIKE '%{}%'".format(ctx.par1.a.text)]

        if ctx.par2 is not None:
            conj = ctx.conj.text
            if conj == 'et':
                s.append('AND')
            if conj == 'ou':
                s.append('OR')
            s.append("texte.mot LIKE '%{}%'".format(ctx.par2.a.text))

        self.sql_request_tree.where_elements.append(" ".join(s))

    # Exit a parse tree produced by GrammaireSQLParser#params.
    def exitParams(self, ctx: GrammaireSQLParser.ParamsContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#param.
    def enterParam(self, ctx: GrammaireSQLParser.ParamContext):
        pass

    # Exit a parse tree produced by GrammaireSQLParser#param.
    def exitParam(self, ctx: GrammaireSQLParser.ParamContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#time_expression.
    def enterTime_expression(self, ctx: GrammaireSQLParser.Time_expressionContext):

        if ctx.year_ is not None:
            d1 = ctx.year_.digit1.text
            d2 = ctx.year_.digit2.text
            d3 = ctx.year_.digit3.text
            d4 = ctx.year_.digit4.text
            year = int("".join([d1, d2, d3, d4]))
            self.sql_request_tree.where_elements.append("date.annee = '%d'" % year)

        if ctx.month_year_ is not None:
            d1 = ctx.month_year_.year_.digit1.text
            d2 = ctx.month_year_.year_.digit2.text
            d3 = ctx.month_year_.year_.digit3.text
            d4 = ctx.month_year_.year_.digit4.text
            year = int("".join([d1, d2, d3, d4]))
            numeric_month = self.month_string_to_number(ctx.month_year_.month_.text)
            self.sql_request_tree.where_elements.append("date.annee = '%d' AND date.month = '%d'" % (year, numeric_month))

        date_ = ctx.date_
        if date_ is not None:
            day, month, year = self.parse_date(date_)

            constraint = "date.annee = '%d' AND date.month = '%d' AND date.day = '%d'" % \
                         (year, month, day)
            self.sql_request_tree.where_elements.append(constraint)

        if ctx.date_interval_ is not None:
            day_a, month_a, year_a = self.parse_date(ctx.date_interval_.a)
            day_b, month_b, year_b = self.parse_date(ctx.date_interval_.b)

            constraint = "date.annee >= '%d' AND date.month >= '%d' AND date.day >= '%d'" \
                         " AND " \
                         "date.annee <= '%d' AND date.month <= '%d' AND date.day <= '%d'" % \
                         (day_a, month_a, year_a, day_b, month_b, year_b)
            self.sql_request_tree.where_elements.append(constraint)

        if ctx.date_interval_ is not None:
            pass

            # Exit a parse tree produced by GrammaireSQLParser#time_expression.

    def parse_date(self, date):
        d1 = date.year_.digit1.text
        d2 = date.year_.digit2.text
        d3 = date.year_.digit3.text
        d4 = date.year_.digit4.text
        year = int("".join([d1, d2, d3, d4]))
        d5 = date.month_.digit1.text
        d6 = date.month_.digit2.text
        month = int("".join([d5, d6]))
        d7 = date.day_.digit1.text
        d8 = date.day_.digit2.text
        day = int("".join([d7, d8]))
        return day, month, year

    def exitTime_expression(self, ctx: GrammaireSQLParser.Time_expressionContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#date_interval.
    def enterDate_interval(self, ctx: GrammaireSQLParser.Date_intervalContext):
        pass

    # Exit a parse tree produced by GrammaireSQLParser#date_interval.
    def exitDate_interval(self, ctx: GrammaireSQLParser.Date_intervalContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#date.
    def enterDate(self, ctx: GrammaireSQLParser.DateContext):
        pass

    # Exit a parse tree produced by GrammaireSQLParser#date.
    def exitDate(self, ctx: GrammaireSQLParser.DateContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#year.
    def enterYear(self, ctx: GrammaireSQLParser.YearContext):
        pass

    # Exit a parse tree produced by GrammaireSQLParser#year.
    def exitYear(self, ctx: GrammaireSQLParser.YearContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#month.
    def enterMonth(self, ctx: GrammaireSQLParser.MonthContext):
        pass

    # Exit a parse tree produced by GrammaireSQLParser#month.
    def exitMonth(self, ctx: GrammaireSQLParser.MonthContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#day.
    def enterDay(self, ctx: GrammaireSQLParser.DayContext):
        pass

    # Exit a parse tree produced by GrammaireSQLParser#day.
    def exitDay(self, ctx: GrammaireSQLParser.DayContext):
        pass

    def month_string_to_number(self, string):
        m = {
            'janvier':1,
            'février':2,
            'mars':3,
            'avril':4,
            'mai':5,
            'juin':6,
            'juillet':7,
            'aout':8,
            'septembre':9,
            'octobre':10,
            'novembre':11,
            'décembre':12
            }
        s = string.strip().lower()

        try:
            out = m[s]
            return out
        except:
            raise ValueError('Not a month')

if __name__ == '__main__':
    # testing the Listener alone:
    request_natural = "combien article parution 2017 contenir nobel et alimentation"
    request_natural = 'vouloir contact contenir robot en 2013'

    print(request_natural)

    input_stream = InputStream(request_natural)
    lexer = GrammaireSQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammaireSQLParser(stream)
    tree = parser.requete()

    sql_listener = GrammaireSQLListener()
    walker = ParseTreeWalker()
    walker.walk(sql_listener, tree)

    print(sql_listener.sql_request_tree.sql_request())
