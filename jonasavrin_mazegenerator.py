#! /usr/bin/python
# Commandline maze generator for Minecraft Pi edition.
# @author: Jonas Avrin cghijinks@gmail.com
 
import sys
import traceback
import mazeLib
 
def main():
    '''Create a maze instance.'''
    m = mazeLib.Maze(sizex=10, sizey=10, max_wall_len=1, verbose=True)
    m.clear()
    m.initMaze()
    m.generate()
 
if __name__ == '__main__':
    try:
        result = main()
    except KeyboardInterrupt:
        print "Bye"
        sys.exit(1)
    if result:
        sys.exit(0)
    elif '--debug' in sys.argv:
        print traceback.sys.exc_info()
    else:
        sys.exit(1)