import pygame
from pygame import draw
import math
from apps.Optics.classes import game
from apps.Optics.classes import gameobjects
from apps.Optics.classes import gameobjects, fps
from apps.Optics import gui
from apps.Optics.gui.button import *
import time

class polygonDrawing:

    def __init__(self):
        self.currentPolygonPoints = []


    def addPoint(self, mousePos):
        self.currentPolygonPoints.append(mousePos)

        print(self.currentPolygonPoints)
    # def renderDots():
    #     for i in currentPolygonPoints:
    #         pygame.draw.circle(screen, (200, 200, 200), i, 10)
    def clearPoints(self):
        print(12345)
        self.currentPolygonPoints = []
    def createPolygon(self, game):
        print('created')
        if len(self.currentPolygonPoints) >= 3:
            Adam = gameobjects.Mirror(game, self.currentPolygonPoints, (200, 200, 200), 0, 0, 0)
            game.objects.append(Adam)
            self.clearPoints()

    def returnPolygonPoints(self):
        return self.currentPolygonPoints

    def popapoint(self):
        self.currentPolygonPoints.pop()

