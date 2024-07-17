import pygame
from gui import screens


class Window:
    def __init__(self, config):
        pygame.init()

        self.config = config

        self.screen_setup()  # Setting the parameters of the screen

        self.clock = pygame.time.Clock()

        self.run = True

        self.screens = {'Main menu': screens.Main_menu(self), 'Settings': screens.Settings(self), 'Selection screen': screens.Selection_screen(self)}  # a dict with all screens

        self.current_screen = self.screens['Main menu']  # Setting current screen from screens.py file

        self.mainloop()

    def mainloop(self):
        while self.run:
            self.events()  # Handle events
            self.render()  # Render stuff
            self.update()  # Updates display
            self.clock.tick(self.fps)  # limit fps to self.fps

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if event == quit -> stop running the application
                self.run = False
            else:
                self.current_screen.events(event)  # If event != quit -> check events in self.current_screen

    def render(self):
        self.screen.fill((26, 26, 26))  # fill the screen the with the color

        self.current_screen.render()  # Rendering the current screen

    def update(self):
        pygame.display.update()  # Update the display

    def screen_setup(self):  # Setting the parameters of the screen
        self.width = int(self.config['width'])
        self.height = int(self.config['height'])
        self.fps = int(self.config['fps'])
        self.version = self.config['version']

        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption('Grape')  # Set the caption to Grape