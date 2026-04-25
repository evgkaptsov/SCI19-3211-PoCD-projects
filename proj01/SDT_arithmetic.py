# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 09:55:44 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

============================================================================
Note that this code is intended for educational purposes. It is deliberately 
simplified in order to improve readability and facilitate understanding 
for students.
============================================================================

A simple recursive descent SDT example for the LL(1) arithmetics grammar:
    
    P -> E
    E -> T E'
    E' -> + T E'
    E' -> eps
    T -> F T'
    T' -> * F T'
    T' -> eps
    F -> (E)
    F -> number
    
The annotated grammar (SDT):
    
    P -> E            { P.syn = E.syn }
    E -> T E'         { E'.inh = T.syn; E.syn = E'.syn }
    E' -> + T E'1     { E'1.inh = E'.inh + T.syn; E'.syn = E'1.syn }
    E' -> eps         { E'.syn = E'.inh }
    T -> F T'         { T'.inh = F.syn; T.syn = T'.syn }
    T' -> * F T'1     { T'1.inh = T'.inh * F.syn; T'.syn = T'1.syn }
    T' -> eps         { T'.syn = T'.inh }
    F -> (E)          { F.syn = E.syn }
    F -> number       { F.syn = number.lexval }
    
Remark: "lexval" means a value coming from the lexer (token), 
not computed by the parser.
"""

import ply.lex as lex
from translation_tools import TokenStream


tokens = ( 'NUM', 'PLUS', 'MULT', 'LBRACKET', 'RBRACKET' )

t_NUM = r"[0-9]+"
t_PLUS = r"\+"
t_MULT = r"\*"
t_LBRACKET = r"\("
t_RBRACKET = r"\)"


# PLY requires a function to process errors of lexer
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)  # move to the next lexeme


# PLY requires a variable to know which characters to skip
t_ignore = ' \t'  # ignore spaces and tabs



class ArithmeticSDT:
    
    def __init__(self, input):
        self.stream = TokenStream()
        self.stream.parse(input, lex.lex())
        
    def parse(self):
        return self.parse_P()

    def parse_P(self):
        return self.parse_E()
        
    def parse_E(self):
        left_val = self.parse_T()
        return self.parse_E_prime(left_val)
        
    def parse_E_prime(self, left_val):
        if not self.stream:
            # eps
            return left_val
        
        tok = self.stream.nextToken()
        if tok.type != 'PLUS':
            # eps
            self.stream.pushTokenBack(tok)
            return left_val
        
        right_val = self.parse_T()
        return self.parse_E_prime(left_val + right_val)
    

    def parse_T(self):
        left_val = self.parse_F()
        return self.parse_T_prime(left_val)
    
    def parse_T_prime(self, left_val):
        
        if not self.stream:
            # eps
            return left_val
        
        tok = self.stream.nextToken()
        if tok.type != 'MULT':
            # eps
            self.stream.pushTokenBack(tok)
            return left_val
        
        right_val = self.parse_F()
        return self.parse_T_prime(left_val * right_val)
        

    def parse_F(self):
        
        tok = self.stream.nextToken()
        if tok.type == 'NUM':
            return int(tok.value)
        else:
            self.stream.match(tok, 'LBRACKET')
            result = self.parse_E()
            self.stream.matchNext('RBRACKET')
            return result


def main():
    
    # input = "4 * 2 + 3 * 7"
    input = "9 + 4 * (2 + (1 * 3)) * 7 + 1"
    
    sdt = ArithmeticSDT(input)
    result = sdt.parse()
    
    print(f"{input} = {result}")



if __name__ == "__main__":
    main()
