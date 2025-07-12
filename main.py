import sys
import os

from app.application import Application

sys.path.append(os.path.dirname(__file__))


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()