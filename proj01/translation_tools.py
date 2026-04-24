# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 19:17:41 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

Some standard classess for translation
"""

from collections import deque

# TokenStream is a simple wrapper for ply.lex
# which provides a simple interface for matching 
# and pushing tockens back
class TokenStream:

    def __init__(self):
        self.tokens = deque()
        
    def __len__(self):
        return len(self.tokens)

    def nextToken(self):
        return self.tokens.popleft()
    

    def pushTokenBack(self, tok):
        self.tokens.appendleft(tok)

    def match(self, tok, tokenType):
        if tok.type != tokenType:
            raise SyntaxError(f"Unexpected token: {tok.type} instead of {tokenType}")

    def matchNext(self, tokenType):
        self.match(self.nextToken(), tokenType)

    def parse(self, input, lexer):
        lexer.input(input)
        self.tokens = deque(tok for tok in lexer)

