## About The Project

This project is the result of the exercises done by Giacomo Menegatti, Enrico Grippi, gaia Volpi and Dario Puggioni during the lectures of Computational Astrophysisics by professor Tiziano Zingales at university of Padua, 2024-2025. 

This python packages contains the exercises 1 and 3 of the course.

## Using the daneel package

### Installing daneel

In a fresh python environment, install the package contained inside the dist folder with pip

```sh
pip install /path/to/directory/daneel-0.0.1.tar.gz
```

This will also install all the required libraries.



## Transit lightcurve

This method of the daneel package is contained in the **detection** folder. It uses the [batman](https://lkreidberg.github.io/batman/docs/html/index.html) package to simulate the lightcurve of a planet transiting in front of its star. 


  ```sh
  daneel -i input_file.yaml -t
  ```

  The *input_file.yaml* (e.g., [WASP_96b_transit_params](https://github.com/enricogrippi/comp_astro_24/blob/main/WASP_96b_transit_params.yaml))contains the orbital parameters and the stellar properties. The method returns a plot of the lightcurve.

## Atmospheric simulation

The atmospheric simulation and retrieval use the [TauREX](https://taurex3-public.readthedocs.io/en/latest/index.html) Bayesian exoplanet retrieval framework. 
The simualtion of an exoplanetary atmosphere is done by typing in a terminal the following command.

  ```sh
  daneel -i input_file.yaml -a model
  ```

  The *input_file.yaml* contains the physical and atmospheric parameters of the planet (use [WASP_62_model](https://github.com/enricogrippi/comp_astro_24/blob/main/WASP_62b_model.yaml) as an example). This will produce a simulated spectrum image (*planet_name_spectrum.png*) and a table of transit depths (i.e., the ratio $(R_P/R_*)^2$) at each wavelength (*planet_name_spectrum.dat*) .

## Atmospheric retrieval

With this method, daneel performs a retrieval of an exoplanetary atmosphere. 

  ```sh
  daneel -i input_file.yaml -a retrieve
  ```

The input file contains the path to a measured transit depth table (for example, [WASP-96](https://github.com/enricogrippi/comp_astro_24/blob/main/WASP_96_b_3.11667_5310_1.tbl)) and the parameters that will be fitted (use [WASP_96b_retrieval_params](https://github.com/enricogrippi/comp_astro_24/blob/main/WASP_96b_retrieval_params.yaml) as an example).  

The package will return the fitted spectrum, the best fit parameters and a corner plot of the posterior distribution.
