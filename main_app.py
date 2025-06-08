import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.application import Application


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()