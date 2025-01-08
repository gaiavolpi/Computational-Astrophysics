import argparse
from .detection.transit import *
from .parameters.parameters import Parameters
from .atmosphere.retrieval import *
from .atmosphere.model import *

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
        # If no dest is indicated and action is store true, the flag does not expect a value
        action = 'store_true',
        required=False,
    )

    parser.add_argument(
        "-a",
        "--atmosphere",
        dest = 'action',
        required=False,
    )

    args = parser.parse_args()
    print('\nReading input file:')
    print(f'--- {args.input_file}\n')
    
    # Read input file parameters and store them into a dictionary
    input_pars = Parameters(args.input_file).params

    if args.transit:

        planet_name = input_pars['title']
        print(f'Plotting transit of {planet_name}')
        #Plot transit
        plot_transit(input_pars)

    if args.action == 'retrieve':
        # Retrieve the atmospheric composition of the planet

        retrieve_atmosphere(input_pars)

    elif args.action == 'model':
        # Create a model of a transmission spectrum
        create_transmission_model(input_pars)
        

if __name__ == '__main__':
    main()
