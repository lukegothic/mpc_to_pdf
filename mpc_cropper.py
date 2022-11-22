import cv2, os, numpy as np, re

# CONSTANTS
# mpc image sizes pixels
mpc_image_w = 3000
mpc_image_h = 4200
# mpc image bleed sizes pixels
mpc_image_bleed_w = 132 # each side, 3000 sans bleed
mpc_image_bleed_h = 120 # each side, 4200 sans bleed

# CONFIGURATION || args
folder = "E:\Proxyshop\out" # MANDATORY
output = "E:\Proxyshop\out\crops"       # OPTIONAL WITH DEFAULT VALUE = "{}\crops".format(folder)
filter_re = ".*\.jpg$"      # OPTIONAL WITH DEFAULT VALUE = ".*\.jpg$"

images = os.listdir(folder)
# filter files
images = [f for f in images if not re.match(filter_re, f) is None]

for image in images:
  image_path = "{}\\{}".format(folder, image)
  cv2image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
  cv2image = cv2image[mpc_image_bleed_h:mpc_image_h+mpc_image_bleed_h, mpc_image_bleed_w:mpc_image_w+mpc_image_bleed_w]
  image_path_output = "{}\\{}".format(output, image)
  cv2.imwrite(image_path_output, cv2image)

#TODO: hacerlo callable desde otros scripts (def xxx:)
#TODO: multi-threading