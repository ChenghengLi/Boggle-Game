# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame


from BoggleSolver import BoggleSolver
from BoggleBoard import BoggleBoard

# CREATE BOGGLE TABLE
table = [['X',  'E',  'H',  'E'],
         ['J',  'L',  'F',  'V'],
         ['D',  'E',  'R',  'L'],
         ['I',  'M',  'M',  'O']]

board = BoggleBoard(table)

# READ DICTIONARY WORD
f = open("dict.txt")
list = list()
for line in f:
    if line is None or line == "":
        continue
    list.append(line.strip())

# CREATE BOGGLE SOLVER
a = BoggleSolver(list)

# PRINT ALL POSSIBLE WORDS
print(sorted(a.getAllWords(board)))









