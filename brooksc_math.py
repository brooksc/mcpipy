#!/usr/bin/env python

#import the minecraft.py module from the minecraft directory
import mcpi.minecraft as minecraft
#import minecraft block module
import mcpi.block as block
#import time, so delays can be used
import time
import server

def main():
    mc = minecraft.Minecraft.create(server.address)
#    mc.postToChat("Flattening surface")
    mc.setBlocks(-50,-10,-50,50,10,50,block.AIR.id)
    mc.setBlocks(-50,0,-50,50,-10,50,block.SANDSTONE.id)

#    mc.setBlocks(-50,0,-50,50,20,50,0)
#    mc.setBlocks(-50,0,-50,20,0,50,block.SANDSTONE.id)
#    mc.setBlocks(-128,0,-128,128,-64,128,block.SANDSTONE.id)

    mc.postToChat("Laying down the grid")
    # first square
    mc.setBlocks(2,0,0,6,0,4,block.DIAMOND_BLOCK.id)
    mc.setBlocks(2,-1,0,6,-1,4,block.DIAMOND_BLOCK.id)
    mc.setBlocks(3,0,1,5,0,3,block.AIR.id)

    # plus sign
    mc.setBlocks(11,0,0,11,0,4,block.DIAMOND_BLOCK.id)
    mc.setBlocks(9,0,2,13,0,2,block.DIAMOND_BLOCK.id)
    # second square
    mc.setBlocks(16,0,0,20,0,4,block.DIAMOND_BLOCK.id)
    mc.setBlocks(16,-1,0,20,-1,4,block.DIAMOND_BLOCK.id)
    mc.setBlocks(17,0,1,19,0,3,block.AIR.id)
    # equals
    mc.setBlocks(23,0,1,27,0,1,block.DIAMOND_BLOCK.id)
    mc.setBlocks(23,0,3,27,0,3,block.DIAMOND_BLOCK.id)
    # third square (result)
    mc.setBlocks(30,0,0,34,0,4,block.DIAMOND_BLOCK.id)
    mc.setBlocks(30,-1,0,34,-1,4,block.DIAMOND_BLOCK.id)
    mc.setBlocks(31,0,1,33,0,3,block.AIR.id)

#    exit()
    while True:
        hits = mc.events.pollBlockHits()
        if hits:
            mc.postToChat("Hit detected!")
        else:
            mc.postToChat("No hit detected!")
        time.sleep(1)


if __name__ == "__main__":
    main()