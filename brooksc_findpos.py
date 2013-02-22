#!/usr/bin/env python

#import the minecraft.py module from the minecraft directory
import mcpi.minecraft as minecraft
#import minecraft block module
import mcpi.block as block
#import time, so delays can be used
import time
import server

if __name__ == "__main__":
    mc = minecraft.Minecraft.create(server.address)
    mc.postToChat("Flattening surface")
    mc.setBlocks(-128,0,-128,128,64,128,0)
    mc.setBlocks(-128,0,-128,128,-64,128,block.SANDSTONE.id)
    mc.postToChat("Putting a diamong block at 0,0,0")
    mc.setBlock(0,0,0,block.DIAMOND_BLOCK.id)
    while True:
        #Find out your players position
        playerPos = mc.player.getPos()
        mc.postToChat("Find your position - its x=%s z=%s y=%s" % (int(playerPos.x), int(playerPos.z), int(playerPos.y)))
        time.sleep(1)
