#! /usr/bin/python
import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import time

""" drawMandelbrot draws the mandelbrot set
    @author: goldfish"""

def pickBlock( iterations, maxIt ):
    #blockChoice = int( 10 * iterations / maxIt )
    blockChoice = iterations
    if blockChoice == 0:
        return( block.STONE )
    elif blockChoice == 1:
        return( block.DIRT )
    elif blockChoice == 2:
        return( block.GRASS )
    elif blockChoice == 3:
        return( block.SAND )
    elif blockChoice == 4:
        return( block.WOOD )
    elif blockChoice == 5:
        return( block.WOOD_PLANKS )
    elif blockChoice == 6:
        return( block.LAPIS_LAZULI_BLOCK )
    elif blockChoice == 7:
        return( block.COAL_ORE )
    elif blockChoice == 8:
        return( block.IRON_ORE )
    elif blockChoice == 9:
        return( block.WOOL )
    elif blockChoice == 10:
        return( block.GLASS )
    else:
        return( block.WATER )

def drawMandelbrot( xloc, yloc, zloc, imgx, imgy, maxIt, xa, ya, xb, yb ):
    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1)  + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1)  + xa
            z = zx + zy * 1j
            c = z
            for i in range(maxIt):
                if abs(z) > 2.0: break 
                z = z * z + c
            mc.setBlock( xloc+x, yloc, zloc+y, pickBlock( i, maxIt ) )

if __name__ == "__main__":
    mc = minecraft.Minecraft.create( server.address )
    mc.postToChat("Drawing Mandelbrot set")
    time.sleep(1)
    #drawMandelbrot( -128, -1, -128, 256, 256, 14, -1.6, 0.0, -1.0, 0.3 )
    # drawMandelbrot( -40, -1, -40, 80, 80, 100, -1.6, 0.0, -1.0, 0.3 )
    drawMandelbrot( -30, -1, -30, 60, 60, 254, -2.0, -1.5, 1.0, 1.5 )
    # drawMandelbrot( -128, -1, -128, 256, 256, 255, -2.0, -1.5, 1.0, 1.5 )
