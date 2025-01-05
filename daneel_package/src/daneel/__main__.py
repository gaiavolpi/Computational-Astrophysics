import argparse
import os
from .detection.transit import *
from .parameters.parameters import Parameters

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        dest="input_file",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-t",
        "--transit",
        action = 'store_true',
        required=False,
    )

    args = parser.parse_args()
    
    input_pars = Parameters(args.input_file).params

    if args.transit:
        print(input_pars)
        #Plot transit
        plot_transit(input_pars)
        

if __name__ == '__main__':
    main()
