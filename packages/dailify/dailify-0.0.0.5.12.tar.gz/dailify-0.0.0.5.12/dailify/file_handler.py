import bpy, os, sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"
folder = argv[0]
name = argv[1]
out = "{}/{}.blend".format(folder, name)

bpy.ops.wm.save_mainfile(filepath=out)
