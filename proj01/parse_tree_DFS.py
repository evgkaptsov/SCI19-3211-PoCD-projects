# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 23:05:21 2026

@author: Dr. Evgenii Kaptsov for SCI19 3211 (Principles of Compiler Design)

============================================================================
Note that this code is intended for educational purposes. It is deliberately 
simplified in order to improve readability and facilitate understanding 
for students.
============================================================================

The program constructs a parse trees and then traverses them using the DFS 
algorithm in two ways: printing all nodes to the console (dfs) and printing 
only the terminal string (the leaves of the tree) to the console (dfs_term). 
Both preorder and postorder DFS traversals are used. Two examples are provided: 

1) a language of strings of the form 0^n 1^n 
(such as 01, 0011, 000111, 00001111, etc.);

2) a simple arithmetic expression language, for example, 1+2*3.
    
"""

eps = "epsilon"

class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []


# DFS traversal (preorder)
def dfs_preorder(node, depth=0):
    print('-' * depth + node.label)
    for child in node.children:
        dfs_preorder(child, depth + 1)

# DFS traversal (postorder)
def dfs_postorder(node, depth=0):
    for child in node.children:
        dfs_postorder(child, depth + 1)
    print('-' * depth + node.label)
        
# DFS traversal (preorder) with printing only terminals
def dfs_term_preorder(node):    
    for child in node.children:
        dfs_term_preorder(child)
    if len(node.children) == 0 and node.label != eps:
        print(node.label, end='')
        
# DFS traversal (postorder) with printing only terminals
def dfs_term_postorder(node):    
    for child in node.children:
        dfs_term_postorder(child)
    if len(node.children) == 0 and node.label != eps:
        print(node.label, end='')

        
#################################################
# Consider the grammar D = {0^n 1^n | n >= 1 }:
# S -> 0S1 
# S -> R 
# R -> epsilon
#
# Construct a simple tree for 000111
#
def language_0n1n_example_tree():
    # Construct parse tree for 000111
    # S -> 0 S 1 -> 0 (0 S 1) 1 -> 0 (0 (0 S 1) 1) 1
    # final: S -> R -> epsilon
    return Node('S', [
        Node('0'),
        Node('S', [
            Node('0'),
            Node('S', [
                Node('0'),
                Node('S', [
                    Node('R', [
                        Node(eps)
                    ])
                ]),
                Node('1')
            ]),
            Node('1')
        ]),
        Node('1')
    ])


#################################################
# Consider the grammar following simple 
# grammar for arithmetic expressions:
# E -> E + T | T
# T -> T * F | F
# F -> num
# num -> 1|2|3|4|5|6|7|8|9
#
# Construct parse tree for: 1 + 2 * 3
#
def language_arithmetic_example_tree():
    return Node('E', [
        Node('E', [
            Node('T', [
                Node('F', [Node('1')])
            ])
        ]),
        Node('+'),
        Node('T', [
            Node('T', [
                Node('F', [Node('2')])
            ]),
            Node('*'),
            Node('F', [Node('3')])
        ])
    ])



def traverse(tree):
    print("=========================")
    print("Preorder DFS with printing all the nodes:")
    dfs_preorder(tree)

    print("\nPostorder DFS with printing all the nodes:")
    dfs_postorder(tree)
    
    print("\nPreorder DFS with printing terminals only:")
    dfs_term_preorder(tree)
    print()

    print("\nPostorder DFS with printing terminals only:")
    dfs_term_postorder(tree)
    print("\n=========================")


def main():

    print("Example 1: Language {0^n 1^n}")
    tree1 = language_0n1n_example_tree()
    traverse(tree1)
    
    print("Example 2: Language of arithmetic expressions")
    tree2 = language_arithmetic_example_tree()
    traverse(tree2)
    
    
    

####################################
if __name__ == "__main__":
    main()

