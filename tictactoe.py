from enum import Enum

class PieceType(Enum):
	X = 'X'
	O = 'O'

class PlayingPiece():
	def __init__(self, pieceType):
		self.pieceType = pieceType

class PlayingPieceX(PlayingPiece):
	def __init__(self):
		super().__init__(PieceType.X)

class PlayingPieceO(PlayingPiece):
	def __init__(self):
		super().__init__(PieceType.O)

class Board():
	def __init__(self, size):
		self.size = size
		self.board = [[None for _ in range(self.size)] for _ in range(self.size)]

	def addPiece(self, row, col, playingPiece):
		if self.board[row][col]:
			return False

		self.board[row][col] = playingPiece
		return True

	def getFreeCells(self):
		freeCells = []

		for i in range(self.size):
			for j in range(self.size):
				if not self.board[i][j]:
					freeCells.append((i, j))

		return freeCells

	def printBoard(self):
		for i in range(self.size):
			for j in range(self.size):
				if self.board[i][j] != None:
					print(self.board[i][j].pieceType.name + ' ', end='')
				else:
					print('  ', end='')

				print(' | ', end='')

			print()

class Player():
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
	def __init__(self):
		self.players = deque()
		self.gameBoard = None
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
			self.gameBoard.printBoard()
			freeSpaces = self.gameBoard.getFreeCells()
			if len(freeSpaces) == 0:
				noWinner = False
				continue

			# read the user input
			inpRow, inpCol = map(int, input('Player: ' + playerTurn._name + ' enter row, column: ').split(','))

			pieceAddedSuccessfully = self.gameBoard.addPiece(inpRow, inpCol, playerTurn.getPlayingPiece())
			if not pieceAddedSuccessfully:
				print('Incorrect position choosen, try again')
				self.players.appendleft(playerTurn)
				continue

			self.players.append(playerTurn)

			winner = self.isThereWinner(inpRow, inpCol, playerTurn.getPlayingPiece().pieceType)
			if winner:
				return playerTurn.getName()


		return 'Tie'

	def isThereWinner(self, row, col, pieceType):
		rowMatch = True
		colMatch = True
		diagonalMatch = True
		antiDiagonalMatch = True

		# need to check in row
		for i in range(len(self.gameBoard.board)):
			if self.gameBoard.board[row][i] == None or self.gameBoard.board[row][i].pieceType != pieceType:
				rowMatch = False

		# need to check in column
		for i in range(len(self.gameBoard.board)):
			if self.gameBoard.board[i][col] == None or self.gameBoard.board[i][col].pieceType != pieceType:
				colMatch = False

		# need to check diagonals
		for i in range(len(self.gameBoard.board)):
			if self.gameBoard.board[i][i] == None or self.gameBoard.board[i][i].pieceType != pieceType:
				diagonalMatch = False

		# need to check anti-diagonals
		for i in range(len(self.gameBoard.board)):
			if self.gameBoard.board[i][len(self.gameBoard.board)-1 - i] == None or self.gameBoard.board[i][len(self.gameBoard.board)-1-i].pieceType != pieceType:
				antiDiagonalMatch = False

		return rowMatch or colMatch or diagonalMatch or antiDiagonalMatch

if __name__ == '__main__':
	game = TicTacToeGame()
	print('game winner is: ', game.startGame())
