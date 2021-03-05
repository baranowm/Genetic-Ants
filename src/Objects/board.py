import pyglet
from pyglet.gl import *
from collections import OrderedDict
from time import time
import pyglet.window.key as key
from ant import Ant, RedAnt, GreenAnt
import numpy as np

### TO DO:
# IMPROVE CHECKING COLISION
class Board(pyglet.window.Window):
    res = {"x": 1000, "y": 1000}

    def __init__(self, iteration=0, *args, **kwargs):
        super(Board, self).__init__(
            width=self.res["x"], height=self.res["y"], *args, **kwargs
        )
        self.alive = 1
        # initialize labels

        self.labels = OrderedDict()
        self.labels["fps_label"] = pyglet.text.Label("0 fps", x=10, y=10)
        self.labels["iteration"] = pyglet.text.Label(
            f"iteration: {iteration}", x=self.width - 100, y=self.height - 50
        )
        # initialize ants
        self.red_ants, self.red_ants_batch = Ant.spawn_batch(
            RedAnt, res=self.res, count=15, name="RED"
        )
        self.green_ants, self.green_ants_batch = Ant.spawn_batch(
            GreenAnt, res=self.res, count=15, name="GREEN"
        )
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

    def update_ants(self):

        for key, red_ant in self.red_ants.items():
            colisions = red_ant.batch_colision_check(
                self.green_ants.values(), self.green_ants.keys()
            )
            red_ant.move()
        for green_ant in self.green_ants.keys():
            colisions = red_ant.batch_colision_check(
                self.green_ants.values(), self.green_ants.keys()
            )
            self.green_ants[green_ant].move()

    def draw_ants(self):
        "draw all sprites"
        self.red_ants_batch.draw()
        self.green_ants_batch.draw()

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
        self.update_ants()
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
