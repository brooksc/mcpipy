#!/usr/bin/env python

#import the minecraft.py module from the minecraft directory
import mcpi.minecraft as minecraft
#import minecraft block module
import mcpi.block as block
#import time, so delays can be used
import time
import server

if __name__ == "__main__":
#    while True:
    #Find out your players position
    mc = minecraft.Minecraft.create(server.address)
    playerPos = mc.player.getPos()
    mc.postToChat("Find your position - its x=%s z=%s y=%s" % (int(playerPos.x), int(playerPos.z), int(playerPos.y)))
#    mc.setBlock(0,0,0,block.DIAMOND_BLOCK)
#    time.sleep(1)
