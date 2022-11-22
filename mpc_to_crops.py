import getopt, sys
from mpc_cropper import crop_folder

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

  if output_folder == "":
    output_folder = "{}\\_crops".format(input_folder)

  crop_folder(input_folder, output_folder)

if __name__ == "__main__":
   main(sys.argv[1:])