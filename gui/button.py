import pygame
from gui import custom_text, custom_images
class Button:  # A button class
    def __init__(self, template, action, x, y, width, height, color, text=None, image=None):  # Getting all the parameters of the button

        self.action = action

        self.template = template

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Creating a rect object

        self.template.objects.append(self)  # Adding self to objects of the screen

        if text != None:  # if there is text it's put on the button
            custom_text.Custom_text(self.template, self.x + self.width // 2, self.y + self.height // 2, None,
                                    self.height // 2, text)

        elif image != None:  # if text == None and image != None -> renders an image in the center of the button
            self.image = custom_images.Custom_image(self.template, image, self.x + 5, self.y + 5, self.width - 10, self.height - 10)


    def render(self):  # Rendering a button on screen
        pygame.draw.rect(self.template.screen, self.color, self.rect, border_radius=10)


    def events(self, event):  # Checks events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):  # Checks if the button has been pressed
            if self.action == 'settings':
                self.template.game.current_screen = self.template.game.screens['Settings']

            elif self.action == 'main-menu':
                self.template.game.current_screen = self.template.game.screens['Main menu']

            elif self.action == 'start':
                self.template.game.current_screen = self.template.game.screens['Selection screen']

            elif self.action == 'tetris':  # Imports tetris, runs it, when it finishes it rescales the window
                from apps.Tetris import main
                main.main()
                self.template.game.screen_setup()

            elif self.action == 'optics':
                print("Optics")
