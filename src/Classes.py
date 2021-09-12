from BoggleBoard import BoggleBoard
from BoggleSolver import BoggleSolver
from BoggleCreator import BoardCreator
import pygame
from pygame.locals import *
import os
import sys

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
LINE_COLOR = Color(12, 233, 249)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)


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
    centery = SCREEN_HEIGHT / 2
    centerx = SCREEN_WIDTH / 2
    last = None
    word = ""
    wordList = set()
    sound = dict()

    def __init__(self):
        self.addSound("correct", load_sound("correcto.mp3", S_DIR))
        self.addSound("incorrect", load_sound("incorrecto.mp3", S_DIR))

    @classmethod
    def addSound(cls, name: str, s: pygame.mixer.Sound):
        cls.sound[name] = s

    @classmethod
    def setY(cls, y: int):
        cls.centery = y

    @classmethod
    def setX(cls, x: int):
        cls.centerx = x

    def generateBoard(self, size: int):

        board = BoardCreator.randomBoard(size)

        print(BS.getAllWords(board))

        self.rows = board.rows()
        self.cols = board.cols()
        self.board = [[None] * self.cols for _ in range(self.rows)]

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

    def update(self, event, win, showWord, showPoints):
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
        self.font = pygame.font.Font("o.ttf", 32)
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
        self.rect.centerx = SCREEN_WIDTH / 2
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


class Start(pygame.sprite.Sprite):

    def __init__(self):
        self.image = load_image("play.png", DIR, True)
        self.rect = self.image.get_rect()
        self.setPos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def display(self, win):
        win.blit(self.image, self.rect)

    def setPos(self, x: int, y: int):
        self.rect.centerx = x
        self.rect.centery = y

    def scale(self, w: int, h: int):
        self.image = pygame.transform.scale(self.image, (w, h))


class MaxPoint:
    def __init__(self):
        self.points = list()
        for i in range(3):
            self.points.append(0)
        self.font = pygame.font.Font("o.ttf", 32)
        self.score = self.font.render("Highest score: " + str(self.points[0]), 10, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = 200

    def display(self, win, size: int):
        self.update(size)
        win.blit(self.score, self.rect)

    def update(self, size: int, points: int = -1):
        size = size - 4
        if points > 0:
            self.points[size] = max(self.points[size], points)
        self.score = self.font.render("Highest score: " + str(self.points[size]), 10, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = 200


class ChangeTable:
    def __init__(self):
        self.table = 4
        self.font = pygame.font.Font("o.ttf", 25)
        self.score = self.font.render(self.toString(), 5, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - 85

    def toString(self):
        return "Size of the table (4-6) : " + str(self.table)

    def display(self, win):
        win.blit(self.score, self.rect)

    def update(self, size: int):
        self.table = size
        self.score = self.font.render(self.toString(), 5, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - 85


class Note:
    def __init__(self):
        self.font = pygame.font.Font("o.ttf", 25)
        self.score = self.font.render(self.toString(), 5, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - 115

    def toString(self):
        return "Press 4-6 key to change grid dimension"

    def display(self, win):
        win.blit(self.score, self.rect)


class Instruction1:
    def __init__(self):
        self.font = pygame.font.Font("o.ttf", 25)
        self.score = self.font.render(self.toString(), 5, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = 110

    def toString(self):
        return "Right click to check the word"

    def display(self, win):
        win.blit(self.score, self.rect)


class Instruction2:
    def __init__(self):
        self.font = pygame.font.Font("o.ttf", 25)
        self.score = self.font.render(self.toString(), 5, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = 80

    def toString(self):
        return "Left click to select the word"

    def display(self, win):
        win.blit(self.score, self.rect)


class Instruction3:

    def __init__(self):
        self.font = pygame.font.Font("o.ttf", 25)
        self.score = self.font.render(self.toString(), 5, BLACK)
        self.rect = self.score.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - 145

    def toString(self):
        return "Press Q to quit"

    def display(self, win):
        win.blit(self.score, self.rect)