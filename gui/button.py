import pygame

class Button:  # A button class
    def __init__(self, number, template, x, y, width, height, color):  # Getting all the parameters of the button

        self.number = number

        self.template = template

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Creating a rect object

        self.template.objects.append(self)  # Adding self to objects of the screen

    def render(self):  # Rendering a button on screen
        pygame.draw.rect(self.template.screen, self.color, self.rect, border_radius=10)

    def events(self, event):  # Checks events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):  # Checks if the button has been pressed
            print('clicked')
