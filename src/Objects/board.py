import pyglet
from pyglet.gl import *
from collections import OrderedDict
from time import time
import pyglet.window.key as key
from ant import Ant
import numpy as np
ant_img = pyglet.image.load("..\\sprites\\ant.png")
class Board(pyglet.window.Window):
    def __init__(self, iteration=0, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.alive = 1
        # initialize labels

        self.labels = OrderedDict()
        self.labels["fps_label"] = pyglet.text.Label("0 fps", x=10, y=10)
        self.labels["iteration"] = pyglet.text.Label(
            f"iteration: {iteration}", x=self.width - 100, y=self.height - 50
        )
        # initialize ants
        self.ants = OrderedDict()
        self.ants["ant1"] = Ant(ant_img, x=100, y=100)
        self.ants["ant2"] = Ant(ant_img, x=200, y=200)
        # For FPS calculation
        self.last_update = time()
        self.fps_count = 0

    def count_fps(self):
        "count fps (ticks/second)"
        self.fps_count += 1
        if time() - self.last_update > 1:  # 1 sec passed
            self.labels["fps_label"].text = str(self.fps_count)
            self.fps_count = 0
            self.last_update = time()
        else:
            pass

    def draw_labels(self):
        "draw all labels"
        for label in self.labels:
            self.labels[label].draw()

    def draw_ants(self):
        "draw all sprites"
        for ant in self.ants:
            self.ants[ant].move()
            self.ants[ant].draw()

    def on_draw(self):
        self.render()

    def on_key_press(self, symbol, modifiers):
        "on escape exit"
        if symbol == key.ESCAPE:  # [ESC]
            self.alive = 0

    def pre_render(self):
        pass

    def render(self):
        self.clear()

        # FPS stuff (if you want to)
        self.count_fps()

        self.pre_render()

        self.draw_ants()
        self.draw_labels()

        self.flip()

    def run(self):
        while self.alive == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()


if __name__ == "__main__":
    board = Board()
    board.run()
