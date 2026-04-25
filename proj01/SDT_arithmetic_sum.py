# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 19:26:02 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

============================================================================
Note that this code is intended for educational purposes. It is deliberately 
simplified in order to improve readability and facilitate understanding 
for students.
============================================================================

A very simple recursive descent SDT example for the LL(1) summation grammar:
    
    P -> E
    E -> T E'
    E' -> + T E'
    E' -> eps
    T -> number
    
The annotated grammar (SDT):
    
    P -> E { P.syn = E.syn }
    E -> T E' { E'.inh = T.syn; E.syn = E'.syn }
    E' -> + T E'1 { E'1.inh = E'.inh + T.syn; E'.syn = E'1.syn }
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
        self.stream.load(input, lex.lex())
        
    def parse(self):
        return self.parse_P()
    
    def parse_P(self):
        return self.parse_E()
        
    def parse_E(self):
        left_val = self.parse_T()
        return self.parse_E_prime(left_val)
        
    def parse_E_prime(self, left_val):
        # epsilon
        if not self.stream:
            return left_val 

        self.stream.matchNext('PLUS')
        right_val = self.parse_T()
        return self.parse_E_prime(left_val + right_val)

    def parse_T(self):
        if not self.stream:
            raise SyntaxError("Number expected but the stream is empty!")
        tok = self.stream.matchNext('NUM')
        return int(tok.value)
        
    

def main():
    
    input = "4 + 2 + 3 + 7"
    
    sdt = ArithmeticSumSDT(input)
    result = sdt.parse()
    
    print(f"{input} = {result}")



if __name__ == "__main__":
    main()
