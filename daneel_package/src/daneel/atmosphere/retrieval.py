import matplotlib.pyplot as plt
import numpy as np
import taurex.log
from taurex.cache import OpacityCache,CIACache
import pandas as pd
import corner

from taurex.planet import Planet
from taurex.stellar import BlackbodyStar
from taurex.temperature import Isothermal
from taurex.chemistry import TaurexChemistry, ConstantGas
from taurex.model import TransmissionModel
from taurex.contributions import AbsorptionContribution, RayleighContribution, CIAContribution
from taurex.data.spectrum.observed import ObservedSpectrum
from taurex.optimizer.nestle import NestleOptimizer

def retrieve_atmosphere(input_params):
    taurex.log.disableLogging()

    #Load xsecs and cia data
    OpacityCache().clear_cache()
    OpacityCache().set_opacity_path(input_params['xsecs'])
    CIACache().set_cia_path(input_params['cia']) 

    # Creating isothermal profile   
    isothermal = Isothermal(input_params['T'])

    #Define planet properties
    planet = Planet(input_params['planet_radius'], input_params['planet_mass'])

    #Define star properties
    star = BlackbodyStar(input_params['star_temperature'], input_params['star_radius'])

    chemistry = TaurexChemistry(input_params['fill_gas'],input_params['ratio'])

    for gas in input_params['gas']:
        chemistry.addGas(ConstantGas(gas,mix_ratio=1e-6))



    tm = TransmissionModel(planet=planet,
                        temperature_profile=isothermal,
                        chemistry=chemistry,
                        star=star,
                        atm_min_pressure=input_params['atm_min_pressure'],
                        atm_max_pressure=input_params['atm_max_pressure'],
                        nlayers=30)


    tm.add_contribution(AbsorptionContribution())
    tm.add_contribution(CIAContribution(input_params['cia_pairs']))
    tm.add_contribution(RayleighContribution())

    print('Building the model...')
    tm.build()
    res = tm.model()

    obs = ObservedSpectrum(input_params['obs'])
 
    obin = obs.create_binner()
    '''
    plt.figure()
    plt.errorbar(obs.wavelengthGrid,obs.spectrum, obs.errorBar,label='Observed')
    plt.plot(obs.wavelengthGrid,obin.bin_model(tm.model(obs.wavenumberGrid))[1],label='Initial Model')
    plt.xscale('log')
    plt.legend()
    plt.show()'''



    opt = NestleOptimizer(input_params['fit_live_points'])

    opt.set_model(tm)
    opt.set_observed(obs)

    for param, bound in zip(input_params['params_to_fit'], input_params['bounds_to_fit']):
        opt.enable_fit(param)
        opt.set_boundary(param, bound)

    print('Fitting the observations\n')
    solution = opt.fit()
    taurex.log.disableLogging()

    title = input_params['planet_name']

    for solution,optimized_map,optimized_value,values in opt.get_solution():
        opt.update_model(optimized_map)
        plt.figure()
        plt.errorbar(obs.wavelengthGrid,obs.spectrum,obs.errorBar,label='Observed', alpha=0.4)
        plt.plot(obs.wavelengthGrid,obs.spectrum, marker='s', color='blue', markersize=2, linestyle='')
        plt.plot(obs.wavelengthGrid,obin.bin_model(tm.model(obs.wavenumberGrid))[1],label='Fitted Model')
        plt.xscale('log')
        plt.title(title)
        plt.legend()
        plt.show()



    res = opt.generate_solution()
    fit_params = res['solution0']['fit_params']
    traces = np.array([fit_params[key]['trace'] for key in fit_params.keys()])


    params = [[key,fit_params[key]['value'], fit_params[key]['sigma_m'], fit_params[key]['sigma_p']] for key in fit_params.keys()]
    df = pd.DataFrame(params, columns=['param', 'value', 'sigma_m', 'sigma_p'], index=None)
    df.to_csv(f'{title}-fit.csv', index=False, sep='\t')

    true_values =  input_params['true_values']

    # Create the corner plot with colors and labels
    fig = corner.corner(
        np.transpose(traces),  
        labels=df['param'], 
        color='blue',  
        plot_datapoints=True,  
        fill_contours=True,
        truths = true_values,
        truth_color = 'red',
    )

    corner.overplot_lines(fig, df['value'], linestyle='dashed', c='orange')
    corner.overplot_lines(fig, df['value']+df['sigma_p'], linestyle='dotted', c='orange')
    corner.overplot_lines(fig, df['value']-df['sigma_m'], linestyle='dotted', c='orange')
    plt.title(title)
    plt.show()


