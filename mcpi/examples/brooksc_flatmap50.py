#!/usr/bin/env python

#import the minecraft.py module from the minecraft directory
from .. import minecraft
from .. import block
import server

def main():
    mc = minecraft.Minecraft.create(server.address)
    # write the rest of your code here...
    mc.postToChat("Erasing a 50x50 block...")
    mc.setBlocks(-50,-10,-50,50,10,50,block.AIR.id)
    mc.setBlocks(-50,0,-50,50,-10,50,block.SANDSTONE.id)
    mc.postToChat("Done Erasing a 50x50 block!")



if __name__ == "__main__":
    main()
