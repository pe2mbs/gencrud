#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
lexer.py: A lexer implementation for TypeScript.
"""

import ply.lex as plylex
from typing import List, Dict, Tuple
from ply.lex import LexToken


class Lexer:
    # -------------------------------------------------------------------------
    # Reserved words
    # --------------------------------------------------------------------------
    keywords: Dict[str, str] = {
        keyword: keyword.upper()
        for keyword in [
            # JA
            "any",
            "bool",
            "break",
            "case",
            "catch",
            "class",
            "const",
            "constructor",
            "continue",
            "else",
            "false",
            "finally",
            "for",
            "function",
            "if",
            "import",
            "let",
            "new",
            "number",
            "private",
            "protected",
            "public",
            "from",
            # Paul
            "console",
            "interface",
            "error",
            "log",
            "return",
            "string",
            "throw",
            "true",
            "try",
            "var",
            "while",
        ]
    }

    # -------------------------------------------------------------------------
    # Data Types
    # -------------------------------------------------------------------------
    dataTypes = {
        key: "TYPE_" + key.upper() for key in ["number", "string", "boolean"]
    }

    # -------------------------------------------------------------------------
    # Tokens
    # -------------------------------------------------------------------------
    # merge keywords + types dicts
    reserved = {**keywords, **dataTypes}

    tokens: Tuple[str] = (
        (
            # Paul
            "STRINGCONTENT",
            "OPENPAREN",
            "CLOSEPAREN",
            "OPENBRACKET",
            "CLOSEBRACKET",
            "OPENBRACE",
            "CLOSEBRACE",
            "COMMA",
            "COLON",
            "SEMICOLON",
            "EQUALS",
            "PLUSEQUALS",
            "MINUSEQUALS",
            "EXCLAMATION",
            # Chris
            "PLUS",
            "ID",
            "AMPERSAND",
            "AMPERSANDAMPERSAND",
            "OR",
            "OROR",
            "XOR",
            "EQUALSEQUALS",
            "EQUALSEQUALSEQUALS",
            "EXCLAMATIONEQUALS",
            "LESSTHAN",
            "LESSTHANEQUALS",
            "GREATERTHAN",
            "GREATERTHANEQUALS",
            "MINUS",
            "MULTIPLY",
            "DIVIDE",
            "MODULO",
            "PLUSPLUS",
            "MINUSMINUS",
            "DOT",
            "WHITESPACE",
            "COMMENT",
            "ARROW",
        )
        + tuple(keywords.values())
        + tuple(dataTypes.values())
    )

    # -------------------------------------------------------------------------
    # Token-RegEx & Functions
    # -------------------------------------------------------------------------
    t_PLUS: str = r"\+"
    t_STRINGCONTENT: str = r"(\"[^\"]*\"|'[^']*')"
    t_OPENPAREN: str = r"\("
    t_CLOSEPAREN: str = r"\)"
    t_OPENBRACKET: str = r"\["
    t_CLOSEBRACKET: str = r"\]"
    t_OPENBRACE: str = r"\{"
    t_CLOSEBRACE: str = r"\}"
    t_COMMA: str = r"\,"
    t_EQUALS: str = r"="
    t_EQUALSEQUALS: str = r"=="
    t_EQUALSEQUALSEQUALS: str = r"==="
    t_PLUSEQUALS: str = r"\+="
    t_MINUSEQUALS: str = r"\-="
    t_COLON: str = r"\:"
    t_SEMICOLON: str = r"\;"
    t_AMPERSAND: str = r"&"
    t_AMPERSANDAMPERSAND: str = r"&&"
    t_OR: str = r"\|"
    t_OROR: str = r"\|\|"
    t_XOR: str = r"\^"
    t_EXCLAMATION: str = r"!"
    t_EXCLAMATIONEQUALS: str = r"!="
    t_LESSTHAN: str = r"<"
    t_LESSTHANEQUALS: str = r"<="
    t_GREATERTHAN: str = r">"
    t_GREATERTHANEQUALS: str = r">="
    t_MINUS: str = r"-"
    t_MULTIPLY: str = r"\*"
    t_DIVIDE: str = r"/"
    t_MODULO: str = r"%"
    t_PLUSPLUS: str = r"\+\+"
    t_MINUSMINUS: str = r"--"
    t_DOT: str = r"\."
    t_WHITESPACE: str = r"\s"
    t_ARROW: str = r"=>"

    # ignored characters
    t_ignore: str = " \t"

    def t_COMMENT(self, t: LexToken) -> None:
        r"//.*|/\*[^*]*\*+(?:[^/*][^*]*\*+)*/"
        pass

    def t_newline(self, t: LexToken) -> None:
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_NUMBER(self, t: LexToken):
        r"\d+"
        t.value = int(t.value)

        return t

    def t_ID(self, t: LexToken) -> LexToken:
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = self.reserved.get(t.value.lower(), "ID")

        return t

    # error handling
    def t_error(self, t: LexToken) -> None:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # -------------------------------------------------------------------------

    def __init__(self) -> None:
        self.lexer = plylex.lex(object=self)

    def input(self, input: str) -> None:
        self.lexer.input(input)

    def token(self) -> LexToken:
        return self.lexer.token()

    def lex(self, input: str) -> List[LexToken]:
        self.input(input)
        return list(self.lexer)
