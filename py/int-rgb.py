# Int to RGB

RGBint = int(input('Please enter the color int.\n\033[93m>\033[0m '))

red_value =   (RGBint >> 16) & 255
green_value = (RGBint >> 8) & 255
blue_value =  RGBint & 255
hex_value = '%02x%02x%02x' % (red_value, green_value, blue_value)

print(f"""
\033[91mRed:\033[0m {red_value}
\033[92mGreen:\033[0m {green_value}
\033[94mBlue:\033[0m {blue_value}

\033[93mRGB:\033[0m {red_value} {green_value} {blue_value}
\033[93mHex:\033[0m #{hex_value}

\033[36mMore data: \033[0m\033[4mhttps://www.colorhexa.com/{hex_value}\033[0m

\033[38;2;{red_value};{green_value};{blue_value}mThis is your color!: \033[48;2;{red_value};{green_value};{blue_value}m       \033[0m
""")