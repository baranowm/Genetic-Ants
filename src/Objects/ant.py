import pyglet
import numpy as np


class Ant(pyglet.sprite.Sprite):
    scale = 0.5

    def __init__(self, img, x, y, *args, **kwargs):
        img = self._scale_img(img, self.scale)
        super(Ant, self).__init__(img, x, y, *args, **kwargs)
        self.x = x
        self.y = y
        self.rotation = 0

    def move(self):
        self.x += 1
        self.y += 1
        self.rotation += 0.1
        self.update(self.x, self.y, self.rotation)

    @staticmethod
    def _scale_img(img, scale):
        "scale img to desired res"
        img.scale = scale, scale
        texture = img.get_texture()
        img.width = int(scale * img.width)
        img.height = int(scale * img.height)
        texture.width = int(scale * img.width)
        texture.height = int(scale * img.height)
        return img

    def _colision_pre_check(self, other):
        "returns true if on x or y axis the dist > view_distance"
        return min(abs(self.x - other.x), abs(self.y - other.y)) > min(
            self.view_dist, other.view_dist
        )

    def check_colision(self, other):
        dist_simplified = min(abs(self.x - other.x), abs(self.y - other.y))
        visible_range, colision = False, False
        if self._colision_pre_check(other):
            # False, False
            visible_range, colision = False, False
        else:
            visible_range = True
            if dist_simplified < (self.img.width / 2 + other.img.width / 2) ** 2:
                colision = True
            else:
                colision = False

        return visible_range, colision

    @staticmethod
    def spawn_batch(ant_class, res, count, name=""):
        batch = pyglet.graphics.Batch()

        sprites = {
            f"name_{i}": ant_class(x, y, batch=batch)
            for i, (x, y) in enumerate(
                zip(
                    np.random.randint(low=0, high=res["x"], size=count),
                    np.random.randint(low=0, high=res["y"], size=count),
                )
            )
        }
        return sprites, batch


class RedAnt(Ant):
    sprite_location = ".\\sprites\\red_ant.png"
    view_dist = 30

    def __init__(self, x, y, *args, **kwargs):
        self.img = pyglet.image.load(self.sprite_location)
        self.name = "RED"
        super(self.__class__, self).__init__(self.img, x, y, *args, **kwargs)


class GreenAnt(Ant):
    sprite_location = ".\\sprites\\green_ant.png"
    view_dist = 30

    def __init__(self, x, y, *args, **kwargs):
        self.img = pyglet.image.load(self.sprite_location)
        self.name = "GREEN"
        super(self.__class__, self).__init__(self.img, x, y, *args, **kwargs)
