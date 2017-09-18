'use strict';

var CELL_SIZE = 7;
var cells = [], buffCells = [];
var timeout = 2000;
var canvas, game;

function init() {

	canvas = document.getElementById('back').getContext('2d');
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
	game = document.getElementById('game').getContext('2d');
	game.width = window.innerWidth;
	game.height = window.innerHeight;
	game.fillStyle = "#8b8b8b";

	function Grid() {
		this.size = {x: 0, y: 0};
		this.width = canvas.width;
		this.height = canvas.height;

		this.size.x = parseInt(canvas.width / CELL_SIZE, 10);
		this.size.y = parseInt(canvas.height / CELL_SIZE, 10);

		this.fill = function () {
			var i, j;
			for (i = 0; i < this.size.x; i += 1) {
				cells[i] = [];
				buffCells[i] = [];
				for (j = 0; j < this.size.y; j += 1) {
					cells[i][j] = false;
					buffCells[i][j] = false;
				}
			}
		};

		this.draw = function () {
			var i;
			canvas.translate(0.5, 0.5);
			canvas.beginPath();
			for (i = 0; i <= this.size.x; i += 1) {
				canvas.moveTo(0, i * CELL_SIZE);
				canvas.lineWidth = 1;
				canvas.lineTo(this.width, i * CELL_SIZE);
				canvas.strokeStyle = "#787878";
			}

			for (i = 0; i <= this.size.x; i += 1) {
				canvas.lineWidth = 1;
				canvas.moveTo(i * CELL_SIZE, 0);
				canvas.lineTo(i * CELL_SIZE, canvas.height);
				canvas.strokeStyle = "#808084";
			}
			canvas.stroke();
		};
	}

	function Update() {
		this.clear = function () {
			game.clearRect(0, 0, canvas.width, canvas.height);
		};

		this.fillCell = function (x, y) {
			game.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE + 1, CELL_SIZE + 1);
		};

		this.fill = function () {
			var i, j, grid = new Grid(), upd = new Update();

			upd.clear();

			for (i = 0; i < grid.size.x; i += 1) {
				for (j = 0; j < grid.size.y; j += 1) {
					if (cells[i][j] === true) {
						upd.fillCell(i, j);
					}
				}
			}
			upd.cells();
		};

		this.randomFill = function () {
			var i, j, fill, fillRnd, grid = new Grid(), upd = new Update();
			upd.clear();

			for (i = 0; i < grid.size.x; i += 1) {
				for (j = 0; j < grid.size.y; j += 1) {
					fill = [true, false][Math.round(Math.random())];
					cells[i][j] = Boolean(fill);
				}
			}

			for (i = 0; i < grid.size.x; i += 1) {
				for (j = 0; j < grid.size.y; j += 1) {
					fill = cells[i][j];
					if (fill === true) {
						fillRnd = new Update();
						fillRnd.fillCell(i, j);
					}
				}
			}
		};

		this.autoplay = function () {
			var upd = new Update();
			upd.fill();
			setTimeout(function () {
				upd.autoplay();
			}, timeout);
		};

		this.getLivingNeighbors = function (x, y) {
			var grid = new Grid(), count = 0, sx = grid.size.x, sy = grid.size.y;

			if (x !== 0 && y !== 0) {
				if (cells[x - 1][y - 1] === true) {
					count += 1;
				}
			}
			if (y !== 0) {
				if (cells[x][y - 1] === true) {
					count += 1;
				}
			}
			if (x !== sx - 1 && y !== 0) {
				if (cells[x + 1][y - 1] === true) {
					count += 1;
				}
			}
			if (x !== 0) {
				if (cells[x - 1][y] === true) {
					count += 1;
				}
			}
			if (x !== sx - 1) {
				if (cells[x + 1][y] === true) {
					count += 1;
				}
			}
			if (x !== 0 && y !== sy - 1) {
				if (cells[x - 1][y + 1] === true) {
					count += 1;
				}
			}
			if (y !== sy - 1) {
				if (cells[x][y + 1] === true) {
					count += 1;
				}
			}
			if (x !== sx - 1 && y !== sy - 1) {
				if (cells[x + 1][y + 1] === true) {
					count += 1;
				}
			}
			return count;
		};

		this.cells = function () {
			var i, j, isAlive, count, result = false, gameUpd = new Update(), grid = new Grid();

			for (i = 0; i < grid.size.x; i += 1) {
				for (j = 0; j < grid.size.y; j += 1) {

					result = false;
					isAlive = cells[i][j];

					count = gameUpd.getLivingNeighbors(i, j);
					if (isAlive && count < 2) {
						result = false;
					}
					if (isAlive && (count === 2 || count === 3)) {
						result = true;
					}
					if (isAlive && count > 3) {
						result = false;
					}
					if (!isAlive && count === 3) {
						result = true;
					}

					buffCells[i][j] = result;
				}
			}

			for (i = 0; i < grid.size.x; i += 1) {
				for (j = 0; j < grid.size.y; j += 1) {
					cells[i][j] = buffCells[i][j];
				}
			}
		};
	}

	var gameGrid = new Grid(), gameUpd = new Update();
	gameGrid.draw();
	gameGrid.fill();
	gameUpd.randomFill();
	gameUpd.autoplay();
}

window.onload = init();