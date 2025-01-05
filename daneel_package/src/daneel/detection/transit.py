import batman
import numpy as np
import matplotlib.pyplot as plt

def plot_transit(input_params):
    c1, c2 = np.genfromtxt(input_params['ExoCTK_file'], skip_header=2, usecols=(8,10), unpack=True)
    mean_c1 = np.mean(c1)
    mean_c2 = np.mean(c2)

    params = batman.TransitParams()       #object to store transit parameters
    params.t0 = input_params['t0']                       #time of inferior conjunction
    params.per = input_params['per']                        #orbital period
    params.rp = input_params['rp']                       #planet radius (in units of stellar radii)
    params.a = input_params['a']                         #semi-major axis (in units of stellar radii)
    params.inc = input_params['inc']                       #orbital inclination (in degrees)
    params.ecc = input_params['ecc']                        #eccentricity
    params.w = input_params['w']                         #longitude of periastron (in degrees)
    params.limb_dark = input_params['limb_dark']        #limb darkening model
    params.u = [mean_c1,mean_c2]      #limb darkening coefficients [u1, u2, u3, u4]

    transit_name = input_params['title']

    t = np.linspace(-0.3, 0.3, 1000)  #times at which to calculate light curve
    m = batman.TransitModel(params, t)    #initializes model

    flux = m.light_curve(params)

    plt.plot(t, flux)
    plt.xlabel('Time [days]')
    plt.ylabel('Normalized flux')
    
    plt.title(f'Transit {transit_name}')
    plt.savefig(f'transit.{transit_name}.png')
    plt.show()
