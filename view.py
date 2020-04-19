from contextlib import contextmanager

from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton
)
from PyQt5.QtGui import (
    QPixmap,
    QColor,
    QPainter,
)
from PyQt5.QtCore import Qt

from legacy_tools import with_neighbour


class GenericCanvas(QLabel):
    _default_size = 700
    _default_virtual_size = 10
    _default_pen_width = 1

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._size = kwargs.get("size", self._default_size)
        self._virtual_size = kwargs.get("virtual_size", self._default_virtual_size)
        self._default_pen_width = kwargs.get("default_pen_width", self._default_pen_width)
        self._init_ui()

    def _init_ui(self):
        pixmap = QPixmap(self._size, self._size)
        self.setPixmap(pixmap)
        self.clear()
        self._default_pen_color = QColor('#ff0000')
        self.paint_cartesian()
        self.show()

    @contextmanager
    def painting(self, width=None, color=None):
        painter = QPainter(self.pixmap())
        pen = painter.pen()
        pen.setWidth(width or self._default_pen_width)
        pen.setColor(color or self._default_pen_color)
        painter.setPen(pen)
        yield painter
        painter.end()
        self.update()

    def paint_line(self):
        with self.painting(width=1) as painter:
            painter.drawLine(0, 0, 499, 499)

    def paint_cartesian(self):
        safe_size = self._size - 1
        virtual_cell_size = round(safe_size / self._virtual_size / 2)
        splitters = tuple(range(0, safe_size, virtual_cell_size))
        splitters_count = len(splitters)
        for i, splitter in enumerate(splitters):
            if i == splitters_count // 2:
                color = QColor(0, 0, 0, 255)
            else:
                color = QColor(0, 0, 0, 25)
            with self.painting(color=color) as painter:
                painter.drawLine(splitter, 0, splitter, safe_size)
                painter.drawLine(0, splitter, safe_size, splitter)

    def clear(self):
        self.pixmap().fill(Qt.white)

    def draw_outline(self, points):
        with self.painting(color=QColor(255, 0, 0, 255)) as painter:
            for start, end in with_neighbour(points):
                painter.drawLine(start[0], start[1], end[0], end[1])
                print(f"drawing line for {(start[0], start[1], end[0], end[1])}")


class ControlPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.super_on_redraw = kwargs["on_redraw"]
        self.super_on_athens_transformation = kwargs["on_athens_transformation"]
        self.super_on_projective_transformation = kwargs["on_projective_transformation"]

        # major radius
        self.major_radius_widget = QWidget(self)
        major_radius_row_layout = QHBoxLayout(self.major_radius_widget)
        self.major_radius_label = QLabel(self.major_radius_widget)
        self.major_radius_label.setText("Major radius:")
        self.major_radius_line_edit = QLineEdit(self.major_radius_widget)
        major_radius_row_layout.addWidget(self.major_radius_label)
        major_radius_row_layout.addWidget(self.major_radius_line_edit)
        self.layout.addWidget(self.major_radius_widget)

        # triangle sid
        self.triangle_side_widget = QWidget(self)
        triangle_side_row_layout = QHBoxLayout(self.triangle_side_widget)
        self.triangle_side_label = QLabel(self.triangle_side_widget)
        self.triangle_side_label.setText("Triangle side:")
        self.triangle_side_line_edit = QLineEdit(self.triangle_side_widget)
        triangle_side_row_layout.addWidget(self.triangle_side_label)
        triangle_side_row_layout.addWidget(self.triangle_side_line_edit)
        self.layout.addWidget(self.triangle_side_widget)

        # horizontal move
        self.horizontal_move_widget = QWidget(self)
        horizontal_move_row_layout = QHBoxLayout(self.horizontal_move_widget)
        self.horizontal_move_label = QLabel(self.horizontal_move_widget)
        self.horizontal_move_label.setText("Move ⇄:")
        self.horizontal_move_line_edit = QLineEdit(self.horizontal_move_widget)
        horizontal_move_row_layout.addWidget(self.horizontal_move_label)
        horizontal_move_row_layout.addWidget(self.horizontal_move_line_edit)
        self.layout.addWidget(self.horizontal_move_widget)

        # vertical move
        self.vertical_move_widget = QWidget(self)
        vertical_move_row_layout = QHBoxLayout(self.vertical_move_widget)
        self.vertical_move_label = QLabel(self.vertical_move_widget)
        self.vertical_move_label.setText("Move ⇅:")
        self.vertical_move_line_edit = QLineEdit(self.vertical_move_widget)
        vertical_move_row_layout.addWidget(self.vertical_move_label)
        vertical_move_row_layout.addWidget(self.vertical_move_line_edit)
        self.layout.addWidget(self.vertical_move_widget)

        # rotation
        self.rotation_widget = QWidget(self)
        rotation_row_layout = QHBoxLayout(self.rotation_widget)
        self.rotation_label = QLabel(self.rotation_widget)
        self.rotation_label.setText("Rotate ⥀ (degrees):")
        self.rotation_line_edit = QLineEdit(self.rotation_widget)
        rotation_row_layout.addWidget(self.rotation_label)
        rotation_row_layout.addWidget(self.rotation_line_edit)
        self.layout.addWidget(self.rotation_widget)

        # redraw button
        self.redraw_button = QPushButton()
        self.redraw_button.setText("redraw")
        self.redraw_button.clicked.connect(self.redraw_trigger)
        self.layout.addWidget(self.redraw_button)

        # X0 Y0
        self.xyyy_widget = QWidget(self)
        xyyy_row_layout = QHBoxLayout(self.xyyy_widget)
        self.x0_label = QLabel(self.xyyy_widget)
        self.x0_label.setText("X0: :")
        self.x0_line_edit = QLineEdit(self.xyyy_widget)
        xyyy_row_layout.addWidget(self.x0_label)
        xyyy_row_layout.addWidget(self.x0_line_edit)

        self.y0_label = QLabel(self.xyyy_widget)
        self.y0_label.setText("Y0 :")
        self.y0_line_edit = QLineEdit(self.xyyy_widget)
        xyyy_row_layout.addWidget(self.y0_label)
        xyyy_row_layout.addWidget(self.y0_line_edit)
        self.layout.addWidget(self.xyyy_widget)

        # Xy Yy
        self.xyyy_widget = QWidget(self)
        xyyy_row_layout = QHBoxLayout(self.xyyy_widget)
        self.xy_label = QLabel(self.xyyy_widget)
        self.xy_label.setText("Xy: :")
        self.xy_line_edit = QLineEdit(self.xyyy_widget)
        xyyy_row_layout.addWidget(self.xy_label)
        xyyy_row_layout.addWidget(self.xy_line_edit)

        self.yy_label = QLabel(self.xyyy_widget)
        self.yy_label.setText("Yy :")
        self.yy_line_edit = QLineEdit(self.xyyy_widget)
        xyyy_row_layout.addWidget(self.yy_label)
        xyyy_row_layout.addWidget(self.yy_line_edit)
        self.layout.addWidget(self.xyyy_widget)

        # Xx Yx

        self.xxyx_widget = QWidget(self)
        xxyx_row_layout = QHBoxLayout(self.xxyx_widget)
        self.xx_label = QLabel(self.xxyx_widget)
        self.xx_label.setText("Xy: :")
        self.xx_line_edit = QLineEdit(self.xxyx_widget)
        xxyx_row_layout.addWidget(self.xx_label)
        xxyx_row_layout.addWidget(self.xx_line_edit)

        self.yx_label = QLabel(self.xxyx_widget)
        self.yx_label.setText("Yy :")
        self.yx_line_edit = QLineEdit(self.xxyx_widget)
        xxyx_row_layout.addWidget(self.yx_label)
        xxyx_row_layout.addWidget(self.yx_line_edit)
        self.layout.addWidget(self.xxyx_widget)

        # athens transformation button
        self.athens_transformation_button = QPushButton()
        self.athens_transformation_button.setText("athens transformation")
        self.athens_transformation_button.clicked.connect(self.athens_transformation_trigger)
        self.layout.addWidget(self.athens_transformation_button)

        # projective transformation button
        self.projective_transformation_button = QPushButton()
        self.projective_transformation_button.setText("projective transformation")
        self.projective_transformation_button.clicked.connect(self.projective_transformation_trigger)
        self.layout.addWidget(self.projective_transformation_button)

        self.setLayout(self.layout)
        self.show()

    @property
    def input_values(self):
        try:
            return {
                "major_radius": float(self.major_radius_line_edit.text()),
                "triangle_side": float(self.triangle_side_line_edit.text()),
                "vertical_move": float(self.vertical_move_line_edit.text()),
                "horizontal_move": float(self.horizontal_move_line_edit.text()),
                "rotation": float(self.rotation_line_edit.text()),
                "x0": float(self.x0_line_edit.text()),
                "y0": float(self.y0_line_edit.text()),
                "xy": float(self.xy_line_edit.text()),
                "yy": float(self.yy_line_edit.text()),
                "xx": float(self.xx_line_edit.text()),
                "yx": float(self.yx_line_edit.text())
            }
        except ValueError:
            print("bad data in inputs")
            return None

    def redraw_trigger(self, *args, **kwargs):
        input_values = self.input_values
        if input_values:
            self.super_on_redraw(input_values)

    def athens_transformation_trigger(self, *args, **kwargs):
        input_values = self.input_values
        if input_values:
            self.super_on_athens_transformation(input_values)

    def projective_transformation_trigger(self, *args, **kwargs):
        input_values = self.input_values
        if input_values:
            self.super_on_projective_transformation(input_values)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._model = kwargs.get("model")
        self._canvas = GenericCanvas(*args, **kwargs)
        self._control_panel = ControlPanel(
            *args,
            **kwargs,
            on_redraw=self.redraw,
            on_athens_transformation=lambda *args: None,
            on_projective_transformation=lambda *args: None
        )
        self._init_ui()

    def _init_ui(self):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self._canvas)
        layout.addWidget(self._control_panel)
        self.setCentralWidget(widget)

    def redraw(self, data):
        with self._model.transformation(data):
            self._canvas.clear()
            self._canvas.paint_cartesian()
            for outline in self._model.outlines:
                self._canvas.draw_outline(outline)


@contextmanager
def App(*args, **kwargs):
    app = QApplication(*args, **kwargs)
    yield app
    app.exec_()
