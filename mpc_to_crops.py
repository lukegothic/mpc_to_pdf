import getopt, sys
from mpc_cropper import crop_folder
from pathlib import Path

def main(argv):
  print ("***BEGIN***")
  help_text = 'mpc_cropper.py -i <input_folder> -o <output_folder>'
  
  input_folder = ""
  output_folder = ""

  try:
    opts, args = getopt.getopt(argv,"hi:o:",["help", "inputfolder=","outputfolder="])
  except getopt.GetoptError:
    print (help_text)
    sys.exit(2)
  for opt, arg in opts:
    match opt:
      case "-h":
        print (help_text)
        sys.exit()
      case "-i":
        input_folder = arg
      case "-o":
        output_folder = arg

  if input_folder == "":
    print ("-i <input_folder> is mandatory")
    sys.exit(2)

  input_folder = Path(input_folder)

  if output_folder == "":
    output_folder = input_folder / "_crops"
  else:
    output_folder = Path(output_folder)

  crop_folder(input_folder, output_folder)

if __name__ == "__main__":
   main(sys.argv[1:])