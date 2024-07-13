import pygame


class Window:
    def __init__(self, config):
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.fps = int(config['fps'])
        self.version = config['version']

        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption('Grape')  # Set the caption to Grape

        self.clock = pygame.time.Clock()

        self.run = True

        self.mainloop()

    def mainloop(self):
        while self.run:
            self.events()  # Handle events
            self.render()  # Render stuff
            self.update()  # Updates display
            self.clock.tick(self.fps)  # limit fps to self.fps

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if event = quit then stop running the application
                self.run = False

    def render(self):
        self.screen.fill((26, 26, 26))  # fill the screen the with the color

    def update(self):
        pygame.display.update()  # Update the display