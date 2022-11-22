# -*- coding: utf-8 -*-
import os, re, getopt, sys
from tempfile import TemporaryDirectory

from fpdf import FPDF

from mpc_cropper import crop_folder

# CONSTANTS
print_name = "PRINT"
# a4 size mm
pdf_w=210
pdf_h=297
# n of images per page
images_per_page = 9
# pdf margins mm
margin_w = 10
margin_h = 16
# target card size mm
card_size_w=63
card_size_h=88
# position of columns/rows mm
pos_x = [0, card_size_w, card_size_w*2]
pos_y = [0, card_size_h, card_size_h*2]
# cut line positions mm
cut_line_x = [0, card_size_w, card_size_w*2, card_size_w*3]
cut_line_y = [0, card_size_h, card_size_h*2, card_size_h*3]

class PDF(FPDF):
  def draw_cut_lines(self):
    self.set_draw_color(r=20, g=20, b=20)
    for x in cut_line_x:
      self.dashed_line(x+margin_w, 0, x+margin_w, pdf_h, 2, 4)
    for y in cut_line_y:
      self.dashed_line(0, y+margin_h, pdf_w, y+margin_h, 2, 4)

  def draw_page(self, images, cut_lines):
    self.add_page()
    for i, image in enumerate(images):
      self.image(image, w=card_size_w, h=card_size_h, x=margin_w+pos_x[i%3], y=margin_h+pos_y[i//3])
    if cut_lines:
      self.draw_cut_lines()

def main(argv):
  print ("***BEGIN***")
  help_text = 'mpc_to_pdf.py -i <input_folder> -p <max_pages_per_pdf> -n -l'
  
  inputfolder = ""
  needs_cropping = True
  cut_lines = False
  pdf_breakpages = -1
  filter_re = ".*\.(png|jpg|jpeg)$"
  pdf_size = "A4"

  try:
    opts, args = getopt.getopt(argv,"hi:nlp:",["help", "inputfolder=","nocrop=","cutlines=","pdfbreak="])
  except getopt.GetoptError:
    print (help_text)
    sys.exit(2)
  for opt, arg in opts:
    match opt:
      case "-h":
        print (help_text)
        sys.exit()
      case "-i":
        inputfolder = arg
      case "-n":
        needs_cropping = False
      case "-l":
        cut_lines = True
      case "-p":
        pdf_breakpages = (int)(arg)

  if inputfolder == "":
    print ("-i <input_folder> is mandatory")
    sys.exit(2)

  print ("***FINISHED CONFIGURATION***")

  print ("Converting renders on path [{}] to PDF\nCROP RENDERS [{}] CUT LINES [{}] MAX PAGES PER PDF [{}]".format(inputfolder, "YES" if needs_cropping else "NO", "YES" if cut_lines else "NO", "ALL" if pdf_breakpages == -1 else pdf_breakpages))

  print ("***STARTING PROCESS***")

  if needs_cropping:
    temp_dir = TemporaryDirectory()
    crops_folder = temp_dir.name
    crop_folder(inputfolder, crops_folder)
  else:
    crops_folder = inputfolder
    print ("***SKIPPING CROPPING RENDERS***")

  # get files inside folder
  images = os.listdir(crops_folder)
  images_non_filtered = len(images)
  # get images
  images = ["{}\{}".format(crops_folder, f) for f in images if not re.match(filter_re, f) is None]

  print ("***CONVERTING {} images out of {} files inside the folder***".format(len(images), images_non_filtered))

  images_per_pdf = len(images) if pdf_breakpages < 1 else pdf_breakpages * images_per_page
  for pdfi in range(0, len(images), images_per_pdf):
    pdfn = (pdfi // images_per_pdf) + 1
    images_pdf = images[pdfi:pdfi+images_per_pdf]
    print ("***GENERATING PDF#{}*** ({} renders)".format(pdfn, len(images_pdf)))
    # create pdf on memory
    pdf = PDF()
    for pagen in range(0, len(images_pdf), images_per_page):
      # draw each page of the pdf passing images_per_page
      pdf.draw_page(images_pdf[pagen:pagen+images_per_page], cut_lines)
    # write pdf on disk
    target_file = '{}\\{}_{}_{}.pdf'.format(inputfolder, pdf_size, print_name, pdfn)
    pdf.output(target_file,'F')
  
  print ("***FINISHED***")

if __name__ == "__main__":
   main(sys.argv[1:])