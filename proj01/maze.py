# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 10:44:47 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)
"""

# include standard PLY Lex package
import ply.lex as lex
import tkinter as tk
from pyrect import Rect


tokens = [
    'SIZE',
    'LCBRACKET',
    'RCBRACKET',
    'LSQBRACKET',
    'RSQBRACKET',
    'DIV',
    'DOOR',
    'OBJECT'
]

t_SIZE = r'[0-9]+'
t_LCBRACKET = r'\{'
t_RCBRACKET = r'\}'
t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_DIV = r'v|h'
t_DOOR = r'l|r|t|b'
t_OBJECT = 'hero|goal|enemy|coin|portal'


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
    
    
class MazeSDT:
    
    def __init__(self, lexer, tkRoot):
        self.lexer = lexer
        self.tkRoot = tkRoot
        self.lookahead = None
        
    def nextToken(self):
        if self.lookahead is None:    
            self.lookahead = self.lexer.token()
        return self.lookahead
    
    def putTokenBack(self, tok):
        #print(f"lookahead = {tok}")
        self.lookahead = tok
        
    def match(self, tok, tokenType):
        if tok.type != tokenType:
            raise ValueError(f"Unexpected token: {tok.type} instead of {tokenType}")
        self.lookahead = None
        
    def matchNext(self, tokenType):
        self.match(self.nextToken(), tokenType)
    
    def parse(self, input):
        self.lexer.input(input)
        self.parse_Level()
            
    def parse_Level(self):
        self.parse_Size()
        self.parse_Room()
        
    def parse_Size(self):
        
        tok = self.nextToken()
        self.match(tok, 'SIZE')
        
        size = int(tok.value)
        self.size = size
        #print(f"Level size: {self.size} x {self.size}." )
        
        offset = 25
        self.canvas = tk.Canvas(self.tkRoot, width=size+2*offset, height=size+2*offset)
        self.canvas.pack()
        
        self.rect = Rect(offset, offset, size, size)
        
        print(f"rect: {self.rect.left}, {self.rect.top}, {self.rect.right}, {self.rect.bottom}")
        
        self.canvas.create_rectangle(
            self.rect.left, 
            self.rect.top, 
            self.rect.right, 
            self.rect.bottom)

    
    def parse_Room(self):
        self.matchNext('LSQBRACKET')
        self.parse_Room1()
        
    def parse_Room1(self):
        tok = self.nextToken()
        if tok.type == 'DIV':
            #print("parsing Div")
            self.parse_Div(tok)
            self.parse_Room()
            self.parse_Room()
        else:
            #print("parsing Doors and Objects")
            self.match(tok, 'LCBRACKET')
            self.parse_Doors()
            self.matchNext('RCBRACKET')
            self.matchNext('LCBRACKET')
            self.parse_Objects()
            self.matchNext('RCBRACKET')

        self.matchNext('RSQBRACKET')
        
    def parse_Doors(self):
        tok = self.nextToken()
        if tok.type == 'DOOR':
            self.parse_Door(tok)
            self.parse_Doors()
        else:
            self.putTokenBack(tok)
    
    def parse_Door(self, tok):
        print(f"Door: {tok.value}")
        self.match(tok, 'DOOR')
    
    def parse_Div(self, tok):
        print(f"Div: {tok.value}")
        self.match(tok, 'DIV')
    
    def parse_Objects(self):
        tok = self.nextToken()
        if tok.type == 'OBJECT':
            self.parse_Object(tok)
            self.parse_Objects()
        else:
            self.putTokenBack(tok)
    
    def parse_Object(self, tok):
        print(f"Object: {tok.value}")
        self.match(tok, 'OBJECT')
    



def main():
    
    input = '''600
    [v
         [h
          [{r}{coin}]
          [{t}{hero portal}]
         ]
        [v
         [{}{portal}]
         [h
              [{l}{coin coin enemy}]
              [{t}{enemy goal}]
         ]
        ]
    ]
    '''
    
    lexer = lex.lex()
    
    
    tkRoot = tk.Tk()
    
    maze = MazeSDT(lexer, tkRoot)
    maze.parse(input)
    
    tkRoot.mainloop()



if __name__ == "__main__":
    main()
