import matplotlib.pyplot as plt
import numpy as np

def plot_sin(a=1, omega=1):
    x = np.linspace(-1,1, 101)
    plt.plot(x, a*np.sin(omega*x))
    plt.title('SINPLOT')
    plt.show()