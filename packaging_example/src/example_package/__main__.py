import argparse
from example_package.sin_plot import *

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-o",
        "--omega",
        dest="omega",
        type=float,
        required=False,
    )

    parser.add_argument(
        "-A",
        "--amplitude",
        dest="amplitude",
        type=float,
        required=False,
    )

    args = parser.parse_args()
    
    omega, a = 1,1
    if args.omega:
        omega = args.omega

    if args.amplitude:
        a = args.amplitude

    plot_sin(a,omega)

if __name__ == '__main__':
    main()
