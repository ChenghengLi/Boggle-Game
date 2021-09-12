import random
from BoggleBoard import BoggleBoard

class BoardCreator:
    letters = "AAAAABCDEEEEEEFGHIIIIJKLMNOOOOPKRSTUUUUVWXZ"

    @classmethod
    def randomBoard(cls, size: int):
        board = [[None] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                board[i][j] = random.choice(cls.letters)

        return BoggleBoard(board)

    @classmethod
    def _getLetters(cls):
        return cls.letters