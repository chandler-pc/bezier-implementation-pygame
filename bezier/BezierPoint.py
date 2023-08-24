import pygame

class BezierPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collide = None
        self.color = (0, 0, 0)
        return
    
    def set_color(self, color):
        self.color = color
        return

    def move(self, x, y):
        self.x = x
        self.y = y
        return
    
    def getIsSelecting(self, pos):
        return self.collide.collidepoint(pos) if self.collide != None else False

    def getPos(self):
        return [self.x, self.y]

    def draw(self, screen):
        self.collide = pygame.draw.circle(screen, self.color, (self.x, self.y), 5)
        return