import math
import functools


DIFF_LIMIT = 1e-10

DOTS = [
    (6.333333, 0),
    (4, 0),
    # (2.82842712475, 2.82842712475),
    (0, 4),
    # (-2.82842712475, 2.82842712475),
    (-4, 0),
    (-4, 5),
    (-3, 5),
    (-3, 7),
    (-5, 7),
    (-7, 3),
    (-7, 1),
    (-3, -5),
    (3, -5)
]


TRIANGLE_DOTS = [
    (2, math.sqrt(12) - 2),
    (-2, math.sqrt(12) - 2),
    (0, -2)
]


def with_neighbour(array, last_with_first=True):
    iterator = iter(array)
    first = current = next(iterator)
    is_executed = False
    while True:
        try:
            prev, current = current, next(iterator)
        except StopIteration:
            is_executed = True
            if last_with_first:
                yield current, first
        else:
            yield prev, current
        if is_executed:
            return


def adapt(f):
    @functools.wraps(f)
    def wrapper(dots):
        return f(dots[0][0], dots[0][1], dots[1][0], dots[1][1])
    return wrapper


@adapt
def build_desmos_equation(x1, y1, x2, y2):
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    if abs(x1 - x2) < DIFF_LIMIT:
        template = r"x={x1}\left\{{{y_min}<=y<={y_max}\right\}}"
        return template.format(x1=x1, y_min=y_min, y_max=y_max)
    if abs(y1 - y2) < DIFF_LIMIT:
        template = r"y={y1}\left\{{{x_min}<=x<={x_max}\right\}}"
        return template.format(y1=y1, x_min=x_min, x_max=x_max)
    x_div = x2 - x1
    y_div = y2 - y1
    x_coef = y_div / x_div
    free_coef = (-x1 * y_div) / x_div + y1
    template = r"y={x_coef}*x{free_coef:+f}\left\{{{x_min}<=x<={x_max}\right\}}\left\{{{y_min}<=y<={y_max}\right\}}"
    return template.format(**locals())


if __name__ == "__main__":
    major = {
        "name": "major",
        "dots": [
            {
                "x": dot[0],
                "y": dot[1],
                "connection": {
                    "name": "circle" if i in (1, 2, 7) else "line"
                }
            } for i, dot in enumerate(DOTS)
        ]
    }
    with open("major.json", "w") as file:
        import json
        json.dump([major], file, indent=2)
    # for equation_literal in map(build_equation, with_neighbour(TRIANGLE_DOTS)):
    #     print(equation_literal)
