#!/usr/bin/env

# http://www.minecraftforum.net/topic/1701483-waterlava-bomb/

import mcpi.minecraft as minecraft
import mcpi.block as block
mc = minecraft.Minecraft.create()
problem = True
#get the size of the cube- i don't know how to error check this
length = int(input('length of side?'))
#get the fill for the cube
question = raw_input('Lava= l or Water=w?')
#loop until correct fill type selected
while problem == True:
                if question in ('l','w'):
                                problem = False
                                if question=='l':
                                                fill=block.LAVA
                                if question=='w':
                                                fill=block.WATER
                else:
                                question = raw_input('Incorrect please press l or w:')
#find where player is
playerPos = mc.player.getPos()
#buildsides of cube
for y in range(0,length):
                for x in range(0,length):
                                mc.setBlock(playerPos.x + x, playerPos.y+y+10 , playerPos.z, block.STONE)
for y in range(0,length):
                for x in range(0,length):
                                mc.setBlock(playerPos.x + x, playerPos.y+y+10 , playerPos.z- length+1, block.STONE)
for y in range(0,length):
                for z in range(0,length):
                                mc.setBlock(playerPos.x, playerPos.y+y+10 , playerPos.z-z, block.STONE)
for y in range(0,length):
                for z in range(0,length):
                                mc.setBlock(playerPos.x+length-1, playerPos.y+y+10 , playerPos.z-z, block.STONE)
#build top and bottom of cube
for x in range(0,length):
                for z in range(0,length):
                                mc.setBlock(playerPos.x+x, playerPos.y+10 , playerPos.z-z, block.STONE)
                           
for x in range(0,length):
                for z in range(0,length):
                                mc.setBlock(playerPos.x+x, playerPos.y+10+length-1 , playerPos.z-z, block.GLASS)
#FILL
for x in range(0,length-2):
                for y in range(0, length-2):
                                for z in range(0,length-2):
                                                mc.setBlock(playerPos.x + x+1, playerPos.y + y+11 , playerPos.z - z-1, fill)