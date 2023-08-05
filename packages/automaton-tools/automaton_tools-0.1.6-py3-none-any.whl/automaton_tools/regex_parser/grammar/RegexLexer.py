# Generated from C:/work/py/automaton_tools/automaton_tools/regex_parser/grammar\Regex.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\26")
        buf.write("T\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3")
        buf.write("\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3")
        buf.write("\f\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\20\3\20\3\21\3\21")
        buf.write("\3\22\3\22\3\23\3\23\3\24\3\24\3\25\3\25\2\2\26\3\3\5")
        buf.write("\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33")
        buf.write("\17\35\20\37\21!\22#\23%\24\'\25)\26\3\2\3\r\2C\\aac|")
        buf.write("\u00c2\u00d8\u00da\u00f8\u00fa\u2001\u3042\u3191\u3302")
        buf.write("\u3381\u3402\u3d2f\u4e02\ua001\uf902\ufb01\2S\2\3\3\2")
        buf.write("\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2")
        buf.write("\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35")
        buf.write("\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2")
        buf.write("\2\'\3\2\2\2\2)\3\2\2\2\3+\3\2\2\2\5-\3\2\2\2\7/\3\2\2")
        buf.write("\2\t\61\3\2\2\2\13\63\3\2\2\2\r\65\3\2\2\2\17\67\3\2\2")
        buf.write("\2\219\3\2\2\2\23;\3\2\2\2\25=\3\2\2\2\27?\3\2\2\2\31")
        buf.write("A\3\2\2\2\33C\3\2\2\2\35F\3\2\2\2\37H\3\2\2\2!J\3\2\2")
        buf.write("\2#L\3\2\2\2%N\3\2\2\2\'P\3\2\2\2)R\3\2\2\2+,\7,\2\2,")
        buf.write("\4\3\2\2\2-.\7-\2\2.\6\3\2\2\2/\60\7}\2\2\60\b\3\2\2\2")
        buf.write("\61\62\7.\2\2\62\n\3\2\2\2\63\64\7\177\2\2\64\f\3\2\2")
        buf.write("\2\65\66\7A\2\2\66\16\3\2\2\2\678\7~\2\28\20\3\2\2\29")
        buf.write(":\7*\2\2:\22\3\2\2\2;<\7+\2\2<\24\3\2\2\2=>\7\60\2\2>")
        buf.write("\26\3\2\2\2?@\7&\2\2@\30\3\2\2\2AB\7`\2\2B\32\3\2\2\2")
        buf.write("CD\7]\2\2DE\7`\2\2E\34\3\2\2\2FG\7_\2\2G\36\3\2\2\2HI")
        buf.write("\7]\2\2I \3\2\2\2JK\7/\2\2K\"\3\2\2\2LM\7^\2\2M$\3\2\2")
        buf.write("\2NO\7\"\2\2O&\3\2\2\2PQ\4\62;\2Q(\3\2\2\2RS\t\2\2\2S")
        buf.write("*\3\2\2\2\3\2\2")
        return buf.getvalue()


class RegexLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    Digit = 19
    Letter = 20

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'*'", "'+'", "'{'", "','", "'}'", "'?'", "'|'", "'('", "')'", 
            "'.'", "'$'", "'^'", "'[^'", "']'", "'['", "'-'", "'\\'", "' '" ]

    symbolicNames = [ "<INVALID>",
            "Digit", "Letter" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "Digit", "Letter" ]

    grammarFileName = "Regex.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


