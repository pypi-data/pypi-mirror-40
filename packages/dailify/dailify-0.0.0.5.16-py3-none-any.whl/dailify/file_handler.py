import bpy, os, sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"
folder = argv[0]

print(folder)

stripped = folder.split('/')
full = stripped[-1]
split = full.split('_')
name = split[1]
out = "{}/{}.blend".format(folder, name)

bpy.ops.wm.save_mainfile(filepath=out)
