'''
import pygame

from BoggleSolver import BoggleSolver
from BoggleBoard import BoggleBoard

# RANDOM TABLE GENERATOR
import random

letters = "ABCDEFGHIJKLMNOPKRSTUVWXZ"

'''
import random
letters = "ABCDEFGHIJKLMNOPKRSTUVWXZ"
def randomBoard(x: int, y : int) -> list[list[chr]]:
    board = [[None] * y for _ in range(x)]

    for i in range(x):
        for j in range(y):
            board[i][j] = random.choice(letters)

    return board

def printBoard(board):
    for i in board:
        print(i)

# CREATE BOGGLE TABLE
'''
table = [['X', 'E', 'H', 'E'],
         ['J', 'L', 'F', 'V'],
         ['D', 'E', 'R', 'L'],
         ['I', 'M', 'M', 'O']]
'''


'''
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
'''

from BoggleBoard import BoggleBoard
import pygame
from pygame.locals import *
import os
import sys


table = randomBoard(4,4)
board = BoggleBoard(table)


# -----------
# Constantes
# -----------

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
DIR = "..\sprites"
IMAGE_DIM = 60


# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:

class Letter(pygame.sprite.Sprite):
    _letter = None

    def __init__(self, letter: chr):
        self._letter = letter.upper()
        image = "letter_" + self._letter + ".png"
        self.image = load_image(image, DIR + "\Box", alpha=True)
        self.scale(IMAGE_DIM, IMAGE_DIM)
        self.rect = self.image.get_rect()

    def scale(self, w: int, h: int):
        self.image = pygame.transform.scale(self.image, (w, h))

    def position(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y


class Board:

    def __init__(self, board: BoggleBoard):
        self.rows = board.rows()
        self.cols = board.cols()
        self.board = [[None] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = Letter(board.getLetter(i, j))

    def calcPos(self):
        centery = SCREEN_HEIGHT / 2
        centerx = SCREEN_WIDTH / 2

        y = centery - (self.cols/2)*IMAGE_DIM
        x = centerx - (self.rows/2)*IMAGE_DIM

        b = y
        for i in range(self.rows):
            a = x
            for j in range(self.cols):
                self.board[i][j].position(a, b)
                a += IMAGE_DIM
            b += IMAGE_DIM

    def display(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                win.blit(self.board[i][j].image, self.board[i][j].rect)



# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ejemplo de un Pong Simple")

    # cargamos los objetos
    letter = Letter('A')
    b = Board(board)
    b.calcPos()

    # el bucle principal del juego
    while True:
        b.display(screen)
        pygame.display.flip()

        # Actualizamos los obejos en pantalla

        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # actualizamos la pantalla
