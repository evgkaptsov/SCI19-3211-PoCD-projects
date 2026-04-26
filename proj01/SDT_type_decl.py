# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:10:29 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

============================================================================
Note that this code is intended for educational purposes. It is deliberately
simplified in order to improve readability and facilitate understanding
for students.
============================================================================

SDT for a simple LL(1) grammar with declarations and scopes

P → { L }
L → D L | S L | ε
D → T id ;
S → id G' = E ; | { L }
T → T0 C
T0 → int | float | record { L }
C → [ num ] C | ε
E → F E'
E' → + F E' | ε
F → G F'
F' → ∗ G F' | ε
G → id G' | (E) | num
G' → [ E ] G' | . id G' | ε

"""

import ply.lex as lex
from translation_tools import TokenStream


reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'record': 'REC'
}

tokens = ['ID', 'NUM' ] + list(reserved.values())

literals = "+*=.;(){}[]"

t_NUM = r"[0-9]+(\.[0-9]+)?"


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')     # Check for reserved words
    return t


# PLY requires a function to process errors of lexer
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)  # move to the next lexeme

# the function t_newline defines how to process new lines


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# PLY requires a variable to know which characters to skip
t_ignore = ' \t'  # ignore spaces and tabs


class DeclSDT:

    def __init__(self, input):
        self.stream = TokenStream()
        self.stream.load(input, lex.lex())

    def parse(self):
        self.parse_P()

    def parse_P(self):
        self.stream.matchNext('{')
        self.parse_L()
        self.stream.matchNext('}')

    def parse_L(self):
        if self.parse_D() or self.parse_S():
            self.parse_L()
    
    def parse_D(self):
        if self.parse_T():
            self.stream.matchNext('ID')
            self.stream.matchNext(';')
            return True
        return False
    
    def parse_S(self):
        t = self.stream.nextToken()
        if t.type == 'ID':
            self.parse_G_prime()
            self.stream.matchNext('=')
            self.parse_E()
            self.stream.matchNext(';')
            return True
        elif t.type == '{':
            self.parse_L()
            self.stream.matchNext('}')
            return True
        else:
            self.stream.pushTokenBack(t)
            return False
        
    def parse_T(self):
        if self.parse_T0():
            self.parse_C()
            return True
        else:
            return False
        
    def parse_T0(self):
        t = self.stream.nextToken()
        if t.type == 'INT':
            return True
        elif t.type == 'FLOAT':
            return True
        elif t.type == 'REC':
            self.stream.matchNext('{')
            self.parse_L()
            self.stream.matchNext('}')
            return True
        else:
            self.stream.pushTokenBack(t)
            return False
        
    def parse_C(self):
        t = self.stream.nextToken()
        if t.type == '[':
            self.stream.matchNext('NUM')
            self.stream.matchNext(']')
            self.parse_C()
        else:
            self.stream.pushTokenBack(t)
    
    def parse_E(self):
        self.parse_F()
        self.parse_E_prime()
    
    def parse_E_prime(self):
        t = self.stream.nextToken()
        if t.type == '+':
            self.parse_F()
            self.parse_E_prime()
        else:
            self.stream.pushTokenBack(t)
    
    def parse_F(self):
        self.parse_G()
        self.parse_F_prime()
        
    def parse_F_prime(self):
        t = self.stream.nextToken()
        if t.type == '*':
            self.parse_G()
            self.parse_F_prime()
        else:
            self.stream.pushTokenBack(t)
        
    def parse_G(self):
        t = self.stream.nextToken()
        if t.type == 'ID':
            self.parse_G_prime()
        elif t.type == '(':
            self.parse_E()
            self.stream.matchNext(')')
        else:
            self.stream.match(t, 'NUM')
    
    def parse_G_prime(self):
        t = self.stream.nextToken()
        if t.type == '[':
            self.parse_E()
            self.stream.matchNext(']')
            self.parse_G_prime()
        elif t.type == '.':
            self.stream.matchNext('ID')
            self.parse_G_prime()
        else:
            self.stream.pushTokenBack(t)
    
    

def main():
    
    input = """\
        {
            int x;
            int y;
            x = 1;
            y = 2;
            
            record {
                int x;
                int y;
            }[2] r1;
            
            r1[0].x = 2;
            r1[0].y = 3;
            
            {
                int[10] w;
                int x;
                float z;
                z = 5.25;
                y = z + x * y;
                r1[1].x = r1[1].y;
                r1[1].y = r1[1].x;
            }
            
            int w;
            w = x + y + z;
        }
    """
    
    sdt = DeclSDT(input)
    sdt.parse()
    
    print("Done.")



if __name__ == "__main__":
    main()
