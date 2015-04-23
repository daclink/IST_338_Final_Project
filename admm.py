#Drew A. Clinkenbeard
#http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html
#http://en.wikipedia.org/wiki/Maze_generation_algorithm
#https://docs.python.org/2/library/curses.html#textbox-objects



#import admm; reload(admm); from admm import *

"""TODO
Fix maze generation
	* why does it error periodically?
	** I think it's going out of bounds when calculating neighbors...
Investigate changing colors

?Add pop-ups for leveling?
	*https://docs.python.org/2/library/curses.html#textbox-objects
Add enemies 
Add items
Add a border!!
Add try catch
"""

import sys
import random
import time
import curses
import locale
import random
import math
import json
from time import localtime, strftime

sys.setrecursionlimit(100000)
class mm():

	def __init__(self, y=15,x=15, debug=True):
		if debug:
			self.log =  open("admm.log",'a+')

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
		# pizza
		player =	u"\U0001f355"

		#house
		self.exit = u"\U0001f3e0"

		# Setup Screen
		stdscr = curses.initscr()
		curses.savetty() #make sure we can put the screen back the way we found it
		curses.noecho() #prevent keypresses appearing on screen
		curses.cbreak() #interpret input with out return
		stdscr.keypad(1) #everyone loves the keypad
		stdscr.clearok(1) #allow the screen to be cleared
		curses.curs_set(0) #hide the caret

		stdscr.clear()
		stdscr.refresh()


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

		stdscr.clear()
		stdscr.refresh()
		# begin main while

		moveTest = True
		# charPos = {'y':0,'x':0}
		while moveTest:

			stdscr.clear()

			for cols in self.maze:
				for rows in self.maze[cols]:
					if self.maze[cols][rows]['wall'] :
						stdscr.addstr(cols,rows,"#")
			stdscr.addstr(charPos[0],charPos[1]-1,player.encode("utf-8"))
			stdscr.addstr(self.startY,self.startX,self.exit.encode("utf-8"))

			stdscr.refresh()
			

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
			

		# end main while


		time.sleep(1)
		##put it all back
		curses.resetty()
		curses.endwin()

		if debug:
			self.log.close()

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


	def __get_neighbor__(self,y,x,diagonals=False):
		neighbors = {}
		# check north and northwest cells
		if (y-2) >= self.minY:
			neighbors['N'] = {'y':y-2,'x':x}
			if diagonals and x-2 >= self.minX:
				neighbors['NW'] = {'y':y-2,'x':x-2}

		# check east and south east
		if (x+2) <= self.maxX-1:
			neighbors['E'] = {'y':y,'x':x+2}
			if diagonals and (y+2) <= self.maxY:
				neighbors['SE'] = {'y':y+2,'x':x+2} 

		# check the north and nw corners
		if (x-2) >= self.minX:
			neighbors['W'] = {'y':y,'x':x-2}
			if diagonals and (y-2) >= self.minY:
				neighbors['NW'] = {'y':y-2,'x':x-2}

		# check south cell and south west cell
		if (y+2) <= self.maxY-1:
			neighbors['S'] = {'y':y+2,'x':x}
			# check southwest cell
			if diagonals and x+2 <= self.maxX:
				neighbors['SW'] = {'y':y+2,'x':x+2}
		# print neighbors
		return neighbors

	def __generate_maze__(self,y,x):

		self.maze[y][x]['wall']= False
		self.maze[y][x]['visited'] = True
		self.visited -= 1
		neighbors = self.__get_neighbor__(y,x)
		self.lastY = y
		self.lastX = x


		# add a border
		for col in self.maze:
			for row in self.maze[col]:
				if row == 0  or row == self.maxX:
					self.maze[col][row]['visited'] = True
					self.maze[col][row]['wall'] = True
				if col == self.minY or col == self.maxY:
					self.maze[col][row]['visited'] = True
					self.maze[col][row]['wall'] = True




		while neighbors:
			rand_neighbor = random.choice(neighbors.keys())
			

			try :
				ny = neighbors[rand_neighbor]['y']
				nx = neighbors[rand_neighbor]['x']
			except KeyError as e:
				self.__err__(e,{'x':x,'y':y,'ny':ny,'nx':nx,'report':"getting neighbors of x and y"})

			try :
				if self.maze[ny][nx]['visited'] or not self.maze[ny][nx]['visited']:
					pass
			except KeyError as e:
				report = { 'ny':ny,'nx':nx, 'report':'callings self.maze with ny and nx'}
				self.__err__(e,report)				


			# try catch and throw to file.

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

	def __err__(self,e,values):
		stats  = "minY %d maxY %d\n" %(self.minY, self.maxY)
		stats += "minX %d maxX %d\n" %(self.minX, self.maxX)
		stats += "len(self.maze) %d len(self.maze[self.minY]) %d" %(len(self.maze) , len(self.maze[self.minY]))

		report = strftime("[%d.%b.%Y %H:%M:%S] ",localtime())
		report += 'KeyError: ['
		report += str(e)
		report += ']\n'
		self.log.write(report)
		self.log.write("\n**stats**\n")
		self.log.write(stats)
		self.log.write("\n**stats**\n")
		self.log.write("\n ** report **\n")
		json.dump(values,self.log)
		self.log.write("\n ** report **\n")
# maze = maze_maker()

# print maze.maze

# maze

