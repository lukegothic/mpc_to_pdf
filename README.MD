GENERATES A PDF using MPC-ready render files inside a source folder.
Currently assumes that renders have 3264x4440 dimensions with bleed line, and 3000x4200 without.

INSTALLATION
pip install -r requirements.txt

USAGE
python mpc_to_pdf.py -i <PATH_TO_MPC_RENDERS>

OPTIONS
-p <pages_per_pdf>  Max number of pages per PDF, will split in multiple PDF if needed. By default it won't split into multiple PDFs.
-n                  Include this option if you don't need to crop the images. By default it crops images.
-l                  Include this option to draw cut lines on the PDF. By default it doesn't include cut-lines.

Since cropping a lot of big images is a lenghty process, I also provide a standalone and runnable file (mpc_to_crops.py) to pre-generate crops, and then on the main program you can specify option -n and point out to the crops folder to skip cropping. USAGE for that file is python mpc_to_crops.py -i <PATH_TO_MPC_RENDERS> -o <OUTPUT_FOLDER>

TODO
More informative output.
Multi-threaded cropping.
Output as A3 PDF.