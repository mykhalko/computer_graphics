import sys

from view import (
    App,
    MainWindow
)


from tools import coordinates_adapter
from model import Model


def main():
    with App(sys.argv):
        size = 700
        virtual_size = 10
        model = Model("objects.json", adapter=coordinates_adapter(size, virtual_size))
        window = MainWindow(size=size, virtual_size=virtual_size, model=model)
        window.show()


if __name__ == "__main__":
    main()
