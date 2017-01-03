class Board:
	def __init__(self, grid = nil):
		if grid:
			self.grid = grid
		else:
			self.grid = [[-1] * (6) for i in range(5)]
		
	def __str__(self):
		return "\n".join(["".join(row) for row in grid]))