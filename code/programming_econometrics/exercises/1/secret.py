import sys
import getopt

A_ord = ord('A')
Z_ord = ord('Z')
a_ord = ord('a')
z_ord = ord('z')


def modded(frm, to, n):
    '''
    A function that increases a number modding it between a minimum and maximum
    '''
    return ((n - frm) % (to - frm)) + frm


def move_forwards(n=1):
    '''
    Returns a function that takes a character and shifts it by "n"
    '''
    def shift_character(c: str) -> str:
        order = ord(c)
        if A_ord <= order <= Z_ord:
            return chr(modded(A_ord, Z_ord, order + n))

        elif a_ord <= order <= z_ord:
            return chr(modded(a_ord, z_ord, order + n))

        else:
            return c

    return shift_character


def encode(message: str, n=3) -> str:
    return ''.join(map(move_forwards(n), message))


def read_opt():
    by = 3
    message = ''
    argv = sys.argv[1:]
    opts, _ = getopt.getopt(argv, 'hb:m:', ['by=', 'message='])

    for opt, arg in opts:
        if opt == '-h':
            print('python secret.py -b <n> -m <text>')
            sys.exit()
        elif opt in ('-b', '--by'):
            by = int(arg)
        elif opt in ('-m', '--message'):
            message = arg

    if len(message) == 0:
        print('No message input')
        sys.exit()

    return by, message


def main():
    by, message = read_opt()
    print('Result:\n', encode(message, by))


if __name__ == '__main__':
    main()
