Image File Name Fixer
======================================

### STATUS:
* master:  TODO: CI Integration.
* develop:  TODO: CI Integration.

======================================
### Table of Contents
1. [Purpose](https://gitlab.com/jeremymreed/image-file-name-fixer#purpose)
2. [Usage](https://gitlab.com/jeremymreed/image-file-name-fixer#usage)
3. [License](https://gitlab.com/jeremymreed/image-file-name-fixer#license)


# Purpose:
This python script takes image files, and modifies their names to
conform to a standard naming scheme.
names should be <image-name>-<image-resolution>.<extension>

To run the app without any destructive changes, pass in --dry-run
as an argument

This app can write its output fixed files three ways.
1. If an output directory is passed in as an argument (-o, --output)
all output fixed files are written to this directory.  This option
overrides the in place option.
2. In place.  If --in-place is passed in, the app will write output
fixed files in the same directory as the input file.  This option
is overridden if an output directory is passed in.
3. Current Working Directory.  This is the default.  If neither
of the two options above are specified, the app will write the
output fixed files to the directory the app is run in.

Fields:
image-name: String, just a descriptive string of what the image is.
This tool does not modify this field.

image-resolution:  String, in the format of XRESxYRES, where:
  XRES is a numeric string representing the x resolution.
  YRES is a numeric string representing the y resolution.
  These two numeric strings should be separated by a lower case 'x'.
  e.g. '1920x1080'

This script should not alter image-name, but ensure that an image-resolution
field exists.  If this field already exists, we check the image to be sure
that the image-resolution field is accurate, and is in the correct
position within the file name.

If it does not exist, we check the image for its resolution, and add the
image-resolution field to the file name in the correct position.

The image-name field can be set manually.

This script will use Pillow to get image-resolution information.

# Usage:
This script is intended to either be installed via pip, or run as
a module from the command line.

To run as a module from the command line:
```
git clone https://gitlab.com/jeremymreed/image-file-name-fixer
cd image-file-name-fixer
source venv/bin/activate
python -m image_file_name_fixer <args>
```

To install via pip, and run:  (Not available on PyPI yet.)
```
git clone https://gitlab.com/jeremymreed/image-file-name-fixer
cd image-file-name-fixer
pip install --user .
image-file-name-fixer <args>
```

Examples:
```
# Fixes test_image/test1.jpg, writes output to current working directory.
image-file-name-fixer test_images/test1.jpg
# Fixes test_image/test1.jpg, writes output to fixed_images/
image-file-name-fixer --output fixed_images test_images/test1.jpg
# Fixes test_images/test1.jpg, writes output to test_images/
image-file-name-fixer --in-place test_images/test1.jpg
# Fixes all image files in test_images, writes output to current working directory.
image-file-name-fixer test_images/
# Fixes all image files in test_images/, writes output to fixed_images/
image-file-name-fixer --output fixed_images/ test_images/
# Fixes all image files in test_images/, writes output to test_images/
image-file-name-fixer --in-place test_images/
```

Help message:
```
usage: image-file-name-fixer [-h] [-o OUTPUT_DIR] [--dry-run] [--in-place] [-m] [-v]
                   path

positional arguments:
  path                  path to file or directory to be processed.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        Write output to specified directory. Overrides --in-
                        place
  --dry-run             Run normally, but don't write anything to disk
  --in-place            Write output files in the same directory as the input
                        file.
  -m, --move            Move the file, rather than copying it.
  -v, --verbose         Increase output detail.
```

# License:
This program is licensed under the MIT License.
