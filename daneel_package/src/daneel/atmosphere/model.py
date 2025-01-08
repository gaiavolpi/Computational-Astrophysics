import matplotlib.pyplot as plt
import numpy as np
import taurex.log
from taurex.cache import OpacityCache,CIACache

from taurex.planet import Planet
from taurex.stellar import BlackbodyStar
from taurex.temperature import Isothermal
from taurex.chemistry import TaurexChemistry, ConstantGas
from taurex.model import TransmissionModel
from taurex.contributions import AbsorptionContribution, RayleighContribution, CIAContribution
from taurex.binning import FluxBinner,SimpleBinner

def create_transmission_model(input_params):
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

    for gas, abundance in zip(input_params['gas'], input_params['abundance']):
        chemistry.addGas(ConstantGas(gas,mix_ratio=10**abundance))


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

    '''
    #Plotting gas abundaces
    plt.figure()

    for x,gasname in enumerate(tm.chemistry.activeGases):
        plt.plot(tm.chemistry.activeGasMixProfile[x],tm.pressureProfile/1e5,label=gasname)

    for x,gasname in enumerate(tm.chemistry.inactiveGases):
        plt.plot(tm.chemistry.inactiveGasMixProfile[x],tm.pressureProfile/1e5,label=gasname)
        
    plt.gca().invert_yaxis()
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel('Abundance')
    plt.ylabel('Pressure (Pa)')
    plt.legend(ncols=6, loc='upper center', bbox_to_anchor=(0.5, 1.1))
    plt.show()
    '''

    binned_fig = plt.figure()

    title = input_params['planet_name']
    #Make a logarithmic grid
    wngrid = np.sort(10000/np.logspace(-0.4,1.1,500))
    bn = SimpleBinner(wngrid=wngrid)

    bin_wn, bin_rprs,_,_  = bn.bin_model(tm.model(wngrid=wngrid))

    plt.title(f'{title} transmission spectrum')
    plt.plot(10000/bin_wn,bin_rprs)
    plt.xscale('log')
    plt.xlabel('Wavelength [$\mu$m]')
    plt.ylabel('$(R_{P}/R_{S})^{2}$')
    plt.tight_layout()
    plt.savefig(f'{title}_spectrum.png')
    plt.show()


    # now we make a .dat file in which the data of the spectrum are stored, then we write the abundances of the various active gases:

    wn = np.array(10000/bin_wn)
    bin_rprs_square_root = bin_rprs**0.5

    np.savetxt(f'{title}_spectrum.dat', np.column_stack([wn,bin_rprs,bin_rprs_square_root]), header='Wavelength, (Rp/Rs)^2, Rp/Rs', delimiter='\t')

