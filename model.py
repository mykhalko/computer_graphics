import math
import json
from contextlib import contextmanager
from copy import deepcopy

from tools import split_arc
from tools import move_point
from tools import multiple_point
from tools import rotate_point


class Connections:
    LINE = "line"
    CIRCLE = "circle"


class Outline:

    def __init__(self, data, adapter=None):
        self._scale_name = data["scale"]["name"]
        self._name = data["name"]
        self._center = data["center"]
        self._scale = data["scale"]["value"]
        self._initial_dots = data["dots"]
        self._dots = self._initial_dots
        self._adapter = adapter

    @property
    def dots(self):
        return self._dots or self._initial_dots

    @contextmanager
    def transformation(self, data):
        rotation = data["rotation"]
        rotation_angle = rotation * math.pi / 180
        vertical_move = data["vertical_move"]
        horizontal_move = data["horizontal_move"]
        scale = data[self._scale_name]
        dots = deepcopy(self._initial_dots)
        for dot in dots:
            self.transform_dot(dot, rotation_angle, scale, horizontal_move, vertical_move)
            if dot["connection"]["name"] == Connections.CIRCLE:
                self.transform_dot(dot["connection"]["center"], rotation_angle, scale, horizontal_move, vertical_move)
        self._dots = dots
        yield
        self._dots = None

    def transform_dot(self, dot, rotation_angle, scale, horizontal_move, vertical_move):
        center_x = self._center["x"]
        center_y = self._center["y"]
        dot["x"], dot["y"] = rotate_point(
            dot["x"],
            dot["y"],
            center_x,
            center_y,
            rotation_angle
        )
        dot["x"], dot["y"] = multiple_point(
            dot["x"],
            dot["y"],
            center_x,
            center_y,
            scale / self._scale
        )
        dot["x"], dot["y"] = move_point(
            dot["x"],
            dot["y"],
            horizontal_move,
            vertical_move
        )

    def __iter__(self):
        cartesian_dots = []
        for i, dot in enumerate(self.dots):
            if dot["connection"]["name"] == Connections.LINE:
                cartesian_dots.append((dot["x"], dot["y"]))
            elif dot["connection"]["name"] == Connections.CIRCLE:
                try:
                    next_dot = self.dots[i + 1]
                except IndexError:
                    next_dot = self.dots[0]
                dots_extension = split_arc(
                    dot["x"],
                    dot["y"],
                    next_dot["x"],
                    next_dot["y"],
                    dot["connection"]["center"]["x"],
                    dot["connection"]["center"]["y"]
                )[:-1]
                cartesian_dots.extend(dots_extension)
        return map(self._adapter, cartesian_dots) if self._adapter else iter(cartesian_dots)


class Model:
    def __init__(self, path, adapter):
        with open(path) as file:
            self._outlines = [Outline(i, adapter=adapter) for i in json.load(file)]

    @property
    def outlines(self):
        return self._outlines

    @contextmanager
    def transformation(self, data):
        context_managers = [outline.transformation(data) for outline in self._outlines]
        for cm in context_managers:
            cm.__enter__()
        yield
        for cm in context_managers:
            cm.__exit__(None, None, None)
