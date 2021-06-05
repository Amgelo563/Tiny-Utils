# Change all mp4 videos on a folder to mp3
# ! Keep in mind that all mp3s will be saved in the same folder you executed this script. I recommend using it on the same folder where your mp4 files are located

import os
import moviepy.editor as mpedit

# ! Turn this on to enable the debug mode, which will print a line for each video that is being converted. Use this in case it doesn't work and you want to know where exactly it freezes
DEBUG = True


def debug_print(message):
    if DEBUG:
        print(f'\033[90m| {message}\033[0m')


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

# ? We need the encode part to get the raw string, ignoring all / and \
PATH = input(
    'Please enter the path where the videos are located.\n\033[36m>\033[0m ').encode('unicode_escape').decode()

while not os.path.exists(PATH):
    print(
        '\033[91mThe specified path does not exist! Please try again.\n\033[36m>\033[0m ', end='')
    PATH = input()

unfiltered_entries = os.listdir(PATH)
valid_mp4s = list()

for entry in unfiltered_entries:
    if entry.endswith('.mp4'):
        valid_mp4s.append(entry)


for originalmp4 in valid_mp4s:
    mp3_name = originalmp4.replace('.mp4', '.mp3')
    mp3_path = os.path.join(PATH, mp3_name)

    debug_print(f'Opening mp4 {originalmp4}...')
    mp4_file = mpedit.VideoFileClip(os.path.join(PATH, originalmp4))
    debug_print(f'Saving mp3 as {mp3_name}...')
    mp4_file.audio.write_audiofile(mp3_name, verbose=DEBUG)
    debug_print('Everything done. Proceeding with next video.\n')

print(f'\033[91mFinished! You can find your audios at {WORKING_DIR} :)\033[0m')
