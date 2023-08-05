


import argparse, random, os





def main():
  parser = argparse.ArgumentParser(description="Ghent Theft Module")
  parser.add_argument("-d", "--daily", type=str, dest="daily")
  
  uid = " ".join([str(random.randint(0, 9)) for x in range(6)])
  
  
  args = parser.parse_args()
  name = args.daily.upper()
  spaced = " ".join(name)
  temp = " ".join([uid, "-", spaced])
  
  print(temp)
  print(os.getcwd())


if __name__ == "__main__":
  main()