import time
import sys


class colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    ENDC = "\033[0m"


def main():
    # CURSOR_UP_ONE = "\x1b[1A"
    ERASE_LINE = "\x1b[2K"
    count = int(sys.argv[1])
    print("")
    for i in reversed(range(count)):
        color = colors.RED if i < 3 else colors.GREEN
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write("   %s%d%s seconds left\r" % (color, i + 1, colors.ENDC))
        time.sleep(1)
    print("  ", count, "seconds complete")


if __name__ == "__main__":
    main()
