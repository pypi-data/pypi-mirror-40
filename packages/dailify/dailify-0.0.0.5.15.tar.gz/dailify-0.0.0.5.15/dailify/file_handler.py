import bpy, os, sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"
folder = argv[0]

print(folder)

out = "{}/{}.blend".format(folder, "test")

bpy.ops.wm.save_mainfile(filepath=out)
