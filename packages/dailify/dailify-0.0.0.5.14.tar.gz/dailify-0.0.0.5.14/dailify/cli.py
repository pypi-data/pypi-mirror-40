


import argparse, random, os






def main():
  parser = argparse.ArgumentParser(description="Ghent Theft Module")
  parser.add_argument("-d", "--daily", type=str, required=True,  dest="daily", help="String input for the daily name.")
  parser.add_argument("-l", "--launch", action="store_true", required=False, help="Opens a new Blender file at the correct location.")
  
  identifier = "".join([str(random.randint(0, 9)) for x in range(6)])
  uid = " ".join([str(random.randint(0, 9)) for x in range(6)])
  
  args = parser.parse_args()
  name = args.daily
  spaced = " ".join(name.upper())
  temp = " ".join([uid, "-", spaced])
  friendly = "_".join([str(identifier), name])
  

  os.makedirs(friendly)
  folderpath = "/".join([os.getcwd(), friendly])
  runpath = os.path.realpath(__file__)
  stripped = runpath.replace('cli.py', 'file_handler.py')

  if args.launch == True:
    os.system('blender --python {} -- {}'.format(stripped, folderpath))
    
  #print(os.getcwd())


if __name__ == "__main__":
  main()