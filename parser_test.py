import argparse

# описание необходимых аргументов командной строки

# обязательные аргументы:
# размер:
# -s --size (ширина x высота)
# path - путь к папке с изображениями
# (может быть несколько путей, разделенных пробелом)
# lines - количество линий в коллаже

# необязательные аргументы:
# quiet - не выводить на экран прогресс выполнения
# verbose - выводить на экран подробную информацию о выполняемых действиях

import os
# formatter = lambda p: argparse.HelpFormatter(p, max_help_position=42)
# formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27)
formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=42)
parser = argparse.ArgumentParser(formatter_class=formatter)
parser.add_argument("-q", "--quiet", action="count",
                    help='quiet level (q - ERROR, qq - CRITICAL)', default=0)

parser.add_argument("-v", "--verbose", action="count",
                    help='verbose level (v - INFO, vv - DEBUG, vvv - TRACE)', default=0)

parser.add_argument("dir", type=str, nargs='*', default=os.getcwd(), help='directory with images')
# parser.add_argument("-p", "--path", type=str, help='path to images', required=True)
parser.add_argument("-s", "--size", type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'),
                    help='size of collage (width x height, or \'screen\')',
                    required=True)

parser.add_argument("-l", "--lines", type=int, help='lines in collage', required=True)

args = parser.parse_args()
print(args)

if args.quiet > 2:
    raise ValueError("quiet level must be <= 2")

if args.verbose > 3:
    raise ValueError("verbose level must be <= 3")

levels = ["ERROR", "CRITICAL", "WARNING", "INFO", "DEBUG", "TRACE"]
log_level = levels[args.verbose - args.quiet + levels.index(log_level)]

level = levels["quiet"][args.quiet] if args.quiet > 0 else levels["verbose"][args.verbose]
print(f"{level=}")

size = args.size.split('x')
print(f"{size=}")
match size:
    case ["screen"]:
        size = "1920x1080"
        print(f"{size=}")
    case [width, height]:
        size = (int(width), int(height))
        print(f"{size=}")