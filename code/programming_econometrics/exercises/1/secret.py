A_ord = ord('A')
Z_ord = ord('Z')
a_ord = ord('a')
z_ord = ord('z')


def modded(frm, to, n):
    '''
    A function that increases a number modding it between a minimum and maximum
    '''
    return ((n - frm) % (to-frm)) + frm


def move_forwards(n=1):
    '''
    Returns a function that takes a character and shifts it by "n"
    '''
    def shift_character(c: str) -> str:
        order = ord(c)
        if order >= A_ord and order <= Z_ord:
            return chr(modded(A_ord, Z_ord, order + n))

        elif order >= a_ord and order <= z_ord:
            return chr(modded(a_ord, z_ord, order + n))

        else:
            return c

    return shift_character


def encode(message: str, n=3) -> str:
    return ''.join(map(move_forwards(n), message))


def main():
    print('result:\n', encode('This is a secret message!', 3))


if __name__ == '__main__':
    main()
