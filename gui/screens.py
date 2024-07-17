import pygame
from gui import button
from gui import custom_text

class Template:  # A template for all the screens
    def __init__(self, game):
        self.game = game  # Main application
        self.objects = []  # Elements in the screen
        self.screen = self.game.screen  # Getting the screen for easier use

        custom_text.Custom_text(self, 24, self.game.height - 44, None, 32, self.game.version, text_color=(255, 255, 255), center=False)  # Creats text of the version and puts it in the bottom left corner in all of the screens

    def render(self):  # Rendering all objects in the class
        for object in self.objects:
            object.render()

    def events(self, event):  # Checks events for every element in self.objects
        for object in self.objects:
            object.events(event)


class Main_menu(Template):  # The main menu subclass of Template
    def __init__(self, game):
        Template.__init__(self, game)  # Inheriting from Template

        custom_text.Custom_text(self, self.game.width//2, self.game.height//6, None, self.game.height//8, 'G.R.A.P.E.', text_color=(111, 45, 168))

        button.Button(self, 'start', self.game.width//2 - 150, self.game.height//1.3, 300, 100, 'white', 'Start')
        button.Button(self, 'settings', self.game.width // 2 + 160, self.game.height // 1.3, 100, 100, 'white', )

class Settings(Template):  # a future settings menu
    def __init__(self, game):
        Template.__init__(self, game)

        button.Button(self, 'main-menu', self.game.width//2 - 150, self.game.height//1.3, 300, 100, 'white', 'Apply')  # For now a button that takes you back to the main menu

class Selection_screen(Template):  # The screen that actually shows you what apps/scripts you can use
    def __init__(self, game):
        Template.__init__(self, game)

        button.Button(self, 'tetris', 45, 45, 75, 75, 'white', None, 'img/tetris.png')  # A button that starts tetris
        custom_text.Custom_text(self, 82.5, 145, None, 25, 'Tetris', text_color='white')  # A text that says Tetris

        button.Button(self, 'optics', 135, 45, 75, 75, 'white', None, 'img/optics.png')  # A button that starts optics
        custom_text.Custom_text(self, 172.5, 145, None, 25, 'Optics', text_color='white')  # A text that says optics

    def render(self):  # Rendering all objects in the class + additional stuff

        pygame.draw.rect(self.screen, (100, 100, 100), (20, 20, self.game.width-40, self.game.height - 40), border_radius=5)  # the lighter grey background

        for object in self.objects:
            object.render()

