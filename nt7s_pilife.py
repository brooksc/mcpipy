# http://www.nt7s.com/blog/2013/02/fancier-minecraft-pi-game-of-life/
# pilife.py
#
# Jason Milldrum
# 18 Feb 2013
#
# www.nt7s.com/blog
 
import minecraft.minecraft as minecraft
import minecraft.block as block
import numpy
import random
 
mc = minecraft.Minecraft.create()
 
# World size in x and z axes
#worldSize = 64
 
# Bounds of x and z axes
negLimit = -32
posLimit = 31
 
# Bounds of y axis
yNegLimit = -64
yPosLimit = 64
 
# Y coord of Life world floor
worldFloor = 0
 
# Number of steps in the surrounding wall
maxWallHeight = 5
 
# Initialize the Life world
theWorld = numpy.zeros((posLimit - negLimit + 1, posLimit - negLimit + 1), dtype=numpy.bool)
theNextWorld = numpy.zeros((posLimit - negLimit + 1, posLimit - negLimit + 1), dtype=numpy.bool)
for x in range(posLimit - negLimit):
	for y in range(posLimit - negLimit):
		theWorld[x][y] = random.randint(0,1)
 
# Clear everything at the world surface and above inside the Life play area
mc.setBlocks(negLimit - (maxWallHeight * 2), worldFloor, negLimit - (maxWallHeight * 2), posLimit + (maxWallHeight * 2) - 1, yPosLimit, posLimit + (maxWallHeight * 2) - 1, block.AIR)
 
# Let's create stairsteps around the Life world
 
# Start with the +x direction
x = posLimit
stepHeight = worldFloor
# Up
while stepHeight <= maxWallHeight:
	mc.setBlocks(x, worldFloor, negLimit - stepHeight - 1, x, stepHeight, posLimit + stepHeight, block.BEDROCK)
	x += 1
	stepHeight += 1
# Down
stepHeight = maxWallHeight
while stepHeight >= worldFloor:
	mc.setBlocks(x, worldFloor, negLimit - stepHeight - 1, x, stepHeight, posLimit + stepHeight, block.BEDROCK)
	x += 1
	stepHeight -= 1
 
# Now the -x direction
x = negLimit - 1
stepHeight = worldFloor
# Up
while stepHeight <= maxWallHeight:
	mc.setBlocks(x, worldFloor, negLimit - stepHeight - 1, x, stepHeight, posLimit + stepHeight, block.BEDROCK)
	x -= 1
	stepHeight += 1
# Down
stepHeight = maxWallHeight
while stepHeight >= worldFloor:
	mc.setBlocks(x, worldFloor, negLimit - stepHeight - 1, x, stepHeight, posLimit + stepHeight, block.BEDROCK)
	x -= 1
	stepHeight -= 1
 
# Next the +z direction
z = posLimit
stepHeight = worldFloor
# Up
while stepHeight <= maxWallHeight:
	mc.setBlocks(negLimit - stepHeight - 1, worldFloor, z, posLimit + stepHeight, stepHeight, z, block.BEDROCK)
	z += 1
	stepHeight += 1
# Down
stepHeight = maxWallHeight
while stepHeight >= worldFloor:
	mc.setBlocks(negLimit - stepHeight - 1, worldFloor, z, posLimit + stepHeight, stepHeight, z, block.BEDROCK)
	z += 1
	stepHeight -= 1
 
# Finally the -z direction
z = negLimit - 1
stepHeight = worldFloor
# Up
while stepHeight <= maxWallHeight:
	mc.setBlocks(negLimit - stepHeight - 1, worldFloor, z, posLimit + stepHeight, stepHeight, z, block.BEDROCK)
	z -= 1
	stepHeight += 1
# Down
stepHeight = maxWallHeight
while stepHeight >= worldFloor:
	mc.setBlocks(negLimit - stepHeight - 1, worldFloor, z, posLimit + stepHeight, stepHeight, z, block.BEDROCK)
	z -= 1
	stepHeight -= 1
 
# Set the player right in the middle of the world
mc.player.setPos(0, worldFloor, 0)
 
# Main processing loop
while True:
	# Display theWorld
	for x in range(posLimit - negLimit):
		for y in range(posLimit - negLimit):
			if theWorld[x][y] == True:
				mc.setBlock(x + negLimit, worldFloor, y + negLimit, block.DIAMOND_BLOCK)
			else:
				mc.setBlock(x + negLimit, worldFloor, y + negLimit, block.OBSIDIAN)
 
	# Check number of neighbors alive
	for x in range(posLimit - negLimit):
		for y in range(posLimit - negLimit):
			
			if x == 0:
				xMinus = posLimit - negLimit
			else:
				xMinus = x - 1
 
			if x == posLimit - negLimit:
				xPlus = 0
			else:
				xPlus = x + 1
 
			if y == 0:
				yMinus = posLimit - negLimit
			else:
				yMinus = y - 1
 
			if y == posLimit - negLimit:
				yPlus = 0
			else:
				yPlus = y + 1
 
			alive = 0			
 
			if theWorld[xPlus][yPlus]:
				alive += 1
			if theWorld[x][yPlus]:
				alive += 1
			if theWorld[xMinus][yPlus]:
				alive += 1
			if theWorld[xPlus][y]:
				alive += 1
			if theWorld[xMinus][y]:
				alive += 1
			if theWorld[xPlus][yMinus]:
				alive += 1
			if theWorld[x][yMinus]:
				alive += 1
			if theWorld[xMinus][yMinus]:
				alive += 1
 
			# Calculate which cells live and die in next generation
			if theWorld[x][y] == False:
				if alive == 3:
					theNextWorld[x][y] = True
			else:
				if alive < 2:
					theNextWorld[x][y] = False
				elif alive > 3:
					theNextWorld[x][y] = False
				else:
					theNextWorld[x][y] = True
	# Copy array
	theWorld = theNextWorld.copy()