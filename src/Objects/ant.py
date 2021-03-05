"class for Ant objects"
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
        self.col_radius = self.img.width / 2

    def move(self, input_m=[1, 1]):

        self.rotation += input_m[0]
        self.x += int(np.sin(np.deg2rad(self.rotation)) * self.max_speed * input_m[1])
        self.y += int(np.cos(np.deg2rad(self.rotation)) * self.max_speed * input_m[1])
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

    def batch_colision_check(self, others, others_names):
        other_m = np.asmatrix([[other.x, other.y, other.rotation] for other in others])
        self_m = np.zeros(other_m.shape) + np.asmatrix([self.x, self.y, self.rotation])
        dist_m = np.linalg.norm(other_m[:, :2] - self_m[:, :2], axis=1)

        vis = np.zeros(self_m[:, :2].shape)
        vis[:, 0] = dist_m < self.view_dist
        vis[:, 1] = dist_m < self.col_radius

        return vis

    @staticmethod
    def spawn_batch(ant_class, res, count, name=""):
        batch = pyglet.graphics.Batch()

        sprites = {
            f"{name}_{i}": ant_class(x, y, batch=batch)
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
    max_speed = 3
    view_dist = 30

    def __init__(self, x, y, *args, **kwargs):
        self.img = pyglet.image.load(self.sprite_location)
        self.name = "RED"
        super(self.__class__, self).__init__(self.img, x, y, *args, **kwargs)


class GreenAnt(Ant):
    sprite_location = ".\\sprites\\green_ant.png"
    view_dist = 30
    max_speed = 3

    def __init__(self, x, y, *args, **kwargs):
        self.img = pyglet.image.load(self.sprite_location)
        self.name = "GREEN"
        super(self.__class__, self).__init__(self.img, x, y, *args, **kwargs)
