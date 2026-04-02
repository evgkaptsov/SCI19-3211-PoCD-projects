# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:07:15 2026
"""
import ply.lex as lex


reserved = {
   'if' : 'IF',
}

literals = '+-*/'

tokens = ['NUMBER', 'LBRACKET', 'RBRACKET', 'ASSIGN', 'EQ', 'ID'] + list(reserved.values())

t_NUMBER = r'\d+'
t_EQ = r'=='
t_ASSIGN = r'='
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_IF = 'if'
t_ignore = ' \t'


def t_COMMENT(t):
    r'%%.*'
    pass
    
    
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

    
def t_error(t):
    print("Illegal character:", t.value[0])
    t.lexer.skip(1)
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    

def main():
    
    input = '''xyz123 = 13+24*(711-993)+33+56/(621-9942)+3564*13+42/712-994 
        %% a comment
        if x==y
    '''

    lexer = lex.lex()
    lexer.input(input)
    
    for tok in lexer:
        print(tok)



if __name__ == "__main__":
    main()
