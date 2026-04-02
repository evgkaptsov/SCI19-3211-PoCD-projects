# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 10:44:47 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

A syntax-directed translator for simple mazes described using the recursive division algorithm. 
The basic grammar, along with commentary, can be found in:

Kaptsov, E. I. Lecture Notes on Theory of Computation (SCI19 2113), 2025.
Suranaree University of Technology (SUT e-Learning+), 162 pp.

Initially, the following left-recursive grammar is used:

Level -> Size Room
Room -> [Div Room Room]
Room -> [{Doors}{Objects}]
Div -> v | h
Doors -> Doors Door | epsilon
Door -> l | r | t | b
Objects -> Objects Object | epsilon
Object -> hero | enemy | coin | portal | goal
Size -> [0-9]+

This grammar is then transformed into LL(1) form, and a corresponding parser is implemented. 

This code is intended for educational purposes. It is deliberately simplified in order to improve readability and facilitate understanding for students.
"""


# include standard PLY Lex package
import ply.lex as lex
import tkinter as tk
from pyrect import Rect
from collections import deque


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
    
    WALL_COLOR = "#aaaaaa"
    
    def __init__(self, tkRoot):
        self.tokens = deque()
        self.tkRoot = tkRoot
        
    def nextToken(self):
        return self.tokens.popleft()
    
    def putTokenBack(self, tok):
        self.tokens.appendleft(tok)
        
    def match(self, tok, tokenType):
        if tok.type != tokenType:
            raise ValueError(f"Unexpected token: {tok.type} instead of {tokenType}")
        
    def matchNext(self, tokenType):
        self.match(self.nextToken(), tokenType)
    
    def parse(self, input):
        
        lexer = lex.lex()
        lexer.input(input)
        self.tokens = deque()
        
        for tok in lexer:
            self.tokens.append(tok)
        
        self.parse_Level()
            
    def parse_Level(self):
        rect = self.parse_Size()
        self.parse_Room(rect)
        print("A level has parsed successfully.")
        
    def parse_Size(self):
        
        tok = self.nextToken()
        self.match(tok, 'SIZE')
        
        # action
        size = int(tok.value)
        self.size = size
        
        offset = 25
        self.canvas = tk.Canvas(self.tkRoot, width=size+2*offset, height=size+2*offset)
        self.canvas.pack()
        
        rect = Rect(offset, offset, size, size)
        self.canvas.config(bg="black")
        self.canvas.create_rectangle(
            rect.left, 
            rect.top, 
            rect.right, 
            rect.bottom, fill="white", outline=MazeSDT.WALL_COLOR, width=8)
        
        print(f"Level size: {self.size} x {self.size}." )
        # /action
        
        return rect

    
    def parse_Room(self, rect):
        self.matchNext('LSQBRACKET')
        self.parse_Room1(rect)
        
    def parse_Room1(self, rect):
        tok = self.nextToken()
        if tok.type == 'DIV':
            rects = self.parse_Div(tok, rect)
            self.parse_Room(rects[0])
            self.parse_Room(rects[1])
        else:
            #print("parsing Doors and Objects")
            self.match(tok, 'LCBRACKET')
            self.parse_Doors(rect)
            self.matchNext('RCBRACKET')
            self.matchNext('LCBRACKET')
            self.parse_Objects(rect)
            self.matchNext('RCBRACKET')

        self.matchNext('RSQBRACKET')
        
    def parse_Doors(self, rect):
        tok = self.nextToken()
        if tok.type == 'DOOR':
            self.parse_Door(tok, rect)
            self.parse_Doors(rect)
        else:
            self.putTokenBack(tok)
    
    def parse_Door(self, tok, rect):
        print(f"Door: {tok.value}")
        
        # action
        hw = rect.width * 0.12
        hh = rect.height * 0.12
        params = dict(width=8, fill="white")
        
        if tok.value == "l":
            self.canvas.create_line(
                rect.left, 
                rect.centery - hh, 
                rect.left, 
                rect.centery + hh, **params)
        elif tok.value == "r":
            self.canvas.create_line(
                rect.right, 
                rect.centery - hh, 
                rect.right, 
                rect.centery + hh, **params)
        elif tok.value == "t":
            self.canvas.create_line(
                rect.centerx - hw, 
                rect.top, 
                rect.centerx + hw, 
                rect.top, **params)
        else: # b
            self.canvas.create_line(
                rect.centerx - hw, 
                rect.bottom, 
                rect.centerx + hw, 
                rect.bottom, **params)
        # /action
        
        self.match(tok, 'DOOR')
    
    def parse_Div(self, tok, rect):
        print(f"Div: {tok.value}")
        
        # action
        wall_width = 4
        if tok.value == 'v': #vert
            hw = rect.centerx - rect.left
            rect1 = Rect(rect.left, rect.top, hw, rect.height)
            rect2 = Rect(rect.centerx, rect.top, hw, rect.height)
            self.canvas.create_line(
                rect.centerx, 
                rect.top, 
                rect.centerx, 
                rect.bottom, fill=MazeSDT.WALL_COLOR, width=wall_width)
        else: # horiz
            hh = rect.centery - rect.top
            rect1 = Rect(rect.left, rect.top, rect.width, hh)
            rect2 = Rect(rect.left, rect.centery, rect.width, hh)
            self.canvas.create_line(
                rect.left, 
                rect.centery, 
                rect.right, 
                rect.centery, fill=MazeSDT.WALL_COLOR, width=wall_width)
        # /action
        
        self.match(tok, 'DIV')
        
        return [rect1, rect2]
        
    
    def parse_Objects(self, rect, n=0):
        tok = self.nextToken()
        if tok.type == 'OBJECT':
            self.parse_Object(tok, rect, n)
            self.parse_Objects(rect, n+1)
        else:
            self.putTokenBack(tok)
    
    def parse_Object(self, tok, rect, n):
        print(f"Object: {tok.value}")
        
        # action
        
        objSize = 25
        objOffset = 10
        obj_l = rect.left + n * objSize + (n+1) * objOffset
        obj_t = rect.top + n * objSize + (n+1) * objOffset
        obj_r = obj_l + objSize
        obj_b = obj_t + objSize
        
        if tok.value == "coin":
            self.canvas.create_oval(obj_l, obj_t, obj_r, obj_b, fill="yellow", outline="black")
        elif tok.value == "enemy":
            self.canvas.create_oval(obj_l, obj_t, obj_r, obj_b, fill="red", outline="black")
        elif tok.value == "portal":
            self.canvas.create_rectangle(obj_l, obj_t, obj_r, obj_b, fill="cyan", outline="black")
        elif tok.value == "hero":
            self.canvas.create_polygon([
                    obj_l + 0.5 * objSize, obj_t, 
                    obj_l + objSize, obj_b,
                    obj_l, obj_b,
                ], 
                fill="green", outline="black")
        elif tok.value == "goal":
            self.canvas.create_polygon([
                    obj_l, obj_t, 
                    obj_r, 0.5 * (obj_t + obj_b),
                    obj_l, obj_b
                ], 
                fill="red", outline="black")
            self.canvas.create_line(obj_l, obj_t, obj_l, obj_b + objSize*0.5)
            
        # /action
        
        self.match(tok, 'OBJECT')
    



def main():
    
    levelDescription = '''500
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
    
    
    tkRoot = tk.Tk()
    tkRoot.title("Maze (SCI19 3211)")
    
    maze = MazeSDT(tkRoot)
    maze.parse(levelDescription)
    
    tkRoot.mainloop()



if __name__ == "__main__":
    main()
