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
usage: minescan [-hcevj] [-x num] [-y num] [-z num]
[-X num] [-Y num] [-Z num] [-o outputfile]

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

-j: If specified, scripts assumes it's running on RaspberryJuice which doesn't
support the getBlockWithData command.  As a result, some detail won't be scanned.

MineScan needs to be told the xyz coordinates of where to scan and/or create
the container and the how far to scan.  This is done by specifying:

-x num: The starting value of x.  This can be positive or negative
-y num: The starting value of y.  This can be positive or negative
-z num: The starting value of z.  This can be positive or negative
-X num: The starting value of X.  This can be positive or negative
-Y num: The starting value of Y.  This can be positive or negative
-Z num: The starting value of Z.  This can be positive or negative

The defaults are as follows:
x = 0, y = 0, z = 0, X = 10, Y = 10, Z = 10
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


# I've considered writing this as a class and sharing data via member variables, however I want this
# script to be easy to understand for anyone that is starting to learn python
# as a result I'm passing all arguments to the function.  It's ugly but easier for someone starting to learn.
def generate_container(mc, opt_ispy, opt_x1, opt_y1, opt_z1, opt_x2, opt_y2, opt_z2, verbose, opt_container, opt_container_empty):
    if verbose:
        print "Creating Container(%s, %s, %s, %s, %s, %s)" % (opt_x1, opt_y1, opt_z1, opt_x2, opt_y2, opt_z2)
    if not opt_container_empty:
        # this will create an glass container without attempting to keep what's inside.
        # it does this by creating a large filled glass container, than hollowing it out with air
        # thus removing anything inside.
        mc.setBlocks(opt_x1-1,opt_y1-1,opt_z1-1,opt_x2+1,opt_y2+1,opt_z2+1,block.GLASS.id)
        mc.setBlocks(opt_x1,opt_y1,opt_z1,opt_x2,opt_y2,opt_z2,block.AIR.id)
    else:
        # this will create a glass container around whatever is inside.
        # as a result this takes additional steps as it has to create each of the 6 sides.
        mc.setBlocks(opt_x1-1,opt_y1-1,opt_z1-1,opt_x2+1,opt_y2+1,opt_z1-1, block.GLASS.id)
        mc.setBlocks(opt_x1-1,opt_y1-1,opt_z1-1,opt_x1-1,opt_y2+1,opt_z2+1, block.GLASS.id)
        mc.setBlocks(opt_x1-1,opt_y1-1,opt_z1-1,opt_x2+1,opt_y1-1,opt_z2+1, block.GLASS.id) # floor
        mc.setBlocks(opt_x1-1,opt_y2+1,opt_z1-1,opt_x2+1,opt_y2+1,opt_z2+1, block.GLASS.id) # roof
        mc.setBlocks(opt_x2+1,opt_y1-1,opt_z2+1,opt_x2+1,opt_y2+1,opt_z1-1, block.GLASS.id)
        mc.setBlocks(opt_x2+1,opt_y1-1,opt_z2+1,opt_x1-1,opt_y2+1,opt_z2+1, block.GLASS.id)
    return

def minescan(mc, opt_ispy, opt_x1, opt_y1, opt_z1, opt_x2, opt_y2, opt_z2, verbose, output_file):
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

# The following was generated by minescan.py from mcpipy.com
""")


    # write the rest of your code here...
    #    mc.postToChat("Hello MCPIPY World!")
    total_cycles = ((opt_x2 - opt_x1)+1) * ((opt_y2 - opt_y1)+1) * ((opt_z2 - opt_z1)+1)
    if verbose:
        print "Scanning %d blocks" % total_cycles
    cycle = 0

    block_data = 0
    for y in range(0, (opt_y2 - opt_y1)+1):
        for x in range(0, (opt_x2 - opt_x1)+1):
            for z in range(0, (opt_z2 - opt_z1)+1):

                if opt_ispy:
                    (block_id, block_data) = mc.getBlockWithData(opt_x1 + x,opt_y1 + y,opt_z1 + z)
                else:
                    block_id = mc.getBlock(opt_x1 + x,opt_y1 + y,opt_z1 + z)
#                block_id = 0
                if block_id:
                    if str(block_id) in block_id_to_name:
                        if block_data:
                            if verbose:
                                print "mc.getBlockWithData(%s,%s,%s) = %s, %s" % (x,y,z,block_id_to_name[str(block_id)],block_data)
                            py_out.write("mc.setBlock(%s,%s,%s,block.%s.id,%s)\n" % (x,y,z,block_id_to_name[str(block_id)],block_data))
                        else:
                            if verbose:
                                print "mc.getBlock(%s,%s,%s) = %s" % (x,y,z,block_id_to_name[str(block_id)])
                            py_out.write("mc.setBlock(%s,%s,%s,block.%s.id)\n" % (x,y,z,block_id_to_name[str(block_id)]))
                    else: # Block ID not defined in MCPI v0.1.1
                        if block_data:
                            if verbose:
                                print "mc.getBlockWithData(%s,%s,%s) = %s, %s" % (x,y,z,block_id, block_data)
                            py_out.write("# Note this block is not supported in Minecraft Pi Edition v0.1.1\n")
                            py_out.write("mc.setBlock(%s,%s,%s,%s,%s)\n" % (x,y,z,block_id, block_data))
                        else:
                            if verbose:
                                print "mc.getBlock(%s,%s,%s) = %s" % (x,y,z,block_id)
                            py_out.write("# Note this block is not supported in Minecraft Pi Edition v0.1.1\n")
                            py_out.write("mc.setBlock(%s,%s,%s,%s)\n" % (x,y,z,block_id))
                else: # No block id returned
                    if verbose:
                        print "mc.getBlock(%s,%s,%s) = %s" % (x,y,z,block_id_to_name[str(block_id)])
                cycle += 1

                # Print this once every 10 cycles
                if not cycle % 10:
                    percent_complete = (float(cycle) / float(total_cycles)) * 100
                    print "[%d/%d] %.f%s complete" % (cycle, total_cycles, percent_complete, "%")

    py_out.write("mc.postToChat('World Re-created!')\n")

    try:
        os.fchmod(py_out.fileno(), 0755)
    except:
        print "Unable to set execute bit"
    py_out.close()



def main(argv):
    global server_address

    output_file = "my-minescanned-%s.py" % (time.strftime("%Y%m%d-%H%M%S"))
    opt_x1 = 0
    opt_y1 = 0
    opt_z1 = 0
    opt_x2 = 10
    opt_y2 = 10
    opt_z2 = 10
    opt_ispy = True

#    verbose = True
    verbose = False
    opt_container_empty = False
    opt_container = False

    try:
        # h = help
        # o: = set output file
        # x: = set opt_x
        # y: = set opt_y
        # z: = set opt_z
        # x: = set opt_x
        # y: = set opt_y
        # z: = set opt_z        
        # c = create container, don't scan
        # e = create empty container, don't scan
        # v = verbose mode
        # s: = server ip
        opts, args = getopt.getopt(argv,"ho:x:y:z:X:Y:Z:b:u:cevs:j",["ofile="])
    except getopt.GetoptError:
        usage(2, output_file)
    for opt, arg in opts:
        if opt == '-h':
            usage(0, output_file)
        elif opt == '-x':
            opt_x1 = int(arg)
        elif opt == '-y':
            opt_y1 = int(arg)
        elif opt == '-z':
            opt_z1 = int(arg)
        elif opt == '-X':
            opt_x2 = int(arg)
        elif opt == '-Y':
            opt_y2 = int(arg)
        elif opt == '-Z':
            opt_z2 = int(arg)
        elif opt == '-j':
            opt_ispy = False
        elif opt == '-v':
            verbose = True
        elif opt == '-e':
            opt_container = True
        elif opt == '-c':
#            opt_container = True
            opt_container_empty = True
        elif opt == '-s':
            server_address = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    if (opt_x2 <= opt_x1) or (opt_y2 <= opt_y1) or (opt_z2 <= opt_z1):
        print "Error, the second number must always be greater than the first number."
        print """
x1 = "%s"
x2 = "%s"
y1 = "%s"
y2 = "%s"
z1 = "%s"
z2 = "%s"
""" % (opt_x1, opt_x2, opt_y1, opt_y2, opt_z1, opt_z2)
        print "Exiting"
        sys.exit(-1)
    if verbose:
        print """
Options as follows:
output file = "%s"
x1 = "%s"
x2 = "%s"
y1 = "%s"
y2 = "%s"
z1 = "%s"
z2 = "%s"
Create Container: %s
Create Empty Container: %s
Server: %s
Is Raspberry Pi: %s

""" % (output_file, opt_x1, opt_x2, opt_y1, opt_y2, opt_z1, opt_z2,
       opt_container, opt_container_empty, server_address, opt_ispy)
    elif not opt_container and not opt_container_empty:
        print 'Output file is "%s"' % (output_file)

    mc = minecraft.Minecraft.create(server_address)

    if opt_container or opt_container_empty:
        generate_container(mc, opt_ispy, opt_x1, opt_y1, opt_z1, opt_x2, opt_y2, opt_z2, verbose, opt_container, opt_container_empty)
    else:
        minescan(mc, opt_ispy, opt_x1, opt_y1, opt_z1, opt_x2, opt_y2, opt_z2, verbose, output_file)

if __name__ == "__main__":
    main(sys.argv[1:])