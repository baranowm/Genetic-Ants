import pyglet
import numpy as np
class Ant(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, *args, **kwargs):
        super(Ant, self).__init__(img, x, y, *args, **kwargs)
        self.x = x
        self.y = y
        self.rotation = 0 

    def move(self):
        self.x += 1
        self.y += 1
        self.rotation += 0.1
        self.update(self.x, self.y, self.rotation)
