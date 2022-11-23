# -*- coding: utf-8 -*-
import os, re, getopt, sys
from tempfile import TemporaryDirectory
from fpdf import FPDF
from pathlib import Path

from mpc_cropper import crop_folder, get_images_from_path

# CONSTANTS
print_name = "PRINT"
# target card size mm
card_size_w=63
card_size_h=88
# TODO: remove this from global, change checking from images per page to pages present
images_per_page_A4 = 9
images_per_page_A3 = 18

# TODO: read docs about margins
# TODO: create parent class with properties (margin_x, margin_y, images_per_page, cut_line_x, cut_line_y, pos_x, pos_y)
class A4(FPDF):
  def draw_cut_lines(self):
    # cut line positions mm
    cutline_x = [x * card_size_w for x in range(self.columns + 1)]
    cutline_y = [y * card_size_h for y in range(self.rows + 1)]
    self.set_draw_color(r=20, g=20, b=20)
    for x in cutline_x:
      self.dashed_line(x + self.margin_x, 0, x + self.margin_x, self.pdf_w, 2, 4)
    for y in cutline_y:
      self.dashed_line(0, y + self.margin_y, self.pdf_h, y + self.margin_y, 2, 4)

  def draw_page(self, image_paths, cut_lines):
    # position of columns/rows mm
    pos_x = [x * card_size_w for x in range(self.columns)]
    pos_y = [y * card_size_h for y in range(self.rows)]
    self.add_page()
    for i, image_path in enumerate(image_paths):
      coords = (pos_x[i%self.columns], pos_y[i//self.columns])
      self.image(str(image_path), w=card_size_w, h=card_size_h, x=self.margin_x+coords[0], y=self.margin_y+coords[1])
    if cut_lines:
      self.draw_cut_lines()
    #TODO: print with bleeds

  def draw_pdf(self, image_paths, cut_lines):
    # dimensions
    self.pdf_w = 210
    self.pdf_h = 297
    # margins
    self.margin_x = 10
    self.margin_y = 16
    # cards
    self.columns = 3
    self.rows = 3
    
    self.images_per_page = self.columns * self.rows

    for pagen in range(0, len(image_paths), self.images_per_page):
      self.draw_page(image_paths[pagen:pagen+self.images_per_page], cut_lines)

class A3(FPDF):
  def draw_cut_lines(self):
    # cut line positions mm
    cutline_x = [x * card_size_w for x in range(self.columns + 1)]
    cutline_y = [y * card_size_h for y in range(self.rows + 1)]
    self.set_draw_color(r=20, g=20, b=20)
    for x in cutline_x:
      self.dashed_line(x + self.margin_x, 0, x + self.margin_x, self.pdf_h, 2, 4)
    for y in cutline_y:
      self.dashed_line(0, y + self.margin_y, self.pdf_w, y + self.margin_y, 2, 4)

  def draw_page(self, image_paths, cut_lines):
    # position of columns/rows mm
    pos_x = [x * card_size_w for x in range(self.columns)]
    pos_y = [y * card_size_h for y in range(self.rows)]
    self.add_page()
    for i, image_path in enumerate(image_paths):
      coords = (pos_x[i%self.columns], pos_y[i//self.columns])
      self.image(str(image_path), w=card_size_w, h=card_size_h, x=self.margin_x+coords[0], y=self.margin_y+coords[1])
    if cut_lines:
      self.draw_cut_lines()
    #TODO: print with bleeds

  def draw_pdf(self, image_paths, cut_lines):
    # dimensions
    self.pdf_w = 297
    self.pdf_h = 420
    # margins
    self.margin_x = 16
    self.margin_y = 24
    # cards
    self.columns = 6
    self.rows = 3
    
    self.images_per_page = self.columns * self.rows

    for pagen in range(0, len(image_paths), self.images_per_page):
      self.draw_page(image_paths[pagen:pagen+self.images_per_page], cut_lines)

def main(argv):
  print ("***BEGIN***")
  help_text = 'mpc_to_pdf.py -i <input_folder> -p <max_pages_per_pdf> -f <A4|A3> -n -l'
  
  input_folder = ""
  needs_cropping = True
  cut_lines = False
  pdf_breakpages = -1
  pdf_size = "A4"

  try:
    opts, args = getopt.getopt(argv,"hi:nlp:f:",["help", "inputfolder=","nocrop=","cutlines=","pdfbreak=","format="])
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
      case "-n":
        needs_cropping = False
      case "-l":
        cut_lines = True
      case "-p":
        pdf_breakpages = (int)(arg)
      case "-f":
        pdf_size = arg

  if input_folder == "":
    print ("-i <input_folder> is mandatory")
    sys.exit(2)

  input_folder = Path(input_folder)

  print ("***FINISHED CONFIGURATION***")

  print ("Converting renders on path [{}] to PDF\nCROP RENDERS [{}] CUT LINES [{}] MAX PAGES PER PDF [{}]".format(str(input_folder), "YES" if needs_cropping else "NO", "YES" if cut_lines else "NO", "ALL" if pdf_breakpages == -1 else pdf_breakpages))

  print ("***STARTING PROCESS***")

  if needs_cropping:
    temp_dir = TemporaryDirectory()
    crops_folder = Path(temp_dir.name)
    crop_folder(input_folder, crops_folder)
  else:
    crops_folder = input_folder
    print ("***SKIPPING CROPPING RENDERS***")

  image_paths = get_images_from_path(input_folder)
  image_count = len(image_paths)
  print ("***CONVERTING {} images to PDF***".format(image_count))

  # TODO: change this so its cleaner (eg: not use n of images per format)
  images_per_pdf = image_count if pdf_breakpages < 1 else pdf_breakpages * (images_per_page_A4 if pdf_size == "A4" else images_per_page_A3)
  for pdfi in range(0, image_count, images_per_pdf):
    pdfn = (pdfi // images_per_pdf) + 1
    images_pdf = image_paths[pdfi:pdfi+images_per_pdf]
    print ("***GENERATING PDF#{}*** ({} renders)".format(pdfn, len(images_pdf)))
    # pdf based on pdf_size
    match (pdf_size):
      case "A4":
        pdf = A4("P", "mm", "A4")
      case "A3":
        pdf = A3("L", "mm", "A3")
    pdf.draw_pdf(images_pdf, cut_lines)
    # write pdf on disk
    target_file = input_folder / "{}_{}_{}.pdf".format(pdf_size, print_name, pdfn)
    pdf.output(str(target_file), 'F')
  
  print ("***FINISHED***")

if __name__ == "__main__":
   main(sys.argv[1:])