# -*- coding: utf-8 -*-
"""
Created: Mar 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

============================================================================
Note that this code is intended for educational purposes. It is deliberately 
simplified in order to improve readability and facilitate understanding 
for students.
============================================================================

A straightforward Python implementation of a parser  
for a very simple arithmetic expression language.
"""

from enum import Enum


class TokenType(Enum):
    ADD = 1, # +
    SUB = 2, # -
    MUL = 3, # *
    DIV = 4, # /
    NUMBER = 5,
    LBRACKET = 6, # (
    RBRACKET = 7 # )


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        
    def __repr__(self):
        return f"({self.type.name})"
    
class TokenLBracket(Token):
    def __init__(self):
        super().__init__(TokenType.LBRACKET)

class TokenRBracket(Token):
    def __init__(self):
        super().__init__(TokenType.RBRACKET)
        
class TokenAdd(Token):
    def __init__(self):
        super().__init__(TokenType.ADD)
        
class TokenSub(Token):
    def __init__(self):
        super().__init__(TokenType.SUB)
        
class TokenMul(Token):
    def __init__(self):
        super().__init__(TokenType.MUL)
        
class TokenDiv(Token):
    def __init__(self):
        super().__init__(TokenType.DIV)
        
class TokenNumber(Token):
    def __init__(self, value):
        super().__init__(TokenType.NUMBER, value)
        
    def __repr__(self):
        return f"({self.type.name}, {self.value})"



class Scanner:
    
    def scan(self, s):
        print("Starting lexical analysis...")
        self.tokenList = []
        i = 0
        while True:
            # analyze if s[i] is a number, `+', `-',
            # or something else?
            
            if (i == len(s)):
                print(f"Lexical analysis is finished with {len(self.tokenList)} tokens.")
                break
            if (s[i].isdigit()): 
                # read digits until a non-digit character appears or the input ends
                num = s[i]
                j = i + 1
                while(j < len(s)):
                    if(s[j].isdigit()):
                        num += s[j]
                    else:
                        break
                    j += 1
                    
                i = j - 1
                self.tokenList.append(TokenNumber(num))
         
            elif (s[i] == '+'):
                self.tokenList.append(TokenAdd())
            elif (s[i] == '-'):
                self.tokenList.append(TokenSub())
            elif (s[i] == '*'):
                self.tokenList.append(TokenMul())
            elif (s[i] == '/'):
                self.tokenList.append(TokenDiv())
            elif (s[i] == '('):
                self.tokenList.append(TokenLBracket())
            elif (s[i] == ')'):
                self.tokenList.append(TokenRBracket())
            else:
                raise ValueError(f"Invalid input `{s[i]}' at position {i}")
            
            i += 1

        return self.tokenList
    

# a very simple handwritten recursive descent parser
class Parser:
    
    NONE_PAIR = (None, None)
    
    # CFG rules:
    # P -> E
    # E -> E + T | E - T | T
    # T -> T * F | T / F | F
    # F -> (E) | number
    
    def parse(self, tokens):
        print("Parsing the code...")
        p, val = self.parseE(tokens, 0)
        if p is not None and p == len(tokens):
            return val
        return None

    def parseE(self, tokens, p):
        
        p, val = self.parseT(tokens, p)
        
        if p is None:
            return Parser.NONE_PAIR
        
        sum = val
        
        while True:
            if self.match(TokenType.ADD, tokens, p):
               p, val = self.parseT(tokens, p+1)
               if p is None:
                   return Parser.NONE_PAIR
               sum += val
            elif self.match(TokenType.SUB, tokens, p):
                p, val = self.parseT(tokens, p+1)
                if p is None:
                    return Parser.NONE_PAIR
                sum -= val
            else:
                break
        return (p, sum)
    
    
    def parseT(self, tokens, p):
        p, val = self.parseF(tokens, p)
        if p is None:
            return Parser.NONE_PAIR
        
        prod = val
        
        while True:
            if self.match(TokenType.MUL, tokens, p):
                p, val = self.parseF(tokens, p+1)
                if p is None:
                    return Parser.NONE_PAIR
                prod *= val
            elif self.match(TokenType.DIV, tokens, p):
                p, val = self.parseF(tokens, p+1)
                if p is None:
                    return Parser.NONE_PAIR
                if val == 0:
                    raise ZeroDivisionError(f"Division by 0 at {p}!")
                prod /= val
            else:
                break
        return (p, prod)
  
    def parseF(self, tokens, p):
        if self.match(TokenType.LBRACKET, tokens, p):
            p, val = self.parseE(tokens, p+1)
            if p is not None and self.match(TokenType.RBRACKET, tokens, p):
                return (p+1,val)
            return Parser.NONE_PAIR

        if self.match(TokenType.NUMBER, tokens, p):
            return (p+1, int(tokens[p].value))

        return Parser.NONE_PAIR
    

    def match(self, tokenType, tokens, p):
       return p < len(tokens) and tokens[p].type == tokenType


        
def main():
    
    # in the future, we are going to read it from an external file 
    # or from the command line
    input = '13+24*(711-993)+33+56/(621-9942)+3564*13+42/712-994'

    scn = Scanner()
    tokenList = scn.scan(input)
    print(tokenList)
    prc = Parser()
    isCorrectProgram = prc.parse(tokenList)
    
    print("Result:", isCorrectProgram)


if __name__ == "__main__":
    main()



