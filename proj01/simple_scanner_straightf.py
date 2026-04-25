# -*- coding: utf-8 -*-
"""
Created: Mar 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

============================================================================
Note that this code is intended for educational purposes. It is deliberately 
simplified in order to improve readability and facilitate understanding 
for students.
============================================================================

A straightforward Python implementation of a scanner 
for a very simple arithmetic expression language.
"""

from enum import Enum


class TokenType(Enum):
    ADD = 1, # +
    SUB = 2, # -
    MUL = 3, # *
    DIV = 4, # /
    NUMBER = 5


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        
    def __repr__(self):
        return f"({self.type.name})"
        
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
            else:
                raise ValueError(f"Invalid input `{s[i]}' at position {i}")
            
            i += 1

        return self.tokenList
    


def main():
    
    # in the future, we are going to read it from an external file 
    # or from the command line
    input = '13+24*711-993+33+56*621-99423564+13+42/712-994'

    scn = Scanner()
    tokenList = scn.scan(input)
    print(tokenList)
        


if __name__ == "__main__":
    main()



