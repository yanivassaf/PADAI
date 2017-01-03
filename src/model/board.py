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
		
	def __str__(self):
		return "\n".join(["".join([str(i) for i in row]) for row in self.grid])