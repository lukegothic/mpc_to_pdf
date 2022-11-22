import cv2, os, numpy as np, re

# CONSTANTS
# mpc image sizes pixels
mpc_image_w = 3000
mpc_image_h = 4200
# mpc image bleed sizes pixels
mpc_image_bleed_w = 132 # each side, 3000 sans bleed
mpc_image_bleed_h = 120 # each side, 4200 sans bleed

def crop_mpc_render(image_path):
  cv2image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
  return cv2image[mpc_image_bleed_h:mpc_image_h+mpc_image_bleed_h, mpc_image_bleed_w:mpc_image_w+mpc_image_bleed_w]

#TODO: multi-threading
def crop_folder(input_folder, output_folder):
  print ("***BEGIN CROPPING RENDERS***")
  filter_re = ".*\.(png|jpg|jpeg)$"
  images = [f for f in os.listdir(input_folder) if not re.match(filter_re, f) is None]
  nimages = len(images)
  print ("***FOUND {} RENDERS TO CROP***".format(nimages))

  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  for i, image in enumerate(images):
    print ("[CROP {}/{}] {}".format(i+1, nimages, image))
    image_path = "{}\\{}".format(input_folder, image)
    image_cropped = crop_mpc_render(image_path)
    image_path_output = "{}\\{}".format(output_folder, image)
    cv2.imwrite(image_path_output, image_cropped)

  print ("***FINISHED CROPPING RENDERS***")