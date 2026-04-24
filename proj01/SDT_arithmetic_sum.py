# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 19:26:02 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

A very simple recursive descent SDT example for the LL(1) summation grammar:
    
    P -> E
    E -> T E'
    E' -> + T E'
    E' -> eps
    T -> number
    
The annotated grammar (SDT):
    
    P -> E { P.syn = E.syn }
    E -> T E' { E'.inh = T.syn; E.syn = E'.syn }
    E' -> + T E'1 { E'_1.inh = E'.inh + T.syn; E'.syn = E'1.syn }
    E' -> eps { E'.syn = E'.inh }
    T -> number { T.syn = number.lexval }
    
Remark: "lexval" means a value coming from the lexer (token), 
not computed by the parser.
"""

import ply.lex as lex
from translation_tools import TokenStream


tokens = ( 'NUM', 'PLUS', )

t_NUM = r"[0-9]+"
t_PLUS = r"\+"

# PLY requires a function to process errors of lexer
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)  # move to the next lexeme


# PLY requires a variable to know which characters to skip
t_ignore = ' \t'  # ignore spaces and tabs



class ArithmeticSumSDT:
    
    def __init__(self, input):
        self.stream = TokenStream()
        self.stream.parse(input, lex.lex())
        
    def parse(self):
        return self.parse_P()
    
    def parse_P(self):
        return self.parse_E()
        
    def parse_E(self):
        left_val = self.parse_T()
        return self.parse_E1(left_val)
        
    def parse_E1(self, left_val):
        if not self.stream:
            # epsilon
            return left_val
            
        tok = self.stream.nextToken()
        if tok.type == 'PLUS':
            right_val = self.parse_T()
            val = left_val + right_val
            return self.parse_E1(val)
        else:
            raise SyntaxError(f"Unexpected token: {tok}")


    def parse_T(self):
        if not self.stream:
            raise SyntaxError("Number expected but the stream is empty!")
        tok = self.stream.nextToken()
        self.stream.match(tok, 'NUM')
        return int(tok.value)
        
    

def main():
    
    input = "4 + 2 + 3 + 7"
    
    sdt = ArithmeticSumSDT(input)
    result = sdt.parse()
    
    print(f"{input} = {result}")



if __name__ == "__main__":
    main()
