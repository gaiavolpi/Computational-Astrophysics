## About The Project

This project is the result of the exercises done by Giacomo Menegatti, Enrico Grippi, gaia Volpi and Dario Puggioni during the lectures of Computational Astrophysisics by professor Tiziano Zingales at university of Padua, 2024-2025. 

This python packages contains the exercises 1 and 3 of the course.

## Using the daneel package

### Installing daneel

In a fresh python environment, install the package contained inside the dist folder with pip

```sh
pip install /path/to/directory/daneel-0.0.1.tar.gz
```

This also install all the required libraries.



## Transit lightcurve

This method of the daneel package is contained in the **detection** folder. It uses the **batman** package


  ```sh
  daneel -i input_file.yaml -t
  ```

## Atmospheric simulation

The atmospheric simulation and retrieval use the **TAUREX** package. 
The simualtion of an exoplanetary atmosphere is done by typing in a terminal the following command.

  ```sh
  daneel -i input_file.yaml -a model
  ```

  The input_file.yaml contains the physical and atmospheric parameters of the planet (use [WASP_62_model]() as an example). This will produce a simulated spectrum image (__planet_name_spectrum.png__) and a table of transit depths (i.e., the ratio $(R_P/R_*)^2$) at each wavelength (__planet_name_spectrum.dat__) .

## Atmospheric retrieval

With this method, daneel performs a retrieval of an exoplanetary atmosphere by reading 

  ```sh
  daneel -i input_file.yaml -a retrieve
  ```


<!-- MARKDOWN LINKS & IMAGES -->