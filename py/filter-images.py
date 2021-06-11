# Apply a filter to all images on a folder

import os
from PIL import Image, ImageFilter

VALID_EXTENSIONS = list(Image.registered_extensions().keys())
VALID_FILTERS = [
    'BLUR',
    'CONTOUR',
    'DETAIL',
    'EDGE_ENHANCE',
    'EDGE_ENHANCE_MORE',
    'EMBOSS',
    'FIND_EDGES',
    'GaussianBlur',
    'SHARPEN',
    'SMOOTH',
    'SMOOTH_MORE',
    'UnsharpMask'
]

# ! Turn this on to enable the debug mode, which will print a line for each image that is being converted. Use this in case it doesn't work and you want to know where exactly it freezes
DEBUG = False


def debug_print(message):
    if DEBUG:
        print(f'\033[90m| {message}\033[0m')


# ? We need the encode part to get the raw string, ignoring all / and \
PATH = input(
    'Please enter the path where the images are located.\n\033[93m>\033[0m ').encode('unicode_escape').decode()

while not os.path.exists(PATH):
    print(
        '\033[91mThe specified path does not exist! Please try again.\n\033[93m>\033[0m ', end='')
    PATH = input()

OUTPUT_FOLDER = os.path.join(PATH, 'filter-output')

# ? Get the input, turn it to lowercase, remove all spaces, separate by comma and add a dot at the beginning
TYPES = input(
    '\nPlease enter all the type of files you want to change, separated by a comma (eg: png,jpeg).\n\033[93m>\033[0m ').lower().replace(' ', '').split(',')

TYPES = ['.' + str(extension) for extension in TYPES]

while not all(item in VALID_EXTENSIONS for item in TYPES):
    print(
        '\033[91mYour input contains invalid extensions! Please try again.\n\033[93m>\033[0m ', end='')
    TYPES = input()

unfiltered_entries = os.listdir(PATH)
valid_images = list()

for entry in unfiltered_entries:
    if entry.endswith(tuple(TYPES)):
        valid_images.append(entry)

if not valid_images:
    print('\033[91mNo valid image was found. Program will exit.\033[0m')
    exit(1)

print('\nPlease enter the filter you want to apply. Available filters:')
for filter_name in VALID_FILTERS:
    print(f'\033[93m  - \033[0m{filter_name}')
FILTER = input('\n\033[93m> \033[0m')

while not FILTER in VALID_FILTERS:
    print(
        '\033[91mThe specified filter does not exist! Make sure it\'s well capitalized and try again.\n\033[93m>\033[0m ', end='')
    FILTER = input()

FILTER_FOLDER = os.path.join(OUTPUT_FOLDER, FILTER)

debug_print('Trying to create filter_output folder...')
if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)
debug_print('filter_output folder exists, proceeding...')

debug_print(f'Trying to create filter_output/{FILTER} folder...')
if not os.path.exists(FILTER_FOLDER):
    os.mkdir(FILTER_FOLDER)
debug_print('filter_output/{FILTER} folder exists, proceeding...')


for originalimg in valid_images:
    debug_print(f'Opening image {originalimg}...')
    image = Image.open(os.path.join(PATH, originalimg)).convert('RGB')
    debug_print(f'Applying filter to {originalimg}...')
    image = image.filter(getattr(ImageFilter, FILTER))
    debug_print(
        f'Saving filtered image {originalimg} to {os.path.join(OUTPUT_FOLDER, originalimg)}...')
    image.save(os.path.join(FILTER_FOLDER, originalimg))
    debug_print('Everything done. Proceeding with next image.\n')

print(f'\033[93mFinished! You can find your images at {FILTER_FOLDER} :)\033[0m')
