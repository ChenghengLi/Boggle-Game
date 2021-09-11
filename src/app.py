'''
import pygame

from BoggleSolver import BoggleSolver
from BoggleBoard import BoggleBoard

# RANDOM TABLE GENERATOR
import random

letters = "ABCDEFGHIJKLMNOPKRSTUVWXZ"

'''
import random

letters = "AAAAABCDEEEEEEFGHIIIIJKLMNOOOOPKRSTUUUUVWXZ"


def randomBoard(x: int, y: int) -> list[list[chr]]:
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






from BoggleBoard import BoggleBoard
from BoggleSolver import BoggleSolver
import pygame
from pygame.locals import *
import os
import sys

table = randomBoard(4, 4)
board = BoggleBoard(table)

# -----------
# Constantes
# -----------
from functools import lru_cache
# READ DICTIONARY WORD

def read():
    f = open("..\dict.txt")
    LIST = list()
    for line in f:
        if line is None or line == "":
            continue
        LIST.append(line.strip())
    return LIST

LIST = read()
BS = BoggleSolver(LIST)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
DIR = "..\images"
S_DIR = "..\sounds"
IMAGE_DIM = 60
LINE_COLOR = Color(12,233,249)
BLACK = Color(0,0,0)
RED = Color(255,0,0)


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

def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
        print("No se pudo cargar el sonido:" + ruta)
        sonido = None
    return sonido


# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:

class Letter(pygame.sprite.Sprite):

    letter = None
    _skins = None
    selected = False

    def __init__(self, letter: chr):
        self.letter = letter.upper()
        image = "letter_" + self.letter + ".png"
        self._skins = list()
        self._skins.append(load_image(image, DIR + "\Box", alpha=True))
        self._skins.append(load_image(image, DIR + "\Metal", alpha=True))
        self._skins.append(load_image(image, DIR + "\Marble", alpha=True))
        self.selected = False
        self.skinUpdate()
        self.rect = self.image.get_rect()

    def scale(self, w: int, h: int):
        self.image = pygame.transform.scale(self.image, (w, h))

    def skinUpdate(self, skin: int = -1):
        if skin == 0:
            self.image = self._skins[0]
        elif skin == 1:
            self.image = self._skins[1]
        elif skin == 2:
            self.image = self._skins[2]
        else:
            if self.selected == False:
                self.image = self._skins[0]
            else:
                self.image = self._skins[1]
        self.scale(IMAGE_DIM, IMAGE_DIM)

    def position(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y


class Board:

    centery = SCREEN_HEIGHT/2
    centerx = SCREEN_WIDTH/2
    last = None
    word = ""
    wordList = set()
    sound = dict()

    @classmethod
    def addSound(cls, name: str, s: pygame.mixer.Sound):
        cls.sound[name] = s

    @classmethod
    def setY(cls, y: int):
        cls.centery = y

    @classmethod
    def setX(cls, x: int):
        cls.centerx = x

    def __init__(self, board: BoggleBoard):

        print(BS.getAllWords(board))

        self.rows = board.rows()
        self.cols = board.cols()
        self.board = [[None] * self.cols for _ in range(self.rows)]

        self.addSound("correct",load_sound("correcto.mp3", S_DIR))
        self.addSound("incorrect", load_sound("incorrecto.mp3", S_DIR))

        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = Letter(board.getLetter(i, j))

    def calcPos(self):

        y = self.centery - (self.cols / 2) * IMAGE_DIM
        x = self.centerx - (self.rows / 2) * IMAGE_DIM

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


    def _check(self, x: int, y: int):
        def neighbour(x: int, y: int):
            for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1),
                         (x + 1, y - 1)):
                if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
                    continue
                yield i, j

        for i, j in neighbour(x, y):

            if i == self.last[0] and j == self.last[1] and self.board[x][y].selected == False:
                return True

        return False

    def _drawLine(self):
        pass

    def update(self, event, win,showWord, showPoints ):
        if event.button == 1:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j].rect.collidepoint(event.pos):
                        if self.last is None:
                            self.word += self.board[i][j].letter
                            self.board[i][j].selected = True
                            self.board[i][j].skinUpdate(2)
                            self.last = [i, j]
                        elif self._check(i, j):
                            self.word += self.board[i][j].letter
                            self.board[i][j].selected = True
                            self.board[self.last[0]][self.last[1]].skinUpdate()
                            self.board[i][j].skinUpdate(2)
                            self.last[0], self.last[1] = i, j

        elif event.button == 3:
            if self.word in self.wordList:
                self.sound["incorrect"].play()
                for row in self.board:
                    for item in row:
                        item.selected = False
                        item.skinUpdate()
                self.word = ""
                self.last = None
                showWord.setWord(self.word)
                return
            print(self.word)
            print(BS.scoreOf(self.word))
            showPoints.sumPoints(BS.scoreOf(self.word))
            if BS.scoreOf(self.word) == 0:
                self.sound["incorrect"].play()
            else:
                self.sound["correct"].play()
            self.wordList.add(self.word)
            self.word = ""
            self.last = None
            for row in self.board:
                for item in row:
                    item.selected = False
                    item.skinUpdate()

        showWord.setWord(self.word)



class ShowWord:

    def __init__(self):
        self.font = pygame.font.Font("o.ttf",32)
        self.score = self.font.render("Word : ", 10, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - 40

    def display(self, win):
        win.blit(self.score, self.rect)

    def setWord(self, s: str, valid: bool = True):
        self.score = self.font.render("Word : " + s, 10, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - 40


class ShowPoints:

    def __init__(self):
        self.points = 0
        self.font = pygame.font.Font("o.ttf", 32)
        self.score = self.font.render("Points: " + str(self.points), 10, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.y = SCREEN_HEIGHT - 85

    def display(self, win):
        win.blit(self.score, self.rect)

    def sumPoints(self, s: int):
        self.points += s
        self.score = self.font.render("Points: " + str(self.points), 10, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - 85


# Displays points and word

class SubMenu(pygame.sprite.Sprite):

    showWord = None
    showPoints = None

    def __init__(self, showWord, showPoints):
        self.image = load_image("subMenu.png", DIR, False)
        self.showWord = showWord
        self.showPoints = showPoints
        self.scale(SCREEN_WIDTH, 100)

    def display(self, win):
        win.blit(self.image, (0, SCREEN_HEIGHT - 100))
        self.showPoints.display(win)
        self.showWord.display(win)

    def scale(self, w: int, h: int):
        self.image = pygame.transform.scale(self.image, (w, h))

class TopMenu(pygame.sprite.Sprite):
    pass




class Backgroud(pygame.sprite.Sprite):

    def __init__(self, text):
        self.image = load_image(text, DIR)
        self.rect = self.image.get_rect()

    def display(self, win):
        win.blit(self.image, self.rect)

    def setPos(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y

    def scale(self, w: int, h: int):
        self.image = pygame.transform.scale(self.image, (w, h))


# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boggle Game")


    # cargamos los objetos
    bg = Backgroud("background.png")
    bg.scale(SCREEN_WIDTH, SCREEN_HEIGHT)
    b = Board(board)
    b.calcPos()
    a = ShowWord()
    c= ShowPoints()
    showMenu = SubMenu(a, c)

    # el bucle principal del juego
    while True:
        # Actualizamos los obejos en pantalla
        bg.display(screen)
        b.display(screen)
        showMenu.display(screen)
        pygame.display.flip()
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                b.update(event, screen, a, c)

            if event.type == pygame.QUIT:
                sys.exit(0)

        # actualizamos la pantalla
