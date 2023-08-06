# Generated from FoostacheParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FoostacheParser import FoostacheParser
else:
    from FoostacheParser import FoostacheParser

# This class defines a complete generic visitor for a parse tree produced by FoostacheParser.

class FoostacheParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FoostacheParser#template.
    def visitTemplate(self, ctx:FoostacheParser.TemplateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#statements.
    def visitStatements(self, ctx:FoostacheParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#statement.
    def visitStatement(self, ctx:FoostacheParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#rawText.
    def visitRawText(self, ctx:FoostacheParser.RawTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#literal.
    def visitLiteral(self, ctx:FoostacheParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#literalText.
    def visitLiteralText(self, ctx:FoostacheParser.LiteralTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#stringField.
    def visitStringField(self, ctx:FoostacheParser.StringFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#numberField.
    def visitNumberField(self, ctx:FoostacheParser.NumberFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#inlineFilter.
    def visitInlineFilter(self, ctx:FoostacheParser.InlineFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#numberFormat.
    def visitNumberFormat(self, ctx:FoostacheParser.NumberFormatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#ifBlock.
    def visitIfBlock(self, ctx:FoostacheParser.IfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#ifTag.
    def visitIfTag(self, ctx:FoostacheParser.IfTagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#elseifBlock.
    def visitElseifBlock(self, ctx:FoostacheParser.ElseifBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#elseifTag.
    def visitElseifTag(self, ctx:FoostacheParser.ElseifTagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#elseBlock.
    def visitElseBlock(self, ctx:FoostacheParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#orExpression.
    def visitOrExpression(self, ctx:FoostacheParser.OrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#andExpression.
    def visitAndExpression(self, ctx:FoostacheParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#boolExpression.
    def visitBoolExpression(self, ctx:FoostacheParser.BoolExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#existsExpression.
    def visitExistsExpression(self, ctx:FoostacheParser.ExistsExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#notExpression.
    def visitNotExpression(self, ctx:FoostacheParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#parenExpression.
    def visitParenExpression(self, ctx:FoostacheParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#typeExpression.
    def visitTypeExpression(self, ctx:FoostacheParser.TypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#dotPath.
    def visitDotPath(self, ctx:FoostacheParser.DotPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#caretPath.
    def visitCaretPath(self, ctx:FoostacheParser.CaretPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#idObjectKey.
    def visitIdObjectKey(self, ctx:FoostacheParser.IdObjectKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#qsObjectKey.
    def visitQsObjectKey(self, ctx:FoostacheParser.QsObjectKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#arrayIndex.
    def visitArrayIndex(self, ctx:FoostacheParser.ArrayIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#withBlock.
    def visitWithBlock(self, ctx:FoostacheParser.WithBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateBlock.
    def visitIterateBlock(self, ctx:FoostacheParser.IterateBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#indexRange.
    def visitIndexRange(self, ctx:FoostacheParser.IndexRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#indexRangeB.
    def visitIndexRangeB(self, ctx:FoostacheParser.IndexRangeBContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#indexRangeC.
    def visitIndexRangeC(self, ctx:FoostacheParser.IndexRangeCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateClause.
    def visitIterateClause(self, ctx:FoostacheParser.IterateClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateBeforeClause.
    def visitIterateBeforeClause(self, ctx:FoostacheParser.IterateBeforeClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateAfterClause.
    def visitIterateAfterClause(self, ctx:FoostacheParser.IterateAfterClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateBetweenClause.
    def visitIterateBetweenClause(self, ctx:FoostacheParser.IterateBetweenClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateElseClause.
    def visitIterateElseClause(self, ctx:FoostacheParser.IterateElseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#filterBlock.
    def visitFilterBlock(self, ctx:FoostacheParser.FilterBlockContext):
        return self.visitChildren(ctx)



del FoostacheParser