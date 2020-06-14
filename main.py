import sys

from rogw.app import App
from rogw.args import Args


if __name__ == '__main__':
    App(Args(sys.argv)).run()
