import bpy, os, sys

path = os.getcwd()


argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"
folder = argv[0]
split = folder.split(sep="_")
name = split[1]
out = "{}/{}.blend".format(folder, name)

bpy.ops.wm.save_mainfile(filepath=out)
