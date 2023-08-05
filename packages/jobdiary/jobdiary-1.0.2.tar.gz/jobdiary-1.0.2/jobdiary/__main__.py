import sys


def main():
    from .core import main
    sys.exit(main())


def run(args):
    from .core import main
    return main(args)


if __name__ == '__main__':
    main()
