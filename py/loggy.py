r"""
Loggy Module Usage

First change the MAIN color using the set_type() function (because nobody likes using default values).
You can use either a HEX string or a RGB tuple.
    - Loggy.set_type('MAIN', '#f72585')
    - Loggy.set_type('MAIN', '94d2bd')
    - Loggy.set_type('MAIN', my_main_rgb_tuple)

You can then proceed using the log() function to log messages to the console.
    - Loggy.log('Hello world!')
    - Loggy.log('A really bad thing happened!', type = 'ERROR')
    - Loggy.log('Some debug info.', type = 'DEBUG')

You can also change the color of any type using the set_type() function (or even add your own types).
    - Loggy.set_type('DEBUG', '#f1faee')      # Ew, white debug text.
    - Loggy.set_type('WARNING', '#560bad')    # I like my warnings purple.
    - Loggy.set_type('my_beloved_custom_type', '#94d2bd')

Additionally, you can specify certain text arguments when logging information.
    - Loggy.log('This text will really stand out.', type = 'MAIN', format_args = {'bold': True, 'underline': True})
    - Loggy.log('I don't want to use a prefix on this one.', format_args = {'prefix': False})
Valid arguments: prefix, separator, bold, italic, underline, strike.

If you ever need to color just a few words and make them stand out, use the colorize() function.
    - Loggy.colorize('I will return a yellow, bold string', '#ee9b00', format_args = {'bold' = True})
    - Loggy.colorize('I will return a white striked string instead.', 'FFFFFF', format_args = {'strike' = True})

You can also set the dump_file boolean to True to dump whatever you log to a .log file, saved on your working directory.
This file will obviously not contain any colors, but it will contain timestamps.
    - Loggy.dump_file = True      # Whatever you log will now be saved on a .log file.

"""


import os
import __main__
import time
import re
if os.name == 'nt':
    os.system('')

dump_file = True
LOG_FILE_NAME = __main__.__file__.split('.', 1)[0]+'.log'
REMOVE_COLOR_REGEX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

DEFAULT_COLOR = '#0077b6'  # ? I'm blue daba dee dabba daee
SEPARATOR = '|'

ANSI_COLOR_REGEX = re.compile(r'(?<=\033\[38;2;)(.*?)(?=m)')


def hex_rgb(hexc):
    r"""This function converts HEX values to RGB. This is meant for internal usage only.
    If you pass a tuple to it, it'll just return it back, assuming it's already an RGB tuple.

    📒 Args:
        hexc (str): Your HEX value goes here (eg. #FFFFFF).

    📤 Returns:    
        tuple: Containing the RGB values.

    💡 Example:
        Input:  Loggy.hex_rgb('#e9c46a')
        Output: ("233","196","106")

    """
    if type(hexc) == tuple:
        return hexc
    hexc = hexc.lstrip('#')
    return tuple(int(hexc[i:i+2], 16) for i in (0, 2, 4))


def ansi_tuple(ansic):
    r"""This function converts ANSI color values to an RGB tuple. This is meant for internal usage only.
    
    📒 Args:
        hexc (str): Your ansi color value goes here (eg. \033[38;2;255;255;255m).

    📤 Returns:    
        tuple: Containing the RGB values.

    💡 Example:
        Input:  Loggy.ansi_tuple('\033[38;2;233;196;106m')
        Output: ("233","196","106")
    """
    
    ansi_regex_match = re.findall(ANSI_COLOR_REGEX, ansic)[0]
    rgbc = tuple(ansi_regex_match.split(";"))
    return rgbc


def format_color(convert_color, format_args={'bold': False, 'italic': False, 'underline': False, 'strike': False}):
    r"""This function formats a HEX string / RGB tuple to a valid ANSI color code, using the format_args you specified.

    📒 Args:
        convert_color (str [HEX] || tuple [RGB]): Specify the color to convert here.
        format_args (dict, optional): The arguments you want to pass, like bold, italic, etc. Defaults to {'bold': False, 'italic': False, 'underline': False, 'strike': False}.

    📤 Returns:
        str: Which contains the equivalent ANSI color code.

    💡 Example:
        Input:  Loggy.format_color('#dc2f02', format_args={'bold': True, 'underline': True})
        Output: '\033[38;2;220;47;2;1;4m'
    """
    
    converted_rgb = hex_rgb(convert_color)
    ANSI_COLOR_BASE = f'\033[38;2;{converted_rgb[0]};{converted_rgb[1]};{converted_rgb[2]}'
    FORMAT_VALUES = {'bold': '1', 'italic': '3',
                     'underline': '4', 'strike': '9'}
    formatted_color = ANSI_COLOR_BASE
    for user_arg in format_args:
        if(format_args.get(user_arg)):
            formatted_color += f';{FORMAT_VALUES.get(user_arg)}'
    formatted_color += f'm'
    return formatted_color


# ? For reference: https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# * All the colors in this dictionary are changeable using the set_type function.
colors = {
    "NONE": "\033[38;2;255;255;255m",
    "DEBUG": "\033[38;2;88;88;88m",
    "WARNING": "\033[38;2;252;163;17m",
    "ERROR": "\033[38;2;230;57;70m",
    "ENDC": "\033[0m"
}


def set_type(name, type_color):
    r"""A function to help you modify existing types or add your own type.

    📒 Args:
        name (str): The name of the type to modify or add.
        type_color (str [HEX] || tuple [RGB]): The color that will be assigned to the log type.
    
    💡 Usage example:
        - Loggy.set_type('newtype', '#264653')
        - Loggy.log('This will be formatted with the #264653 color', type= 'newtype')
    """
    converted_rgb = hex_rgb(type_color)
    colors[name.upper()] = f'\033[38;2;{converted_rgb[0]};{converted_rgb[1]};{converted_rgb[2]}m'


def colorize(string, color, format_args={'bold': False, 'italic': False, 'underline': False, 'strike': False}):
    r"""A function to color and format a string, using the arguments given.

    📒 Args:
        message (str): The string to format.
        color (str [HEX] || tuple [RGB]): Specify the color to use when colorizing this string.
        format_args (dict, optional): Specify extra arguments to format the string. Defaults to {'bold': False, 'italic': False, 'underline': False, 'strike': False}.

    📤 Returns:
        str: Which contains the string, alonside its specific ANSI color code.
    
    💡 Example:
        Input:  Loggy.colorize('I want this to look red and bold', '#d62828', format_args= {'bold': True})
        Output: "\033[38;2;214;40;40;1mI want this to look red and bold\033[0m"
    """
    return f'{format_color(color, format_args)}{string}{colors.get("ENDC")}'


def dump_log(print_message):
    r"""A function to dump a message to a file, if dump_file == True.

    📒 Args:
        print_message (str): Specify the message to dump.

    💡 Usage example:
        - Loggy.dump_log('This will be dumped to a file, if dump_file == True')

    """
    if(dump_file):
        currenttime = time.strftime("[%H:%M:%S] ")
        with open(LOG_FILE_NAME, 'a') as file:
            file.write(currenttime + print_message + '\n')


def log(message, type="MAIN", format_args={'prefix': True, 'bold': False, 'italic': False, 'underline': False, 'strike': False}):
    r"""A function to log a message. This is the module's main function.

    📒 Args:
        message (str): Whatever you want to log.
        type (str, optional): Specify the type of message, like an ERROR or WARNING (grabbed from colors dictionary, case insensitive). Defaults to "MAIN". 
        args (dict, optional): The custom arguments to use when logging. Defaults to {'prefix': True, 'bold': False, 'italic': False, 'underline': False, 'strike': False}.
    
    💡 Usage example:
        - Loggy.log('Some message')
        - Loggy.log('An error happened.', type="ERROR")
    """
    type = type.upper()
    if colors.get(type) is None:
        raise ValueError("Invalid log type.")

    print_message = ''
    print_message += f'{colors.get(type)}'
    ansi_format_args = format_args
    if format_args.get('prefix') == None or format_args['prefix']:
        format_args['prefix'] = True
        print_message += f'{type.upper()} '
        del ansi_format_args['prefix']

    print_message += f'{SEPARATOR} {format_color(ansi_tuple(colors.get(type)), ansi_format_args)}{message}'

    print(f'{print_message}{colors.get("ENDC")}')
    dump_log(REMOVE_COLOR_REGEX.sub('', print_message))

set_type('MAIN', DEFAULT_COLOR)