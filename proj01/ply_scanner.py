# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:43:09 2026

@author: SCI19 3211 (Principles of Compiler Design)

This scanner produces tokens for a very simple programming language. 
See extended documentation and examples at: https://www.dabeaz.com/ply/ply.html#ply_nn4
"""

# include standard PLY Lex package
import ply.lex as lex


# map of reserved words in the format lexeme : TokenType
reserved = {
   'if' : 'IF',
   'then': 'THEN',
   'else': 'ELSE'
}


# list of tokens including reserved words
tokens = ['VAR', 'NUMBER', 'ASSIGN', 
          'EQUAL', 'LEQ', 'GEQ', 'LESS', 'GREATER',
          'ADD', 'SUB', 'MULT', 'DIV', 
          'AADD', 'ASUB', 'AMULT', 'ADIV',
          'LBRACKET', 'RBRACKET', 'SEPARATOR'
         ] + list(reserved.values())

# regular expressions for the tokens:
t_ASSIGN = r'='
t_NUMBER = r'[0-9]+' # + means "one or more"
t_ADD = r'\+' # \+ means just "plus"
t_SUB = r'-'
t_MULT = r'\*' # escape so we will not mix up with Kleene star
t_DIV = r'/'
t_AADD = r'\+='
t_ASUB = r'-='
t_AMULT = r'\*='
t_ADIV = r'/='
t_EQUAL = r'=='
t_LEQ = r'<='
t_GEQ = r'>='
t_LESS = r'<'
t_GREATER = r's>'
t_LBRACKET = r'\(' # escape because '(' has special meaning in reg. expr.
t_RBRACKET = r'\)' # (same story, so we escape the bracket)
t_SEPARATOR = r';' # separator for expressions


# for variables, we distinguish reserved words from ids
def t_VAR(t):
    r'[A-Za-z_][A-Za-z_0-9]*' # standard reg expr for variables and ids
    t.type = reserved.get(t.value,'VAR')    # Check for reserved words
    return t

# PLY requires a function to process errors of lexer
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1) # move to the next lexeme

# PLY requires a variable to know which characters to skip
t_ignore = ' \t' # ignore spaces and tabs

# this function defines how to process new lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    

def main():
    
    # a simple example of a code to be converted into a sequence of tokens
    input = '''Xyz_123 = 13+24*(711-993)+33+56/(621-9942)+3564*13+42/712-994;
    if(x<=y) then 
        x+=4;
    else
        y/=3+x;
    '''
    
    # use PLY Lexer here
    lexer = lex.lex()
    lexer.input(input) # use our input
    
    for tok in lexer: # get and output the sequence of tokens
        print(tok)



if __name__ == "__main__":
    main()
