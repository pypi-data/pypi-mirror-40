


import argparse, random, os, pyperclip

import subprocess





def main():
  parser = argparse.ArgumentParser(description="Ghent Theft Module")
  parser.add_argument("-d", "--daily", type=str, required=True,  dest="daily", help="String input for the daily name.")
  parser.add_argument("-l", "--launch", action="store_true", required=False, help="Opens a new Blender file at the correct location.")
  uid = " ".join([str(random.randint(0, 9)) for x in range(6)])
  
  
  args = parser.parse_args()
  name = args.daily.upper()
  spaced = " ".join(name)
  temp = " ".join([uid, "-", spaced])
  pyperclip.copy(temp)
  print(temp)
  if args.launch == True:
    os.system("blender")
  #print(os.getcwd())


if __name__ == "__main__":
  main()