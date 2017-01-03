class Board:
	def __init__(self, rows, columns):
		self.grid = [[-1] * (columns) for i in range(rows)]
		
	def getGrid(self):
		return grid
			
	def set(self, row, column, color):
		currentColor = self.get(row, column)
		returnVal = currentColor == -1 or currentColor == color
		
		self.grid[row][column] = color
		
		return returnVal
		
	def get(self, row, column):
		return self.grid[row][column]
		
	def __set(self, array):
		self.grid = array

	# take string and create Board object
	@staticmethod
	def fromString(string):
		splitString = [map(int, list(x)) for x in string.split('\n')]
		board = Board(len(splitString), len(splitString[0]))
		board.__set(splitString)
		return board

	# take a Board and turn it into an array of hexidecimals
	def serialize(self):
		out = 0
		for row in self.grid:
			for num in row:
				out = (out << 4) | num
		return out

	# take a hexidecimal array and turn it into a Board
	@staticmethod
	def deserialize(hexed, rows, columns):
		board = Board(rows, columns)
		for r in range(rows)[::-1]:
			for c in range(columns)[::-1]:
				board.grid[r][c] = hexed & 15
				hexed = hexed >> 4
		return board

	def __str__(self):
		return "\n".join(["".join([str(i) for i in row]) for row in self.grid])
