#!/usr/bin/env python

#import the minecraft.py module from the minecraft directory
import mcpi.minecraft as minecraft
#import minecraft block module
import mcpi.block as block
#import time, so delays can be used
import time
import os
import getopt
import sys
try:
    import server
    server_address = server.address
except:
    server_address = "127.0.0.1"

block_id_to_name = {
    '0':'AIR',
    '1':'STONE',
    '2':'GRASS',
    '3':'DIRT',
    '4':'COBBLESTONE',
    '5':'WOOD_PLANKS',
    '6':'SAPLING',
    '7':'BEDROCK',
    '8':'WATER_FLOWING',
    '9':'WATER_STATIONARY',
    '10':'LAVA_FLOWING',
    '11':'LAVA_STATIONARY',
    '12':'SAND',
    '13':'GRAVEL',
    '14':'GOLD_ORE',
    '15':'IRON_ORE',
    '16':'COAL_ORE',
    '17':'WOOD',
    '18':'LEAVES',
    '20':'GLASS',
    '21':'LAPIS_LAZULI_ORE',
    '22':'LAPIS_LAZULI_BLOCK',
    '24':'SANDSTONE',
    '26':'BED',
    '30':'COBWEB',
    '31':'GRASS_TALL',
    '35':'WOOL',
    '37':'FLOWER_YELLOW',
    '38':'FLOWER_CYAN',
    '39':'MUSHROOM_BROWN',
    '40':'MUSHROOM_RED',
    '41':'GOLD_BLOCK',
    '42':'IRON_BLOCK',
    '43':'STONE_SLAB_DOUBLE',
    '44':'STONE_SLAB',
    '45':'BRICK_BLOCK',
    '46':'TNT',
    '47':'BOOKSHELF',
    '48':'MOSS_STONE',
    '49':'OBSIDIAN',
    '50':'TORCH',
    '51':'FIRE',
    '53':'STAIRS_WOOD',
    '54':'CHEST',
    '56':'DIAMOND_ORE',
    '57':'DIAMOND_BLOCK',
    '58':'CRAFTING_TABLE',
    '60':'FARMLAND',
    '61':'FURNACE_INACTIVE',
    '62':'FURNACE_ACTIVE',
    '64':'DOOR_WOOD',
    '65':'LADDER',
    '67':'STAIRS_COBBLESTONE',
    '71':'DOOR_IRON',
    '73':'REDSTONE_ORE',
    '78':'SNOW',
    '79':'ICE',
    '80':'SNOW_BLOCK',
    '81':'CACTUS',
    '82':'CLAY',
    '83':'SUGAR_CANE',
    '85':'FENCE',
    '89':'GLOWSTONE_BLOCK',
    '95':'BEDROCK_INVISIBLE',
    '98':'STONE_BRICK',
    '102':'GLASS_PANE',
    '103':'MELON',
    '107':'FENCE_GATE',
    '246':'GLOWING_OBSIDIAN',
    '247':'NETHER_REACTOR_CORE'
    }



def usage(exit_val, output_file):
    print """
usage: minescan [-hcev] [-x num] [-y num] [-z num] [-b num] [-u num]
[-o outputfile]

MineScan will connect to Minecraft PI Edition server or Bukkit Server using the
RaspberryJuice plugin. It will by default scan a region and generate a python
script which can be used to regenerate the blocks in that region.

There is also an option to create a glass box around the region it will scan.
This can be used to first define an area in which you will later create something
in minecraft, then scan it.

The options are as follows:

-h: this Help message on how to use minescan

-c: Create a glass container around the specified coordinates.  Doesn't affect
what's inside the container.

-e: Creates a EMPTY glass container.  This will annihilate anything inside the
glass container.

-v: Verbose output on the console, prints information on what's found...

MineScan needs to be told the xyz coordinates of where to scan and/or create
the container and the how far to scan.  This is done by specifying:

-x num: The starting value of x.  This can be positive or negative
-y num: The starting value of y.  This can be positive or negative
-z num: The starting value of z.  This can be positive or negative
-b num: This represents the number of blocks on the horizontal to scan.  This
is added to x and z.
-u num: This represents the number of blocks up to scan from y.  This is
added to y.

The defaults are as follows:
x = 0, y = 0, z = 0, b = 10, u = 10.
This means that the program will scan and/or create a container
from 0,0,0 to 10,10,10.

Note that when scanning the program must scan each block one by one,
so in the above example 10 * 10 * 10 or 1000 blocks must be scanned.  This
takes some time. So if you increase these numbers significantly it will take
some time to complete!

Finally...

-o filename: specifies what file to output, such as "scanned.py".  If this
file exists, it will be overwritten! The default is to create a filename with
a prefix of "my-minescanned" with the date/time and a ".py".
If not specified, this time the program would have output to %s

-s address: Specifies the IP address/hostname of the Minecraft Server.
Default is 127.0.0.1 (local machine)

""" % (output_file)
    sys.exit(exit_val)

def generate_container(mc, opt_x, opt_y, opt_z, opt_b, opt_u, verbose, opt_container, opt_container_empty):
    x1 = opt_x
    x2 = opt_x + opt_b
    y1 = opt_y
    y2 = opt_y + opt_u
    z1 = opt_z
    z2 = opt_z + opt_b

#    mc.setBlocks(-50,-10,-50,50,10,50,block.AIR.id)
#    mc.setBlocks(-50,0,-50,50,-10,50,block.SANDSTONE.id)
    if not opt_container_empty:
        mc.setBlocks(x1-1,y1-1,z1-1,x2+1,y2+1,z2+1,block.GLASS.id)
        mc.setBlocks(x1,y1,z1,x2,y2,z2,block.AIR.id)

    else:
#        mc.setBlocks(-1,-1,-1,11,11,-1, block.GLASS.id)
#        mc.setBlocks(-1,-1,-1,-1,11,11, block.GLASS.id)
#        mc.setBlocks(-1,-1,-1,11,-1,11, block.GLASS.id)
#        mc.setBlocks(-1,11,-1,11,11,11, block.GLASS.id)
#        mc.setBlocks(11,-1,11,11,11,-1, block.GLASS.id)
#        mc.setBlocks(11,-1,11,-1,11,11, block.GLASS.id)
#

        mc.setBlocks(x1-1,y1-1,z1-1,x2+1,y2+1,z1-1, block.GLASS.id)
        mc.setBlocks(x1-1,y1-1,z1-1,x1-1,y2+1,z2+1, block.GLASS.id)
        mc.setBlocks(x1-1,y1-1,z1-1,x2+1,y1-1,z2+1, block.GLASS.id) # floor
        mc.setBlocks(x1-1,y2+1,z1-1,x2+1,y2+1,z2+1, block.GLASS.id) # roof
        mc.setBlocks(x2+1,y1-1,z2+1,x2+1,y2+1,z1-1, block.GLASS.id)
        mc.setBlocks(x2+1,y1-1,z2+1,x1-1,y2+1,z2+1, block.GLASS.id)


def minescan(mc, opt_x, opt_y, opt_z, opt_b, opt_u, verbose, output_file):
    try:
        py_out = open(output_file, "w")
    except:
        print "Unable to open file %s for writing, exiting" % (output_file)
        sys.exit(1)


    py_out.write("""#!/usr/bin/env python
# generated by minescan.py from mcpipy.com

import mcpi.minecraft as minecraft
import mcpi.block as block
import server

mc = minecraft.Minecraft.create(server.address)
mc.postToChat("Re-creating world")

# The following was generated by brooksc_minescraper.py from mcpipy.com
""")


    # write the rest of your code here...
    #    mc.postToChat("Hello MCPIPY World!")
    total_cycles = (opt_u * opt_b * opt_b)
    if verbose:
        print "Scanning %d blocks" % total_cycles
    cycle = 0
    for y in range(0, opt_u):
        for x in range(0, opt_b):
            for z in range(0, opt_b):

                block_id = mc.getBlock(opt_x + x,opt_y + y,opt_z + z)
                if block_id:
                    if str(block_id) in block_id_to_name:
                        if verbose:
                            print "mc.getblock(%s,%s,%s) = %s" % (x,y,z,block_id_to_name[str(block_id)])
                        py_out.write("mc.setBlock(%s,%s,%s,block.%s.id)\n" % (x,y,z,block_id_to_name[str(block_id)]))
                    else:
                        if verbose:
                            print "mc.getblock(%s,%s,%s) = %s" % (x,y,z,block_id)
                        py_out.write("# Note this block is not supported in Minecraft Pi Edition v0.1.1\n")
                        py_out.write("mc.setBlock(%s,%s,%s,%s)\n" % (x,y,z,block_id))
                else:
                #                print "# mc.getblock(%s,%s,%s) = %s" % (x,y,z,block_id)
                    if verbose:
                        print "mc.getblock(%s,%s,%s) = %s" % (x,y,z,block_id_to_name[str(block_id)])
                cycle += 1

                percent_complete = (float(cycle) / float(total_cycles)) * 100
                print "[%d/%d] %.f%s complete" % (cycle, total_cycles, percent_complete, "%")


    py_out.write("mc.postToChat('World Re-created!')\n")

    try:
        os.fchmod(py_out.fileno(), 0755)
    except:
        print "Unable to set execute bit"
    py_out.close()



def main(argv):
#    global output_file
#    global server_address
#    global opt_x
#    global opt_y
#    global opt_z
#    global opt_b
#    global opt_u
#    global verbose
#    global opt_container
#    global opt_container_empty
#    global verbose
    global server_address

    output_file = "my-minescanned-%s.py" % (time.strftime("%Y%m%d-%H%M%S"))
    opt_x = 0
    opt_y = 0
    opt_z = 0
    # specifies how many blocks to extend out from x and z
    opt_b = 10
    # specifies how many blocks up from y to search
    # e.g. if y = 0 and u = 10, then it will search up to y=10
    opt_u = 10
    #verbose = True
    verbose = False
    opt_container_empty = False
    opt_container = False

#    inputfile = ''
#    output_file = ''


    try:
        # h = help
        # o: = set output file
        # x: = set loc_x
        # y: = set loc_y
        # z: = set loc_z
        # b: = set loc_b, # of blocks
        # u: = set loc_u
        # c = create container, don't scan
        # a = annihilate (with -c only)
        # v = verbose mode
        # s: = server ip
        opts, args = getopt.getopt(argv,"ho:x:y:z:b:u:cevs:",["ofile="])
    except getopt.GetoptError:
        usage(2, output_file)
    for opt, arg in opts:
        if opt == '-h':
            usage(0, output_file)
        elif opt == '-x':
            opt_x = int(arg)
        elif opt == '-y':
            opt_y = int(arg)
        elif opt == '-z':
            opt_z = int(arg)
        elif opt == '-b':
            opt_b = int(arg)
        elif opt == '-u':
            opt_u = int(arg)
        elif opt == '-v':
            verbose = True
        elif opt == '-e':
            opt_container = True
        elif opt == '-c':
            opt_container = True
            opt_container_empty = True
        elif opt == '-s':
            server_address = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

#    print 'Input file is "', inputfile
    if verbose:
        print 'Output file is "', output_file


    mc = minecraft.Minecraft.create(server_address)

    if opt_container or opt_container_empty:
        generate_container(mc, opt_x, opt_y, opt_z, opt_b, opt_u, verbose, opt_container, opt_container_empty)
    else:
        minescan(mc, opt_x, opt_y, opt_z, opt_b, opt_u, verbose, output_file)

if __name__ == "__main__":
    main(sys.argv[1:])