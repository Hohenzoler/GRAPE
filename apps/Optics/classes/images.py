import pygame  # Importing the pygame module
from apps.Optics import imgtocode  # Importing the imgtocode module
import os  # Importing the os module


imgtocode.generateImages()  # Generating images if the directory does not exist

# Loading various images using the pygame module
torch_icon = pygame.image.load("apps/Optics/images/torch_icon.png")  # Loading the torch icon image
object_icon = pygame.image.load("apps/Optics/images/lustro.png")  # Loading the object icon image
prism_icon = pygame.image.load("apps/Optics/images/Prism.png")  # Loading the prism icon image
settings_icon = pygame.image.load('apps/Optics/images/settings.png')  # Loading the settings icon image
exit_icon = pygame.image.load('apps/Optics/images/exit.png')  # Loading the exit icon image
torch = pygame.image.load('apps/Optics/images/torch.png')  # Loading the torch image
laser = pygame.image.load('apps/Optics/images/black_rectangle.png')  # Loading the laser image
bin = pygame.image.load('apps/Optics/images/trash.png')  # Loading the bin image
bad_coursor = pygame.image.load('apps/Optics/images/bad_coursor.png')  # Loading the bad cursor image
topopisy = pygame.image.load('apps/Optics/images/bad_pen.png')  # Loading the topopisy image
pen = pygame.image.load('apps/Optics/images/pen.png')  # Loading the pen image
# water = pygame.image.load('images/materials/water.png')  # Loading the water image
# clouds = pygame.image.load('images/materials/clouds.png')  # Loading the clouds image
# wood = pygame.image.load('images/materials/wood.png')  # Loading the wood image
# glass = pygame.image.load('images/materials/glass.png')  # Loading the glass image
# papier = pygame.image.load('images/materials/paper.png')  # Loading the paper image
lens = pygame.image.load('apps/Optics/images/glasses.png')  # Loading the lens image
glass_icon = pygame.image.load("apps/Optics/images/glass_thing_icon.png")  # Loading the glass icon image
concave = pygame.image.load("apps/Optics/images/concave.png")  # Loading the concave icon image
oneconcave = pygame.image.load("apps/Optics/images/oneconcave.png")  # Loading the one concave icon image
oneconvex = pygame.image.load("apps/Optics/images/oneconvex.png")  # Loading the oneconvex icon image
puchar = pygame.image.load("apps/Optics/images/upo_puchar.png")
corridor = pygame.image.load("apps/Optics/images/idk.png")
corridor_icon = pygame.image.load("apps/Optics/images/corridor_icon.png")
