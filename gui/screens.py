import pygame
from gui import button
from gui import custom_text

class Template:  # A template for all the screens
    def __init__(self, game):
        self.game = game  # Main application
        self.objects = []  # Elements in the screen
        self.screen = self.game.screen  # Getting the screen for easier use

    def render(self):  # Rendering all objects in the class
        for object in self.objects:
            object.render()

    def events(self, event):  # Checks events for every element in self.objects
        for object in self.objects:
            object.events(event)


class Main_menu(Template):  # The main menu subclass of Template
    def __init__(self, game):
        Template.__init__(self, game)  # Inheriting from Template
