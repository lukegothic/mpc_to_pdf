import cv2, numpy as np

# CONSTANTS
# mpc image sizes pixels
mpc_image_w = 3000
mpc_image_h = 4200
# mpc image bleed sizes pixels
mpc_image_bleed_w = 132 # each side, 3000 sans bleed
mpc_image_bleed_h = 120 # each side, 4200 sans bleed

# path: Path
# image_extensions (opcional) : Array de extensiones
# TODO: a pyluke
def get_images_from_path(path, image_extensions=[".png", ".jpg", ".jpeg"]):
  return [f for f in path.iterdir() if f.is_file() and f.suffix in image_extensions]

# image_path: Path
def crop_mpc_render(image_path):
  cv2image = cv2.imdecode(np.fromfile(str(image_path), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
  return cv2image[mpc_image_bleed_h:mpc_image_h+mpc_image_bleed_h, mpc_image_bleed_w:mpc_image_w+mpc_image_bleed_w]

#TODO: multi-threading
# input_folder: Path
# output_folder: Path
def crop_folder(input_folder, output_folder):
  print ("***BEGIN CROPPING RENDERS***")
  image_paths = get_images_from_path(input_folder)
  nimages = len(image_paths)
  print ("***FOUND {} RENDERS TO CROP***".format(nimages))

  if not output_folder.exists():
    output_folder.mkdir()

  for i, image_path in enumerate(image_paths):
    print ("[CROP {}/{}] {}".format(i+1, nimages, image_path.name))
    image_cropped = crop_mpc_render(image_path)
    image_path_output = output_folder / image_path.name
    cv2.imwrite(str(image_path_output), image_cropped)

  print ("***FINISHED CROPPING RENDERS***")