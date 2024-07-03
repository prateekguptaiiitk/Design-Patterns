from enum import Enum

class PieceType(Enum):
	X = 'X'
	O = 'O'

class PlayingPiece():
	pieceType = None

	def __init__(self, pieceType):
		self.pieceType = pieceType

class PlayingPieceX(PlayingPiece):
	def __init__(self):
		super().__init__(PieceType.X)

class PlayingPieceO(PlayingPiece):
	def __init__(self):
		super().__init__(PieceType.Y)

class Board():
	size = 0
	board = None

	def __init__(self, size):
		self.size = size
		self.board = [[None] * (size)] * (size)

	def addPiece(self, row, col, playingPiece):
		if board[row][col]:
			return False

		board[row][col] = playingPiece
		return True

	def getFreeCells(self):
		freeCells = []

		for i in range(size):
			for j in range(size):
				if not board[i][j]:
					freeCells.add((i, j))

		return freeCells

class Player():
	_name = None
	_playingPiece = None

	def __init__(self, name, playingPiece):
		self._name = name
		self._playingPiece = playingPiece

	def getName(self):
		return self._name

	def setName(self, name):
		self._name = name

	def getPlayingPiece(self):
		return self._playingPiece

	def setPlayingPiece(self, playingPiece):
		self._playingPiece = playingPiece

from collections import deque
class TicTacToeGame():
	players = deque()
	gameBoard = None

	def __init__(self):
		self.initializeGame()

	def initializeGame(self):
		crossPiece = PlayingPieceX()
		player1 = Player('Player1', crossPiece)

		noughtsPiece = PlayingPieceO()
		player2 = Player('Player2', noughtsPiece)

		self.players.append(player1)
		self.players.append(player2)

		self.gameBoard = Board(3)

	def startGame(self):
		noWinner = True

		while noWinner:
			# take out the player whose turn is and also put at the back of the list
			playerTurn = self.players.popleft()

			# get the free space from the board
			gameBoard.printBoard()
			freeSpaces = gameBoard.getFreeCells()
			if len(freeSpaces) == 0:
				noWinner = False
				continue

			# read the user input
			s = input('Player:', playerTurn._name, ' Enter row, column: ')
			
