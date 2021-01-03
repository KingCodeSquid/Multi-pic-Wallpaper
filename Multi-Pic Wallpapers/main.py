import ctypes
import json
import os
import time
import random

# Config
config_file = open("config.json")
config = json.load(config_file)

PATH = config["PATH"]

# Get amount of pictures in folder

for file in os.listdir(PATH):
    if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
        amountOfPictures = len(file)

# Check if shuffled or in order
# Is not shuffled

if config["shuffledOrder"] == 0 or config["shuffledOrder"] == "no":

    pic = 0

    while True:
        pic += 1

        if pic > amountOfPictures:
            pic = 1

        ctypes.windll.user32.SystemParametersInfoW(config["SPI_SET_WALLPAPER"], 0, f"{PATH}\\{pic}.jpg", 0)
        time.sleep(config["secondsUntilChange"])

# Is shuffled

elif config["shuffledOrder"] == 1 or config["shuffledOrder"] == "yes":

    # previouslyDone = []
    done_files = set()
    amount_check = 0
    file_count = os.listdir(PATH)
    skipPass = 0

    while True:
        for file in os.listdir(PATH):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):

                if skipPass == 1 or skipPass == 2:
                    if skipPass != 2:
                        choice_files = list(done_files)
                        skipPass = 2

                    random_file = random.choice(choice_files)

                    if random_file in done_files:
                        choice_files.remove(random_file)

                    done_files.add(random_file)

                    ctypes.windll.user32.SystemParametersInfoW(config["SPI_SET_WALLPAPER"], 0,
                                                               f"{PATH}\\{random_file}",
                                                               0)
                    time.sleep(config["secondsUntilChange"])

                    if len(choice_files) == 0:
                        choice_files = list(done_files)

                    break

                if file in done_files:
                    break

                amount_check += 1

                done_files.add(file)

                if amount_check == len(file_count):

                    skipPass = 1

                    choice_files = list(done_files)
                    random_file = random.choice(choice_files)

                    if random_file in done_files:
                        break

                    done_files.add(random_file)

                    ctypes.windll.user32.SystemParametersInfoW(config["SPI_SET_WALLPAPER"], 0, f"{PATH}\\{random_file}",
                                                               0)
                    time.sleep(config["secondsUntilChange"])

# Error reading config

else:
    print("Invalid value in config.json. \"shuffledOrder\" can only be set to 0 or 1.")
