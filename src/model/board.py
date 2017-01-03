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
		
	def normalize(self):
		next = 0
		mapping = {}
		needMapping = False
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				val = self.grid[i][j]
				if  val not in mapping:
					if val != next:
						needMapping = True
					mapping[val] = next
					next += 1
					
		if not needMapping:
			return
			
		backMapping = {value:key for key, value in mapping.items() if key != value}
		
		keys = [key for key, value in backMapping.iteritems() if key != value]
		while len(keys) > 0:
			start = keys.pop()
			self.grid = [[-1 if x == start else x for x in row] for row in self.grid]
			walker = backMapping[start]
			while walker != start:
				keys.remove(walker)
				self.grid = [[mapping[walker] if x == walker else x for x in row] for row in self.grid]
				walker = backMapping[walker]
			self.grid = [[mapping[walker] if x == -1 else x for x in row] for row in self.grid]
		
	def serialize(self):
		commonGrid = self.__commonOrder()