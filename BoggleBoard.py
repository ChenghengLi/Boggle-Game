class BoggleBoard:

    _board = None
    _rows = 0
    _cols = 0

    def __init__(self, board : list[list[chr]]):
        self._board = board
        self._rows = len(board[0])
        self._cols = len(board)

    def getLetter(self, x : int, y : int):
        return self._board[x][y]

    def rows(self):
        return self._rows

    def cols(self):
        return self._cols