# http://www.minecraftforum.net/topic/1701517-raspberry-logo/

from PIL import Image
import mcpi.minecraft as minecraft
import mcpi.block as block
# Bring in the image - image should be a simple rpi logo savedin the same placeas this file
im=Image.open('logo3.png')
# Connect to Minecraft.
mc = minecraft.Minecraft.create()
# Identify position of player - used for vertical positioning
playerPos=mc.player.getPos()
# Find the size of the image
size = (im.getbbox())
# Create the logo in mcworld
for x in range (0,size[2]):
        for z in range (0,size[3]):
                fred=im.getpixel((x,z))
                if ((fred[1])>=50):
                        mc.setBlock(x-(size[2]/2),playerPos.y+1,z-(size[3]/2),block.WOOL.id,5) #green
                elif ((fred[0])>=50):
                        mc.setBlock(x-(size[2]/2),playerPos.y+1,z-(size[3]/2),block.WOOL.id,14) #red
                else:
                        mc.setBlock(x-(size[2]/2),playerPos.y+1,z-(size[3]/2),block.AIR)
                if ((fred[3])==0):
                        mc.setBlock(x-(size[2]/2),playerPos.y,z-(size[3]/2),block.AIR)
                else:
                        mc.setBlock(x-(size[2]/2),playerPos.y,z-(size[3]/2),block.WOOL.id,15) #black