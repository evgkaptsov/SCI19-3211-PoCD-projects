# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 19:17:41 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

============================================================================
Note that this code is intended for educational purposes. It is deliberately 
simplified in order to improve readability and facilitate understanding 
for students.
============================================================================

Some standard utilities for translation
"""

from collections import deque

# TokenStream is a simple wrapper for ply.lex
# which provides a standard interface for matching 
# and pushing tokens back
class TokenStream:

    def __init__(self):
        self.tokens = deque()
        
    def __len__(self):
        return len(self.tokens)
    
    def load(self, input, lexer):
        lexer.input(input)
        self.tokens = deque(tok for tok in lexer)

    # "scan_token" in  [Thain]
    def nextToken(self):
        return self.tokens.popleft()
    
    # "putback_token" [Thain]
    def pushTokenBack(self, tok):
        self.tokens.appendleft(tok)

    # similar to "expect_token" in [Thain]
    def matchNext(self, tokenType):
        tok = self.nextToken()
        self.match(tok, tokenType)
        return tok
    
    def match(self, tok, tokenType):
        if tok.type != tokenType:
            raise SyntaxError(f"Unexpected token: {tok.type} instead of {tokenType}")
            
    def raiseError(self, tok):
        raise SyntaxError(f"Unexpected token: {tok.type}")


