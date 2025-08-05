import sys
import os
import argparse

from app.application import Application
from app.core.debug import Debug

sys.path.append(os.path.dirname(__file__))


def main():
    parser = argparse.ArgumentParser(description='Tactical Game Engine')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    
    if args.debug:
        Debug.enable()
    
    Debug.log("Starting Tactical Game Engine...", __file__)
    app = Application(debug=args.debug)
    Debug.log("Application initialized, starting game loop", __file__)
    app.run()
    Debug.log("Application finished", __file__)


if __name__ == '__main__':
    main()