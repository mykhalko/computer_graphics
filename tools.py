import math


DIFF_LIMIT = 1e-10


def rotate_point(point_x, point_y, origin_x, origin_y, alpha):
    sin = math.sin(alpha)
    cos = math.cos(alpha)
    x_rotated = (point_x * cos) - (point_y * sin) - (origin_x * (cos - 1)) + (origin_y * sin)
    y_rotated = (point_x * sin) + (point_y * cos) - (origin_y * (cos - 1)) - (origin_x * sin)
    return x_rotated, y_rotated


def multiple_point(point_x, point_y, origin_x, origin_y, multiplier):
    point_x, point_y = point_x - origin_x, point_y - origin_y
    point_x, point_y = point_x * multiplier, point_y * multiplier
    point_x, point_y = point_x + origin_x, point_y + origin_y
    return point_x, point_y


def move_point(point_x, point_y, shift_x, shift_y):
    return point_x + shift_x, point_y + shift_y


def relation(center_x, center_y):
    return lambda x, y: (x - center_x, y - center_y)


def reverse_relation(center_x, center_y):
    return lambda x, y: (x + center_x, y + center_y)


def get_angle(x, y):
    extra = 0
    if abs(x) < DIFF_LIMIT:
        angle = math.pi / 2
        if y < 0:
            extra = math.pi
        return angle + extra
    angle = math.atan(y / x)
    extra = 0
    if x > 0:
        if y < 0:
            extra = 2 * math.pi
    elif x < 0:
        extra = math.pi
    return angle + extra


def split_arc(start_x, start_y, end_x, end_y, center_x, center_y, split_count=100):
    radius = math.sqrt((start_x - center_x)**2 + (start_y - center_y)**2)
    print(f"radius: {radius}")
    relative = relation(center_x, center_y)
    reverse_relative = reverse_relation(center_x, center_y)
    start_angle = get_angle(*relative(start_x, start_y))
    end_angle = get_angle(*relative(end_x, end_y))
    portion = (end_angle - start_angle) / split_count
    points_angles = [start_angle + i * portion for i in range(split_count)]
    points_angles.append(end_angle)
    cartesian_coordinates = [
        reverse_relative(radius * math.cos(alpha), radius * math.sin(alpha))
        for alpha in points_angles
    ]
    return cartesian_coordinates


def coordinates_adapter(real_size, virtual_size):
    virtual_cell_size = round(real_size / virtual_size / 2)
    shift_value = round(real_size / 2)

    def adapter(point):
        x = point[0]
        y = point[1]
        real_x = round(x * virtual_cell_size + shift_value)
        real_y = round((real_size - shift_value) - y * virtual_cell_size)
        return real_x, real_y
    return adapter
