import argparse

parser = argparse.ArgumentParser(description='Test get')
parser.add_argument("-q", "--quiet", action="count",
                    help='quiet level (q - ERROR, qq - CRITICAL)', default=0)
parser.add_argument("-v", "--verbose", action="count",
                    help='verbose level (v - INFO, vv - DEBUG, vvv - TRACE)', default=0)

args = parser.parse_args()

if args.quiet > 2:
    raise ValueError("quiet level must be <= 2")

if args.verbose > 3:
    raise ValueError("verbose level must be <= 3")

levels = {
  "quiet": [None, "ERROR", "CRITICAL"],
  "verbose": ["WARNING", "INFO", "DEBUG", "TRACE"]
}

level = levels["quiet"][args.quiet] if args.quiet > 0 else levels["verbose"][args.verbose]
print(f"{level=}")