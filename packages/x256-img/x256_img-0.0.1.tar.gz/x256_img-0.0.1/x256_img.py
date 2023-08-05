from PIL import Image
from x256 import x256
from sys import stdout
from argparse import ArgumentParser, FileType
from shutil import get_terminal_size
from sys import platform

if platform in ['cygwin', 'win32']:
    from colorama import init

    init()


def display(data, width):
    for i, px in enumerate(data):
        if i % width == 0:
            stdout.write("\033[0m\n")
        px = px[:3] if len(px) > 3 else px
        stdout.write(f"\033[48;5;{str(x256.from_rgb(*px))}m  ")


def _cli_init():
    parser = ArgumentParser("x256-img", description="Print an image using x256 color escape codes")
    parser.add_argument("--width", type=int, metavar="width", default=32, dest="width", help="width to resize to")
    parser.add_argument("--height", type=int, metavar="height", default=32, dest="height", help="height to resize to")
    parser.add_argument("--original", action="store_true", default=False, dest="original",
                        help="keep the original and don't resize")
    parser.add_argument("--auto", action="store_true", default=False, dest="auto", help="resize to fit the screen")
    parser.add_argument("file", type=FileType('rb'))
    invoke = parser.parse_args()
    img = Image.open(invoke.file)
    if not invoke.original:
        if invoke.auto:
            term = get_terminal_size()
            w = int(term.columns / 2)
            h = term.lines
        else:
            w, h = invoke.width, invoke.height
        img = img.resize((w, h))
    width, _ = img.size
    display(img.getdata(), width)
