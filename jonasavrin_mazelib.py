'''
Created on Feb 18, 2013
@originalAuthor: Dave Finch
@author: Jonas Avrin cghijinks@gmail.com
'''
import minecraft
import block
import random
from random import randint as rand
 
class Maze(object):
    ''''''
    def __init__(self, **kwargs):
        self.verbose = kwargs.setdefault('verbose', False)
        # Connect to minecraft <img src="http://www.jonasavrin.com/wp-includes/images/smilies/icon_smile.gif" alt=":)" class="wp-smiley"> 
        self.mc = self.connect()
        self.maze = []
        self.spl = []
 
        # Define the X and Y size of the maze including the outer walls.
        self.sizex = kwargs.get('sizex', None)
        self.sizey = kwargs.get('sizey', None)
        self.dimms = ()
        if self.sizex and self.sizey:
            self.dimms = (self.sizex, self.sizey)
        else:
            self.sizex = kwargs.setdefault('sizex', 21)
            self.sizey = kwargs.setdefault('sizey', 21)
        if self.verbose:
            print '# MAZE DIMMS #\n' \
                + 'sizex: %d sizey: %d:' % (self.sizex, self.sizey)
 
        # Set maximum length of wall
        self.max_wall_len = kwargs.setdefault('max_wall_len', 1)
        # Find position of player and set base of maze 3 blocks lower.
        self.ppos = self.mc.player.getPos()
        self.ppos.y -= 3
 
    @property
    def dimms(self):
        return self.sizex, self.sizey
 
    @dimms.setter
    def dimms(self, val):
        if not isinstance(val, tuple):
            raise TypeError('Dimensions value type must be a tuple(x, y)')
        for v in val:
            if not self.isodd(v):
                self.sizex, self.sizey = [v + 1 for v in val]
            else:
                self.sizex, self.sizey = [v for v in val]
 
    def isodd(self, num):
            return num & 1 and True or False
 
    def create(self):
        # Create an empty maze.
        self.clear()
        self.initMaze()
 
    @staticmethod
    def connect():
        # Connect to Minecraft.
        try:
            mc = minecraft.Minecraft.create()
            return mc
        except:
            raise RuntimeError('Minecraft unavailable.')
 
    def clear(self):
        # Clear an area for the maze.
        for x in xrange(0, self.sizex - 1):
            for z in xrange(self.sizey - 1):
                self.mc.setBlock(self.ppos.x + x, self.ppos.y, self.ppos.z + z,
                                 block.STONE)
                for y in xrange(1, 6):
                    self.mc.setBlock(self.ppos.x + x, self.ppos.y + y,
                                     self.ppos.z + z, block.AIR)
 
    # Create a function to initialize the maze.
    def initMaze(self):
        # print player position
        if self.verbose:
            print 'player pos: %r' % self.ppos
 
        # Create a 2 dimensional array.
        self.maze = [[0] * self.sizey for x in xrange(self.sizex)]
 
        # print the maze
        if self.verbose:
            colsize = 0
            for m in self.maze:
                print ''.join(('%-*s' % (colsize + 3, i) for i in m))
 
        # Create four walls around the maze.
        # 1=wall, 0=walkway.
        for x in xrange(0, self.sizex):
            self.maze[x][0] = self.maze[x][self.sizey - 1] = 1
            self.makeWall(self.ppos.x + x, self.ppos.z + 0)
            self.makeWall(self.ppos.x + x, self.ppos.z + self.sizey - 1)
        for y in xrange(0, self.sizey):
            self.maze[0][y] = self.maze[self.sizex - 1][y] = 1
            self.makeWall(self.ppos.x, self.ppos.z + y)
            self.makeWall(self.ppos.x + self.sizex - 1, self.ppos.z + y)
 
        # Make every other cell a starting point.
        # 2=starting point.
        # Also create a list of these points to speed up the main loop.
        for y in xrange(2, self.sizey - 1, 2):
            for x in xrange(2, self.sizex - 2, 2):
                self.maze[x][y] = 2
                self.spl.append((x, y))
 
        # print the initialized maze
        if self.verbose:
            colsize = 0
            print 'maze initialized: \n'
            for m in self.maze:
                print ''.join(('%-*s' % (colsize + 3, i) for i in m))
 
            print '\n', 'rand spl: %r' % self.spl
 
        # Shuffle the list of points and we can choose a random point by
        # simply "popping" it off the list.
        random.shuffle(self.spl)
        if self.verbose:
            print 'rand spl: %r' % self.spl
 
    # Create a function for picking a random direction.
    def randDir(self):
        r = rand(0, 3)
        # Up.
        if r == 0:
            rv = (0, -1)
        # Down.
        if r == 1:
            rv = (0, 1)
        # Left.
        if r == 2:
            rv = (-1, 0)
        # Right.
        if r == 3:
            rv = (1, 0)
        return rv
 
    def generate(self):
        # Loop until we have no more starting points (2's in the empty maze)
        while filter(lambda x: 2 in x, self.maze):
            # Get the X and Y values of the first point in our randomized list.
            rx = self.spl[0][0]
            ry = self.spl[0][1]
            # Pop the first entry in the list, this deletes it,
            # the rest move down.
            self.spl.pop(0)
            # Check to see if our chosen point is still a valid starting point.
            ud = False
            if self.maze[rx][ry] == 2:
                ud = True
                # Pick a random wall length up to the maximum.
                rc = rand(0, self.max_wall_len)
                # Pick a random direction.
                rd = self.randDir()
                fc = rd
                loop = True
                while loop:
                    # Look in each direction, if the current wall being built
                    # is stuck inside itself start again.
                    if (self.maze[rx][ry - 2] == 3 and
                       self.maze[rx][ry + 2] == 3 and
                       self.maze[rx - 2][ry] == 3 and
                       self.maze[rx + 2][ry] == 3):
                        #
                        # Code to clear maze area required
                        #
                        self.initMaze(self.sizex, self.sizey)
                        break
                    # Look ahead to see if we're okay to go in this direction.
                    cx = rx + (rd[0] * 2)
                    cy = ry + (rd[1] * 2)
                    nc = self.maze[cx][cy]
                    if nc != 3:
                        for i in xrange(0, 2):
                            self.maze[rx][ry] = 3
                            self.makeWall(self.ppos.x + rx, self.ppos.z + ry)
                            rx += rd[0]
                            ry += rd[1]
                    # .....if not choose another direction.
                    else:
                        rd = self.randDir()
                    # If we hit an existing wall break out of the loop.
                    if nc == 1:
                        loop = False
                    # Update our wall length counter.
                    # When this hits zero pick another direction.
                    # This also makes sure the new direction
                    # isn't the same as the current one.
                    rc -= 1
                    if rc <= 0:                         rc = rand(0, self.max_wall_len)                         dd = rd                         de = (fc[0] * -1, fc[1] * -1)                         while dd == rd or rd == de:                             rd = self.randDir()             # The latest wall has been built so             # change all 3's (new wall) to 1's (existing wall)             if ud:                 for x in xrange(0, self.sizex):                     for y in xrange(0, self.sizey):                         if self.maze[x][y] == 3:                             self.maze[x][y] = 1     def makeWall(self, x, z):         self.mc.setBlock(x, self.ppos.y, z, block.STONE)         self.mc.setBlock(x, self.ppos.y + 1, z, block.STONE)         self.mc.setBlock(x, self.ppos.y + 2, z, block.STONE)