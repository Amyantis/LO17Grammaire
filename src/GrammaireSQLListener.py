# Generated from GrammaireSQL.g4 by ANTLR 4.5.3
from antlr4 import *

# This class defines a complete listener for a parse tree produced by GrammaireSQLParser.
from gen.GrammaireSQLLexer import GrammaireSQLLexer
from gen.GrammaireSQLParser import GrammaireSQLParser


class GrammaireSQLListener(ParseTreeListener):
    def __init__(self) -> None:
        super().__init__()
        self.request_tree = []
        self.sql_request = ""

    # Enter a parse tree produced by GrammaireSQLParser#listrequete.
    def enterListrequete(self, ctx: GrammaireSQLParser.ListrequeteContext):
        pass

    # Exit a parse tree produced by GrammaireSQLParser#listrequete.
    def exitListrequete(self, ctx: GrammaireSQLParser.ListrequeteContext):
        pass

    # Enter a parse tree produced by GrammaireSQLParser#requete.
    def enterRequete(self, ctx: GrammaireSQLParser.RequeteContext):
        if ctx.SELECT() is not None:
            self.request_tree.append("SELECT DISTINCT *")
        if ctx.COUNT() is not None:
            self.request_tree.append("SELECT COUNT(*)")

        # if ctx.ARTICLE() is not None:
        #     self.request_tree.append("article")
        # if ctx.BULLETIN() is not None:
        #     self.request_tree.append("bulletin")

        self.request_tree.append("FROM titreresume")

        if ctx.WHEN() is not None:
            self.request_tree.append(", date")

        if ctx.MOT() is not None or ctx.WHEN() is not None:
            self.request_tree.append("WHERE")
            ctx.subtree = []
            # self.request_tree.append(ctx.subtree)

    # Exit a parse tree produced by GrammaireSQLParser#requete.
    def exitRequete(self, ctx: GrammaireSQLParser.RequeteContext):
        self.request_tree.append(" AND ".join(ctx.subtree))
        self.sql_request = " ".join(self.request_tree)

    # Enter a parse tree produced by GrammaireSQLParser#params.
    def enterParams(self, ctx: GrammaireSQLParser.ParamsContext):
        params_tree = []
        params_tree.append("titreresume.mot LIKE '%{}%'".format(ctx.par1.a.text))

        if ctx.par2 is not None:
            conj = ctx.conj.text
            if conj == 'et':
                params_tree.append('AND')
            if conj == 'or':
                params_tree.append('OR')
            params_tree.append("titreresume.mot LIKE '%{}%'".format(ctx.par2.a.text))
        ctx.parentCtx.subtree.append(" ".join(params_tree))

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
            ctx.parentCtx.subtree.append("".join(["date.annee = %d" % year]))

        if ctx.date_ is not None:
            pass
        if ctx.date_interval_ is not None:
            pass

            # Exit a parse tree produced by GrammaireSQLParser#time_expression.

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


if __name__ == '__main__':
    request_natural = "combien article parution 2017 contenir nobel et alimentation"
    input_stream = InputStream(request_natural)
    lexer = GrammaireSQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammaireSQLParser(stream)
    tree = parser.requete()

    sql_listener = GrammaireSQLListener()
    walker = ParseTreeWalker()
    walker.walk(sql_listener, tree)

    print(sql_listener.sql_request)
