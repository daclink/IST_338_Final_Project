#Drew A. Clinkenbeard
import sys
import random
import time
import curses
import locale
import random
import math

sys.setrecursionlimit(100000)
class mm():

	def __init__(self, y=15,x=15, debug=True):
		maze = {}
		self.maxY = y-1
		self.maxX = x-1
		self.minY = self.minX = 0
		self.visited = 0

		locale.setlocale(locale.LC_ALL, '')
		code = locale.getpreferredencoding()
		self.debug = debug
		if debug :
			print "Hello there! deubg is ", debug
		# Setup Player
		self.setScore(0)
		player =	u"\U0001f355"

		# Setup Screen
		stdscr = curses.initscr()
		curses.savetty() #make sure we can put the screen back the way we found it
		curses.noecho() #prevent keypresses appearing on screen
		curses.cbreak() #interpret input with out return
		stdscr.keypad(1) #everyone loves the keypad
		stdscr.clearok(1) #allow the screen to be cleared
		curses.curs_set(0) #hide the caret

		self.minX = minX	= 0
		#how far to the right we can go.
		#Leaving room for messages.
		self.maxX = maxX	= stdscr.getmaxyx()[1] -15

		self.minY = minY	= 0
		##how far down we can go
		#leaving room for messages
		self.maxY = maxY	= stdscr.getmaxyx()[0] -5


		# setup maze
		for cols in range(maxY):
			maze[cols] = {}
			for rows in range(maxX):
				maze[cols][rows] = {}
				maze[cols][rows]['visited'] = False
				self.visited += 1
				maze[cols][rows]['wall'] = True

		self.maze = maze
		self.__get_start__()
		self.__generate_maze__(self.startY,self.startX)

		charPos = [self.lastY,self.lastX]


		# begin main while

		moveTest = True
		# charPos = {'y':0,'x':0}
		while moveTest:
			move = stdscr.getch()
			if move == 113 :
				moveTest = False
			elif move == curses.KEY_RIGHT:
				if self.maze[charPos[0]][charPos[1]+1]['wall'] == False :
					charPos[1] += 1
			elif move == curses.KEY_LEFT:
				if self.maze[charPos[0]][charPos[1]-1]['wall'] == False :
					charPos[1] -= 1
			elif move == curses.KEY_UP:
				if self.maze[charPos[0]-1][charPos[1]]['wall'] == False :
					charPos[0] -= 1
			elif move == curses.KEY_DOWN:
				if self.maze[charPos[0]+1][charPos[1]]['wall'] == False :
					charPos[0] += 1
			stdscr.clear()

			for cols in self.maze:
				for rows in self.maze[cols]:
					if self.maze[cols][rows]['wall'] :
						stdscr.addstr(cols,rows,"#")
			stdscr.addstr(charPos[0],charPos[1],player.encode("utf-8"))
			stdscr.refresh()

		# end main while


		time.sleep(1)
		##put it all back
		curses.resetty()
		curses.endwin()

	def __get_start__(self):
		self.startY = random.choice(self.maze.keys())
		self.startX = random.choice(self.maze[self.startY].keys())

	def __repr__(self):
		maze = ''
		for cols in self.maze:
			for rows in self.maze[cols]:
				if self.maze[cols][rows]['wall'] :
					# print '.',
					maze += '#'
				else:
					# print ' ',
					maze += ' '
			# print '\n'
			maze += '\n'

		return maze


	def __get_neighbor__(self,y,x):
		neighbors = {}
		if (y-2) >= self.minY:
			neighbors['N'] = {'y':y-2,'x':x}
		if (x+2) <= self.maxX:
			neighbors['E'] = {'y':y,'x':x+2}
		if (x-2) >= self.minX:
			neighbors['W'] = {'y':y,'x':x-2}
		if (y+2) <= self.maxY:
			neighbors['S'] = {'y':y+2,'x':x}
		# print neighbors
		return neighbors

	def __generate_maze__(self,y,x):

		self.maze[y][x]['wall']= False
		self.maze[y][x]['visited'] = True
		self.visited -= 1
		neighbors = self.__get_neighbor__(y,x)
		self.lastY = y
		self.lastX = x

		while neighbors:
			rand_neighbor = random.choice(neighbors.keys())
			# print rand_neighbor

			ny = neighbors[rand_neighbor]['y']
			nx = neighbors[rand_neighbor]['x']

			if not self.maze[ny][nx]['visited']:
				# self.visited -= 1

				if (ny - y) > 0:
					self.maze[ny-1][x]['visited'] = True
					self.maze[ny-1][x]['wall'] = False
				if (ny - y) < 0:
					self.maze[ny+1][x]['visited'] = True
					self.maze[ny+1][x]['wall'] = False
				if (nx - x) > 0:
					self.maze[y][nx-1]['visited'] = True
					self.maze[y][nx-1]['wall'] = False
				if (nx - x) < 0:
					self.maze[y][nx+1]['visited'] = True
					self.maze[y][nx+1]['wall'] = False
			del neighbors[rand_neighbor]

			if self.visited > 0:
				self.__generate_maze__(ny,nx)

		return 0


	def setScore(self, score):
		self.score = score
# maze = maze_maker()

# print maze.maze

# maze

