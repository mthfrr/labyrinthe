import random

class CRoom():
	def __init__(self, pos):
		self.pos = pos
		self.doors = [0, 0, 0, 0] # East, North, West, South (odre trigo)
		return
	
	def __str__(self):
		t = []
		for e in self.doors:
			if e == 0:
				t.append(0)
			else:
				t.append(1)
		return str(t)
		

	def link(self, target, room):
		if  target[0]-self.pos[0] == 1:
			self.doors[0] = room
		elif target[1]-self.pos[1] == 1:
			self.doors[1] = room
		elif target[0]-self.pos[0] == -1:
			self.doors[2] = room
		elif target[1]-self.pos[1] == -1:
			self.doors[3] = room
		else:
			print("room.openDoor : target - pos != 1 or -1")

	def outDoors(self):
		return self.doors

class CLaby():
	def __init__(self):
		return

	def gen(self):
		room = CRoom((0,0)) # pos = (x, y)
		self.laby = {(0,0) : room} 
		a, b = 0, 0
		for i in range(10):
			A, B = a, b
			if random.randint(0, 1):
				a += random.choice((-1, 1))
			else:
				b += random.choice((-1, 1))
			self.laby[a, b] = CRoom((a, b))
			self.laby[a, b].link((A, B), self.laby[A, B])
			self.laby[A, B].link((a, b), self.laby[a, b])
		return

	def out(self):
		return self.laby

	def printLaby(self):
		keylist = list(self.laby.keys())
		x = [0, 0]
		y = [0, 0]
		for k in keylist:
			if x[0]>k[0]:
				x[0] = k[0]
			elif x[1]<k[0]:
				x[1] = k[0]
			if y[0]>k[1]:
				y[0]=k[1]
			elif y[1]<k[1]:
				y[1]=k[1]
		#print(x, y)
		for j in range(y[0], y[1]):
			for i in range(x[0], x[1]):
				if (i,j) in keylist:
					print("+", end='')
				else:
					print(" ", end='')
			print("")
		'''
		print('\n'.join('%2d %2d %s'%(i,j,self.laby[(i, j)]) for i,j in self.laby))
		'''
		return

laby = CLaby()
laby.gen()
laby.printLaby()