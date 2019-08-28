import sys
import getopt


def read_opt():
    obs = 1
    sigma = 0.25
    argv = sys.argv[1:]
    opts, _ = getopt.getopt(argv, 'ho:s:', ['obs=', 'sigma='])

    for opt, arg in opts:
        if opt == '-h':
            print('python your.py -o 25 -s 0.25')
            sys.exit()
        elif opt in ('-o', '--obs'):
            obs = int(arg)
        elif opt in ('-s', '--sigma'):
            sigma = int(arg)

    return obs, sigma
