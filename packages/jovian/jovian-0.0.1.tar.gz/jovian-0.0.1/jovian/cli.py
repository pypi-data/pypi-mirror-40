import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    print('You provided the command:' + args.command)


if __name__ == '__main__':
    main()
