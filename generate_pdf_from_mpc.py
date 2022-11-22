# -*- coding: utf-8 -*-
import os, re
from fpdf import FPDF
import cv2
from tempfile import TemporaryDirectory
import numpy as np

# CONSTANTS
print_name = "_print"
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
# mpc image sizes pixels
mpc_image_w = 3000
mpc_image_h = 4200
# mpc image bleed sizes pixels
mpc_image_bleed_w = 132 # each side, 3000 sans bleed
mpc_image_bleed_h = 120 # each side, 4200 sans bleed
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

  def draw_page(self, images):
    self.add_page()
    with TemporaryDirectory() as f:
      for i, image in enumerate(images):
        if needs_cropping:
          cv2image = cv2.imdecode(np.fromfile(image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
          cv2image = cv2image[mpc_image_bleed_h:mpc_image_h+mpc_image_bleed_h, mpc_image_bleed_w:mpc_image_w+mpc_image_bleed_w]
          image = "{}\\{}.jpg".format(f, i)
          cv2.imwrite(image, cv2image)
        self.image(image, w=card_size_w, h=card_size_h, x=margin_w+pos_x[i%3], y=margin_h+pos_y[i//3])
    if cut_lines:
      self.draw_cut_lines()

# CONFIGURATION || args
folder = "E:\Proxyshop\out\crops" # MANDATORY
needs_cropping = False       # OPTIONAL WITH DEFAULT VALUE = True
filter_re = ".*\.jpg$"      # OPTIONAL WITH DEFAULT VALUE = ".*\.jpg$"
cut_lines = True            # OPTIONAL WITH DEFAULT VALUE = True
pdf_breakpages = 10         # OPTIONAL WITH DEFAULT VALUE = -1

# PROGRAM
# get files from folder
images = os.listdir(folder)
# filter files
images = ["{}\{}".format(folder, f) for f in images if not re.match(filter_re, f) is None]

images_per_pdf = len(images) if pdf_breakpages < 1 else pdf_breakpages * images_per_page
for pdfn in range(0, len(images), images_per_pdf):
  images_pdf = images[pdfn:pdfn+images_per_pdf]
  # create pdf on memory
  pdf = PDF()
  for pagen in range(0, len(images_pdf), images_per_page):
    # draw each page of the pdf passing images_per_page
    pdf.draw_page(images_pdf[pagen:pagen+images_per_page])
  # write pdf on disk
  target_file = '{}\{}_{}.pdf'.format(folder, print_name, pdfn // images_per_pdf)
  pdf.output(target_file,'F')
