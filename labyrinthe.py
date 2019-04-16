import random

def getKey(val, dict):
	out = []
	for key, value in dict.items(): 
		if val == value:
			out.append(key)
	return out 


class CRoom():
	def __init__(self, pos):
		self.pos = pos # room coordinates
		self.doors = [0, 0, 0, 0] # East, North, West, South (odre trigo)
		self.texture = "A" # not used (yet ?)
		self.isEnd = 0 # is this room the end of the level
		return

	def __str__(self): # nice display in case of a print(object)
		t = []
		for e in self.doors:
			if e == 0:
				t.append(0)
			else:
				t.append(1)
		return 'ROOM %s - %s'%(str(self.pos), str(t))
		return str(t)

	def link(self, target, room): # create a one way-link with another room
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

	def outTexture(self): # not used
		return self.texture

class CLaby():
	def __init__(self):
		return

	def initRandom(self, n=None):
		if n:
			random.seed(n)
		else:
			random.seed()

	def gen(self, n=9): # generating the labyrinth
		for rooms, (i,j) in self.stepGen(n): # calling stepGen as many times as necessary
			pass
		self.map = CDistance(self).spread((0,0)) # get the distance between any tile and the starting position
		possiblePos = getKey(max(self.map.values()), self.map) # list all max distance rooms
		room = self.laby[possiblePos[random.randint(0, len(possiblePos)-1)]] #pick a random room at a max distance from the inital position
		room.isEnd = 1 # set the end of the game
		return self.laby

	def stepGen(self, n=9):
		room = CRoom((0,0)) # pos = (x, y)
		self.laby = {(0,0) : room} #init starting room
		a, b = 0, 0
		while len(self.laby) < n: # while there is less than n rooms
			A, B = a, b
			if random.randint(0, 1):
				a += random.choice((-1, 1))
			else:
				b += random.choice((-1, 1))
			if (a, b) not in self.laby.keys():
				self.laby[a, b] = CRoom((a, b))
			self.laby[a, b].link((A, B), self.laby[A, B])
			self.laby[A, B].link((a, b), self.laby[a, b])

			yield self.laby, (a,b) # yield a intermediary position to enable following the generation process

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
		
		for j in range(y[0], y[1]+1):
			for i in range(x[0], x[1]+1):
				if (i,j) in keylist:
					if self.laby[(i,j)].isEnd:
						print("XX", end='')
					else:
						print("·{0:2d}·".format(self.map[i,j]), end='')
				else:
					print("····", end='')
			print("")
			for i in range(x[0], x[1]+1):
				print("····", end='')
			print("")
		print("\n")
		return



class CDistance():
	def __init__(self, laby):
		self.laby = laby
		return
		
	def listNextRooms(self, pos):
		out = []
		for room in self.laby.laby[pos].doors:
			if room != 0:
				out.append(room.pos)
		return out

	def spread(self, curr_pos):
		depth = 0
		frontiere = [curr_pos]
		map = {curr_pos : depth}
		modif = 1
		while frontiere != []:
			pos = frontiere[0]
			for posNextRoom in self.listNextRooms(pos):
				if posNextRoom not in list(map.keys()):
					map[posNextRoom] = map[pos]+1
					frontiere.append(posNextRoom)
			frontiere.pop(0)
		if map.keys() == self.laby.laby.keys():
			return map
		else:
			return 1
			
	def shortestDistTo(self, curPos, targetPos):
		return
		

if __name__ == '__main__':
	
	laby = CLaby()
	laby.initRandom()
	laby.gen(30)
	laby.printLaby()
	for room in laby.laby.values():
		if room.isEnd == 1:
			endFound = 1
	if endFound != 1:
		print("error multiple/no end(s)")

	
	dist = CDistance(laby)



