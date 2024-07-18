import cProfile
import logging
import tkinter
from datetime import datetime
from apps.Optics.classes import game
from apps.Optics.gui import gui_main as gui
import pygame
from apps.Optics import settingsSetup
from apps.Optics.screens import startscreen as ss
import os

# Create a "logs" folder if it doesn't exist
if not os.path.exists("apps/Optics/logs"):
    os.makedirs("apps/Optics/logs")

if not os.path.exists("apps/Optics/saves"):
    os.makedirs("apps/Optics/saves")

if not os.path.exists("apps/Optics/presets"):
    os.makedirs("apps/Optics/presets")

# Set up the logging configuration
log_file = f"apps/Optics/logs/{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


version = '1.0! (Modded)'

def new_game(save, preset):
    try:
        settings = settingsSetup.start()
        width = settings['WIDTH']
        height = settings['HEIGHT']

        position = settings['HOTBAR_POSITION']

        game_instance = game.Game(save, preset)
        GUI = gui.GUI(game_instance)
        game_instance.loop()

        return  game_instance

    except Exception as e:
        # Log any unhandled exceptions
        logging.error(e, exc_info=True)
        raise

def main():
    while 1:
        programIcon = pygame.image.load('apps/Optics/images/torch_icon.png')
        pygame.display.set_icon(programIcon)

            # try:
            #     startscreen = ss.StartScreen(version)
            #     new_game(startscreen.save_to_load, startscreen.preset)
            # except Exception as e:
            #     print(e)
            #     # raise
            #     # logging.error(e, exc_info=True)
            #     # tkinter.messagebox.showerror("Error", "An error occurred. Please check the logs for more information.")
            #     # raise
            #     break

        startscreen = ss.StartScreen(version)

        if startscreen.quit != True:
            a = new_game(startscreen.save_to_load, startscreen.preset)
            if a.quit == True:
                break
        else:
            break

