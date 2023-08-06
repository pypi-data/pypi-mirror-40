# Generated from FoostacheParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FoostacheParser import FoostacheParser
else:
    from FoostacheParser import FoostacheParser

# This class defines a complete listener for a parse tree produced by FoostacheParser.
class FoostacheParserListener(ParseTreeListener):

    # Enter a parse tree produced by FoostacheParser#template.
    def enterTemplate(self, ctx:FoostacheParser.TemplateContext):
        pass

    # Exit a parse tree produced by FoostacheParser#template.
    def exitTemplate(self, ctx:FoostacheParser.TemplateContext):
        pass


    # Enter a parse tree produced by FoostacheParser#statements.
    def enterStatements(self, ctx:FoostacheParser.StatementsContext):
        pass

    # Exit a parse tree produced by FoostacheParser#statements.
    def exitStatements(self, ctx:FoostacheParser.StatementsContext):
        pass


    # Enter a parse tree produced by FoostacheParser#statement.
    def enterStatement(self, ctx:FoostacheParser.StatementContext):
        pass

    # Exit a parse tree produced by FoostacheParser#statement.
    def exitStatement(self, ctx:FoostacheParser.StatementContext):
        pass


    # Enter a parse tree produced by FoostacheParser#rawText.
    def enterRawText(self, ctx:FoostacheParser.RawTextContext):
        pass

    # Exit a parse tree produced by FoostacheParser#rawText.
    def exitRawText(self, ctx:FoostacheParser.RawTextContext):
        pass


    # Enter a parse tree produced by FoostacheParser#literal.
    def enterLiteral(self, ctx:FoostacheParser.LiteralContext):
        pass

    # Exit a parse tree produced by FoostacheParser#literal.
    def exitLiteral(self, ctx:FoostacheParser.LiteralContext):
        pass


    # Enter a parse tree produced by FoostacheParser#literalText.
    def enterLiteralText(self, ctx:FoostacheParser.LiteralTextContext):
        pass

    # Exit a parse tree produced by FoostacheParser#literalText.
    def exitLiteralText(self, ctx:FoostacheParser.LiteralTextContext):
        pass


    # Enter a parse tree produced by FoostacheParser#stringField.
    def enterStringField(self, ctx:FoostacheParser.StringFieldContext):
        pass

    # Exit a parse tree produced by FoostacheParser#stringField.
    def exitStringField(self, ctx:FoostacheParser.StringFieldContext):
        pass


    # Enter a parse tree produced by FoostacheParser#numberField.
    def enterNumberField(self, ctx:FoostacheParser.NumberFieldContext):
        pass

    # Exit a parse tree produced by FoostacheParser#numberField.
    def exitNumberField(self, ctx:FoostacheParser.NumberFieldContext):
        pass


    # Enter a parse tree produced by FoostacheParser#inlineFilter.
    def enterInlineFilter(self, ctx:FoostacheParser.InlineFilterContext):
        pass

    # Exit a parse tree produced by FoostacheParser#inlineFilter.
    def exitInlineFilter(self, ctx:FoostacheParser.InlineFilterContext):
        pass


    # Enter a parse tree produced by FoostacheParser#numberFormat.
    def enterNumberFormat(self, ctx:FoostacheParser.NumberFormatContext):
        pass

    # Exit a parse tree produced by FoostacheParser#numberFormat.
    def exitNumberFormat(self, ctx:FoostacheParser.NumberFormatContext):
        pass


    # Enter a parse tree produced by FoostacheParser#ifBlock.
    def enterIfBlock(self, ctx:FoostacheParser.IfBlockContext):
        pass

    # Exit a parse tree produced by FoostacheParser#ifBlock.
    def exitIfBlock(self, ctx:FoostacheParser.IfBlockContext):
        pass


    # Enter a parse tree produced by FoostacheParser#ifTag.
    def enterIfTag(self, ctx:FoostacheParser.IfTagContext):
        pass

    # Exit a parse tree produced by FoostacheParser#ifTag.
    def exitIfTag(self, ctx:FoostacheParser.IfTagContext):
        pass


    # Enter a parse tree produced by FoostacheParser#elseifBlock.
    def enterElseifBlock(self, ctx:FoostacheParser.ElseifBlockContext):
        pass

    # Exit a parse tree produced by FoostacheParser#elseifBlock.
    def exitElseifBlock(self, ctx:FoostacheParser.ElseifBlockContext):
        pass


    # Enter a parse tree produced by FoostacheParser#elseifTag.
    def enterElseifTag(self, ctx:FoostacheParser.ElseifTagContext):
        pass

    # Exit a parse tree produced by FoostacheParser#elseifTag.
    def exitElseifTag(self, ctx:FoostacheParser.ElseifTagContext):
        pass


    # Enter a parse tree produced by FoostacheParser#elseBlock.
    def enterElseBlock(self, ctx:FoostacheParser.ElseBlockContext):
        pass

    # Exit a parse tree produced by FoostacheParser#elseBlock.
    def exitElseBlock(self, ctx:FoostacheParser.ElseBlockContext):
        pass


    # Enter a parse tree produced by FoostacheParser#orExpression.
    def enterOrExpression(self, ctx:FoostacheParser.OrExpressionContext):
        pass

    # Exit a parse tree produced by FoostacheParser#orExpression.
    def exitOrExpression(self, ctx:FoostacheParser.OrExpressionContext):
        pass


    # Enter a parse tree produced by FoostacheParser#andExpression.
    def enterAndExpression(self, ctx:FoostacheParser.AndExpressionContext):
        pass

    # Exit a parse tree produced by FoostacheParser#andExpression.
    def exitAndExpression(self, ctx:FoostacheParser.AndExpressionContext):
        pass


    # Enter a parse tree produced by FoostacheParser#boolExpression.
    def enterBoolExpression(self, ctx:FoostacheParser.BoolExpressionContext):
        pass

    # Exit a parse tree produced by FoostacheParser#boolExpression.
    def exitBoolExpression(self, ctx:FoostacheParser.BoolExpressionContext):
        pass


    # Enter a parse tree produced by FoostacheParser#existsExpression.
    def enterExistsExpression(self, ctx:FoostacheParser.ExistsExpressionContext):
        pass

    # Exit a parse tree produced by FoostacheParser#existsExpression.
    def exitExistsExpression(self, ctx:FoostacheParser.ExistsExpressionContext):
        pass


    # Enter a parse tree produced by FoostacheParser#notExpression.
    def enterNotExpression(self, ctx:FoostacheParser.NotExpressionContext):
        pass

    # Exit a parse tree produced by FoostacheParser#notExpression.
    def exitNotExpression(self, ctx:FoostacheParser.NotExpressionContext):
        pass


    # Enter a parse tree produced by FoostacheParser#parenExpression.
    def enterParenExpression(self, ctx:FoostacheParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by FoostacheParser#parenExpression.
    def exitParenExpression(self, ctx:FoostacheParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by FoostacheParser#typeExpression.
    def enterTypeExpression(self, ctx:FoostacheParser.TypeExpressionContext):
        pass

    # Exit a parse tree produced by FoostacheParser#typeExpression.
    def exitTypeExpression(self, ctx:FoostacheParser.TypeExpressionContext):
        pass


    # Enter a parse tree produced by FoostacheParser#dotPath.
    def enterDotPath(self, ctx:FoostacheParser.DotPathContext):
        pass

    # Exit a parse tree produced by FoostacheParser#dotPath.
    def exitDotPath(self, ctx:FoostacheParser.DotPathContext):
        pass


    # Enter a parse tree produced by FoostacheParser#caretPath.
    def enterCaretPath(self, ctx:FoostacheParser.CaretPathContext):
        pass

    # Exit a parse tree produced by FoostacheParser#caretPath.
    def exitCaretPath(self, ctx:FoostacheParser.CaretPathContext):
        pass


    # Enter a parse tree produced by FoostacheParser#idObjectKey.
    def enterIdObjectKey(self, ctx:FoostacheParser.IdObjectKeyContext):
        pass

    # Exit a parse tree produced by FoostacheParser#idObjectKey.
    def exitIdObjectKey(self, ctx:FoostacheParser.IdObjectKeyContext):
        pass


    # Enter a parse tree produced by FoostacheParser#qsObjectKey.
    def enterQsObjectKey(self, ctx:FoostacheParser.QsObjectKeyContext):
        pass

    # Exit a parse tree produced by FoostacheParser#qsObjectKey.
    def exitQsObjectKey(self, ctx:FoostacheParser.QsObjectKeyContext):
        pass


    # Enter a parse tree produced by FoostacheParser#arrayIndex.
    def enterArrayIndex(self, ctx:FoostacheParser.ArrayIndexContext):
        pass

    # Exit a parse tree produced by FoostacheParser#arrayIndex.
    def exitArrayIndex(self, ctx:FoostacheParser.ArrayIndexContext):
        pass


    # Enter a parse tree produced by FoostacheParser#withBlock.
    def enterWithBlock(self, ctx:FoostacheParser.WithBlockContext):
        pass

    # Exit a parse tree produced by FoostacheParser#withBlock.
    def exitWithBlock(self, ctx:FoostacheParser.WithBlockContext):
        pass


    # Enter a parse tree produced by FoostacheParser#iterateBlock.
    def enterIterateBlock(self, ctx:FoostacheParser.IterateBlockContext):
        pass

    # Exit a parse tree produced by FoostacheParser#iterateBlock.
    def exitIterateBlock(self, ctx:FoostacheParser.IterateBlockContext):
        pass


    # Enter a parse tree produced by FoostacheParser#indexRange.
    def enterIndexRange(self, ctx:FoostacheParser.IndexRangeContext):
        pass

    # Exit a parse tree produced by FoostacheParser#indexRange.
    def exitIndexRange(self, ctx:FoostacheParser.IndexRangeContext):
        pass


    # Enter a parse tree produced by FoostacheParser#indexRangeB.
    def enterIndexRangeB(self, ctx:FoostacheParser.IndexRangeBContext):
        pass

    # Exit a parse tree produced by FoostacheParser#indexRangeB.
    def exitIndexRangeB(self, ctx:FoostacheParser.IndexRangeBContext):
        pass


    # Enter a parse tree produced by FoostacheParser#indexRangeC.
    def enterIndexRangeC(self, ctx:FoostacheParser.IndexRangeCContext):
        pass

    # Exit a parse tree produced by FoostacheParser#indexRangeC.
    def exitIndexRangeC(self, ctx:FoostacheParser.IndexRangeCContext):
        pass


    # Enter a parse tree produced by FoostacheParser#iterateClause.
    def enterIterateClause(self, ctx:FoostacheParser.IterateClauseContext):
        pass

    # Exit a parse tree produced by FoostacheParser#iterateClause.
    def exitIterateClause(self, ctx:FoostacheParser.IterateClauseContext):
        pass


    # Enter a parse tree produced by FoostacheParser#iterateBeforeClause.
    def enterIterateBeforeClause(self, ctx:FoostacheParser.IterateBeforeClauseContext):
        pass

    # Exit a parse tree produced by FoostacheParser#iterateBeforeClause.
    def exitIterateBeforeClause(self, ctx:FoostacheParser.IterateBeforeClauseContext):
        pass


    # Enter a parse tree produced by FoostacheParser#iterateAfterClause.
    def enterIterateAfterClause(self, ctx:FoostacheParser.IterateAfterClauseContext):
        pass

    # Exit a parse tree produced by FoostacheParser#iterateAfterClause.
    def exitIterateAfterClause(self, ctx:FoostacheParser.IterateAfterClauseContext):
        pass


    # Enter a parse tree produced by FoostacheParser#iterateBetweenClause.
    def enterIterateBetweenClause(self, ctx:FoostacheParser.IterateBetweenClauseContext):
        pass

    # Exit a parse tree produced by FoostacheParser#iterateBetweenClause.
    def exitIterateBetweenClause(self, ctx:FoostacheParser.IterateBetweenClauseContext):
        pass


    # Enter a parse tree produced by FoostacheParser#iterateElseClause.
    def enterIterateElseClause(self, ctx:FoostacheParser.IterateElseClauseContext):
        pass

    # Exit a parse tree produced by FoostacheParser#iterateElseClause.
    def exitIterateElseClause(self, ctx:FoostacheParser.IterateElseClauseContext):
        pass


    # Enter a parse tree produced by FoostacheParser#filterBlock.
    def enterFilterBlock(self, ctx:FoostacheParser.FilterBlockContext):
        pass

    # Exit a parse tree produced by FoostacheParser#filterBlock.
    def exitFilterBlock(self, ctx:FoostacheParser.FilterBlockContext):
        pass


