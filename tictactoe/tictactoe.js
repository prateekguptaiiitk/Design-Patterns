// Enums
const PieceType = Object.freeze({
  X: 'X',
  O: 'O'
});

// Playing Piece Classes
class PlayingPiece {
  constructor(pieceType) {
    this.pieceType = pieceType;
  }
}

class PlayingPieceX extends PlayingPiece {
  constructor() {
    super(PieceType.X);
  }
}

class PlayingPieceO extends PlayingPiece {
  constructor() {
    super(PieceType.O);
  }
}

// Player Class
class Player {
  constructor(name, playingPiece) {
    this._name = name;
    this._playingPiece = playingPiece;
  }

  getName() {
    return this._name;
  }

  setName(name) {
    this._name = name;
  }

  getPlayingPiece() {
    return this._playingPiece;
  }

  setPlayingPiece(piece) {
    this._playingPiece = piece;
  }
}

// Board Class
class Board {
  constructor(size) {
    this.size = size;
    this.board = Array.from({ length: size }, () => Array(size).fill(null));
  }

  addPiece(row, col, piece) {
    if (this.board[row][col]) return false;
    this.board[row][col] = piece;
    return true;
  }

  getFreeCells() {
    const freeCells = [];
    for (let i = 0; i < this.size; i++) {
      for (let j = 0; j < this.size; j++) {
        if (!this.board[i][j]) {
          freeCells.push([i, j]);
        }
      }
    }
    return freeCells;
  }

  printBoard() {
    for (let i = 0; i < this.size; i++) {
      let row = '';
      for (let j = 0; j < this.size; j++) {
        if (this.board[i][j]) {
          row += `${this.board[i][j].pieceType} | `;
        } else {
          row += '  | ';
        }
      }
      console.log(row);
    }
  }
}

// Game Class
class TicTacToeGame {
  constructor() {
    this.players = [];
    this.board = null;
    this.initializeGame();
  }

  initializeGame() {
    const player1 = new Player('Player1', new PlayingPieceX());
    const player2 = new Player('Player2', new PlayingPieceO());
    this.players.push(player1, player2);
    this.board = new Board(3);
  }

  async startGame() {
    let noWinner = true;

    while (noWinner) {
      const playerTurn = this.players.shift();

      this.board.printBoard();

      const freeCells = this.board.getFreeCells();
      if (freeCells.length === 0) {
        noWinner = false;
        break;
      }

      const input = await this.readInput(`${playerTurn.getName()} enter row,col: `);
      const [row, col] = input.split(',').map(Number);

      if (
        row < 0 ||
        row >= this.board.size ||
        col < 0 ||
        col >= this.board.size
      ) {
        console.log('Incorrect position chosen, try again.');
        this.players.unshift(playerTurn);
        continue;
      }

      const success = this.board.addPiece(row, col, playerTurn.getPlayingPiece());
      if (!success) {
        console.log('Cell already occupied, try again.');
        this.players.unshift(playerTurn);
        continue;
      }

      this.players.push(playerTurn);

      if (this.isThereWinner(row, col, playerTurn.getPlayingPiece().pieceType)) {
        return playerTurn.getName();
      }
    }

    return 'Tie';
  }

  isThereWinner(row, col, pieceType) {
    const size = this.board.size;
    let rowMatch = true;
    let colMatch = true;
    let diagMatch = true;
    let antiDiagMatch = true;

    for (let i = 0; i < size; i++) {
      if (!this.board.board[row][i] || this.board.board[row][i].pieceType !== pieceType)
        rowMatch = false;

      if (!this.board.board[i][col] || this.board.board[i][col].pieceType !== pieceType)
        colMatch = false;

      if (!this.board.board[i][i] || this.board.board[i][i].pieceType !== pieceType)
        diagMatch = false;

      if (
        !this.board.board[i][size - 1 - i] ||
        this.board.board[i][size - 1 - i].pieceType !== pieceType
      )
        antiDiagMatch = false;
    }

    return rowMatch || colMatch || diagMatch || antiDiagMatch;
  }

  readInput(promptText) {
    return new Promise((resolve) => {
      const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
      });
      readline.question(promptText, (input) => {
        readline.close();
        resolve(input);
      });
    });
  }
}

// Start the game
(async () => {
  const game = new TicTacToeGame();
  const result = await game.startGame();
  console.log('Game winner is: ', result);
})();
