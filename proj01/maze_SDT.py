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

This grammar is then transformed into LL(1)-friendly form, and a corresponding parser is implemented. 

Note that this code is intended for educational purposes. It is deliberately simplified in order to improve readability and facilitate understanding for students.
"""


# import standard PLY Lex package
import ply.lex as lex
# import tkinter for drawing
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
    t.lexer.skip(1)  # move to the next lexeme


# PLY requires a variable to know which characters to skip
t_ignore = ' \t'  # ignore spaces and tabs

# this function defines how to process new lines


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


class BasicSDT:

    def __init__(self):
        self.tokens = deque()

    def nextToken(self):
        return self.tokens.popleft()

    def putTokenBack(self, tok):
        self.tokens.appendleft(tok)

    def match(self, tok, tokenType):
        if tok.type != tokenType:
            raise ValueError(f"Unexpected token: {
                             tok.type} instead of {tokenType}")

    def matchNext(self, tokenType):
        self.match(self.nextToken(), tokenType)

    def parse(self, input):

        lexer = lex.lex()
        lexer.input(input)
        self.tokens = deque([tok for tok in lexer])


class MazeStyles:

    VIEWPORT_OFFSET = 25

    MAZE_DEFAULT_SIZE = 480
    MAZE_BG_COLOR = "#ddddbb"
    VIEWPORT_BG_COLOR = "#330000"
    WALL_COLOR = "#777777"
    OBJECT_OUTLINE_COLOR = "#444444"

    INNER_WALL_WIDTH = 4
    OUTER_WALL_WIDTH = 8
    DOOR_SIZE_MULT = 0.12

    OBJECT_SIZE = 25
    OBJECT_OFFSET = 10

    OBJ_COIN_COLOR = "#f7d42d"
    OBJ_HERO_COLOR = "#00ff00"
    OBJ_ENEMY_COLOR = "#cc0000"
    OBJ_PORTAL_COLOR = "cyan"
    OBJ_GOAL_COLOR = "#9b1fe8"


class MazeSDT(BasicSDT):

    def __init__(self, tkRoot):
        super().__init__()
        self.tkRoot = tkRoot

    def parse(self, input):
        super().parse(input)
        self.parse_Level()

    def parse_Level(self):
        rect = self.parse_Size()
        self.parse_Room(rect)
        print("A level has parsed successfully.")

    def parse_Size(self):

        tok = self.nextToken()
        self.match(tok, 'SIZE')

        # actions
        rect = self.calcLevelRect(tok.value)
        self.prepareCanvas(rect)
        self.drawLevelBg(rect)

        return rect

    def parse_Room(self, rect):
        self.matchNext('LSQBRACKET')
        self.parse_Room1(rect)

    def parse_Room1(self, rect):
        tok = self.nextToken()
        if tok.type == 'DIV':
            rect1, rect2 = self.parse_Div(tok, rect)
            self.parse_Room(rect1)
            self.parse_Room(rect2)
        else:
            # print("parsing Doors and Objects")
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
        self.drawDoor(rect, tok.value)

        self.match(tok, 'DOOR')

    def parse_Div(self, tok, rect):

        print(f"Div: {tok.value}")

        # action
        match tok.value:
            case 'v':  # vert
                split = self.calcVSplit(rect)
                self.drawVDiv(rect)
            case 'h':
                split = self.calcHSplit(rect)
                self.drawHDiv(rect)

        self.match(tok, 'DIV')

        return split

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
        self.drawObject(tok.value, rect, n)

        self.match(tok, 'OBJECT')

    ################################################
    # semantic actions
    ################################################

    ##### Calculations #####

    def calcVSplit(self, rect):
        hw = rect.centerx - rect.left
        rect1 = Rect(rect.left, rect.top, hw, rect.height)
        rect2 = Rect(rect.centerx, rect.top, hw, rect.height)
        return (rect1, rect2)

    def calcHSplit(self, rect):
        hh = rect.centery - rect.top
        rect1 = Rect(rect.left, rect.top, rect.width, hh)
        rect2 = Rect(rect.left, rect.centery, rect.width, hh)
        return (rect1, rect2)

    def calcLevelRect(self, sizeDesc):

        size = int(sizeDesc)

        if size <= 0 or size > 4096:
            print(
                "WARNING: The specified maze size is out of (0, 4096], so the default size will be set.")
            size = MazeStyles.MAZE_DEFAULT_SIZE

        print(f"Level size: {size} x {size}.")

        return Rect(
            MazeStyles.VIEWPORT_OFFSET,
            MazeStyles.VIEWPORT_OFFSET,
            size,
            size
        )

    ##### Visualization #####

    def prepareCanvas(self, rect):
        self.canvas = tk.Canvas(
            self.tkRoot,
            width=rect.width + 2*MazeStyles.VIEWPORT_OFFSET,
            height=rect.height + 2*MazeStyles.VIEWPORT_OFFSET
        )
        self.canvas.pack()

    def drawVDiv(self, rect):
        self.canvas.create_line(
            rect.centerx,
            rect.top,
            rect.centerx,
            rect.bottom,
            fill=MazeStyles.WALL_COLOR,
            width=MazeStyles.INNER_WALL_WIDTH)

    def drawHDiv(self, rect):
        self.canvas.create_line(
            rect.left,
            rect.centery,
            rect.right,
            rect.centery,
            fill=MazeStyles.WALL_COLOR,
            width=MazeStyles.INNER_WALL_WIDTH)

    def drawLevelBg(self, rect):
        self.canvas.config(bg=MazeStyles.VIEWPORT_BG_COLOR)
        self.canvas.create_rectangle(
            rect.left,
            rect.top,
            rect.right,
            rect.bottom,
            fill=MazeStyles.MAZE_BG_COLOR,
            outline=MazeStyles.WALL_COLOR,
            width=MazeStyles.OUTER_WALL_WIDTH)

    def drawDoor(self, rect, doorType):
        hw = rect.width * MazeStyles.DOOR_SIZE_MULT
        hh = rect.height * MazeStyles.DOOR_SIZE_MULT
        w = 2*MazeStyles.INNER_WALL_WIDTH + 1

        params = dict(width=w, fill=MazeStyles.MAZE_BG_COLOR)

        match doorType:
            case "l":
                self.canvas.create_line(
                    rect.left,
                    rect.centery - hh,
                    rect.left,
                    rect.centery + hh, **params)
            case "r":
                self.canvas.create_line(
                    rect.right,
                    rect.centery - hh,
                    rect.right,
                    rect.centery + hh, **params)
            case "t":
                self.canvas.create_line(
                    rect.centerx - hw,
                    rect.top,
                    rect.centerx + hw,
                    rect.top, **params)
            case "b":
                self.canvas.create_line(
                    rect.centerx - hw,
                    rect.bottom,
                    rect.centerx + hw,
                    rect.bottom, **params)

    def drawObject(self, objType, rect, n):
        outl = MazeStyles.OBJECT_OUTLINE_COLOR
        objSize = MazeStyles.OBJECT_SIZE
        objOffset = MazeStyles.OBJECT_OFFSET
        obj_l = rect.left + n * objSize + (n+1) * objOffset
        obj_t = rect.top + n * objSize + (n+1) * objOffset
        obj_r = obj_l + objSize
        obj_b = obj_t + objSize
        obj_cx = (obj_l + obj_r) // 2
        obj_cy = (obj_t + obj_b) // 2
        fnt = ("Arial", objSize // 2)

        match objType:
            case "coin":
                self.canvas.create_oval(
                    obj_l, obj_t, obj_r, obj_b, fill=MazeStyles.OBJ_COIN_COLOR, outline=outl)
                self.canvas.create_text(obj_cx, obj_cy, text="$", font=fnt)
            case "enemy":
                self.canvas.create_rectangle(
                    obj_l, obj_t, obj_r, obj_b, fill=MazeStyles.OBJ_ENEMY_COLOR, outline=outl)
                self.canvas.create_text(
                    obj_cx, obj_cy, text="^^", font=fnt, fill="white")
            case "portal":
                self.canvas.create_oval(
                    obj_l, obj_t, obj_r, obj_b, fill=MazeStyles.OBJ_PORTAL_COLOR, outline=outl)
                self.canvas.create_text(
                    obj_cx, obj_cy, text="@", font=fnt, fill=MazeStyles.OBJECT_OUTLINE_COLOR)
            case "hero":
                self.canvas.create_polygon([
                    obj_l + objSize // 2, obj_t,
                    obj_l + objSize, obj_b,
                    obj_l, obj_b,
                ],
                    fill=MazeStyles.OBJ_HERO_COLOR, outline=outl)
            case "goal":
                self.canvas.create_polygon([
                    obj_l, obj_t,
                    obj_r, (obj_t + obj_b) // 2,
                    obj_l, obj_b
                ],
                    fill=MazeStyles.OBJ_GOAL_COLOR, outline=outl)
                self.canvas.create_line(
                    obj_l, obj_t, obj_l, obj_b + objSize // 2)


def main():

    levelDescription = '''\
        500
        [v
             [h
              [{r}{coin coin coin}]
              [{t}{hero portal}]
             ]
            [v
             [{}{portal}]
             [h
                  [{l}{coin enemy coin}]
                  [{t}{enemy goal coin}]
             ]
            ]
        ]
    '''

    tkRoot = tk.Tk()
    tkRoot.title("Maze Renderer (SCI19 3211)")

    maze = MazeSDT(tkRoot)
    maze.parse(levelDescription)

    tkRoot.mainloop()


if __name__ == "__main__":
    main()
