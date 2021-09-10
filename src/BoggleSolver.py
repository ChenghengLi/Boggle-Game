from BoggleBoard import BoggleBoard


class Node:
    def __init__(self, r: int):
        self.inDict = False
        self.hijos = [None] * r


class BoggleSolver:
    _R = 26
    _A = ord("A")
    _valid = set()
    _root = Node(_R)

    def __init__(self, dictionary: list[str]):
        for string in dictionary:
            self._add(string)

    # Make R statatic
    @classmethod
    def getR(cls):
        return cls._R

    # CONSTRUCTION OF RX TRIE

    # CHAR AT function
    def _charAt(self, s: str, i: int):
        return ord(s[i]) - self._A

    # RX TRIE ADD function
    def _add(self, s: str):

        def add(node: Node, s: str, d: int) -> Node:
            if node is None:
                node = Node(self._R)

            if len(s) == d:
                node.inDict = True
                return node

            pos = self._charAt(s, d)
            node.hijos[pos] = add(node.hijos[pos], s, d + 1)

            return node

        self._root = add(self._root, s, 0)

    # RX TRIE SEARCH function
    def _search(self, node: Node, s: str, d: int) -> Node:
        if node is None:
            return None

        if len(s) == d:
            return node

        pos = self._charAt(s, d)

        return self._search(node.hijos[pos], s, d + 1)

    # USEFUL FUNCTION TO GET ALL VALID WORDS

    # IS PREFIX? Function that checks if the word is a prefix of a word in the dict
    def _isPrefix(self, s: str) -> bool:
        return self._search(self._root, s, 0) is not None

    # IS WORD? Function that checks if the word is in the dict
    def _isWord(self, s: str) -> bool:
        node = self._search(self._root, s, 0)
        return False if node is None else node.inDict

    # DFS function, searches all valid words
    def _dfs(self, board: BoggleBoard, x: int, y: int):

        rows = board.rows()
        cols = board.cols()
        marked = [[False] * cols for _ in range(rows)]

        def neighbour(x: int, y: int):
            for i, j in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1),
                         (x + 1, y - 1)):
                if i < 0 or j < 0 or i >= rows or j >= cols:
                    continue
                yield i, j

        def dfs(s: str, x: int, y: int):
            marked[x][y] = True

            if self._isWord(s) and len(s) > 2:
                self._valid.add(s)

            for i, j in neighbour(x, y):
                if not marked[i][j]:
                    word = s + board.getLetter(i, j)
                    if self._isPrefix(word):
                        dfs(word, i, j)

            marked[x][y] = False

        dfs(board.getLetter(x, y), x, y)

    # PUBLIC METHODS
    def getAllWords(self, board: BoggleBoard) -> set:

        self._valid = set()

        rows = board.rows()
        cols = board.cols()

        for x in range(rows):
            for y in range(cols):
                self._dfs(board, x, y)

        return self._valid

    def scoreOf(self, s: str):
        pass

    def highestScore(self):
        score = 0
        for i in self._valid:
            score += self.scoreOf(i)
        return score
