import random
random.seed("62")


class CRoom():
	def __init__(self, pos):
		self.pos = pos
		self.doors = [0, 0, 0, 0] # East, North, West, South (odre trigo)
		self.texture = "A"
		self.distCentre = 0
		return

	def __str__(self):
		t = []
		for e in self.doors:
			if e == 0:
				t.append(0)
			else:
				t.append(1)
		return str(t)
		
	def setDist(self, dist):
		self.distCentre = dist
		return

	def link(self, target, room):
		if target[0]-self.pos[0] == 1:
			self.doors[0] = room
		elif target[1]-self.pos[1] == 1:
			self.doors[1] = room
		elif target[0]-self.pos[0] == -1:
			self.doors[2] = room
		elif target[1]-self.pos[1] == -1:
			self.doors[3] = room
		else:
			print("room.openDoor : target - pos != 1 or -1")
		return

	def outDoors(self):
		return self.doors
	
	def outTexture(self):
		return self.texture

class CLaby():
	def __init__(self):
		return

	def gen(self):
		room = CRoom((0,0)) # pos = (x, y)
		self.laby = {(0,0) : room}
		a, b = 0, 0
		n = 9
		for i in range(1, n+1):
			A, B = a, b
			if random.randint(0, 1):
				a += random.choice((-1, 1))
			else:
				b += random.choice((-1, 1))
			if (a, b) not in self.laby.keys():
				self.laby[a, b] = CRoom((a, b))
				#self.laby[a, b].setDist(i)
			self.laby[a, b].link((A, B), self.laby[A, B])
			self.laby[A, B].link((a, b), self.laby[a, b])
		
		self.addDistance(self.laby[0,0])
		return
		
	def addDistance(self, room):
		print(room.outDoors())
		for nroom in room.outDoors():
			if nroom != 0 and room.distCentre == 0:
				print(nroom)
				nroom.setDist(room.distCentre+1)
				return self.addDistance(nroom)
			
		return
		
	def out(self):
		return self.laby

	def printLaby(self):
		keylist = list(self.laby.keys())
		x, y = [], []
		for i in range(len(keylist)):
			x.append(keylist[i][0])
			y.append(keylist[i][1])
		x = [min(x), max(x)]
		y = [min(y), max(y)]
		#print(x, y)
		
		for j in range(y[0], y[1]):
			for i in range(x[0], x[1]):
				if (i,j) in keylist:
					print(self.laby[i,j].distCentre, end='')
				else:
					print(" ", end='')

			print("")
		print("")
		print('\n'.join('%2d %2d %s'%(i,j,self.laby[(i, j)]) for i,j in self.laby))
		
		return


laby = CLaby()
laby.gen()
laby.printLaby()


