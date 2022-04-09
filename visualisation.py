import numpy as np
import matplotlib.pyplot as plt

def matrix_heat_map(arr, x_lim=[0, 200], y_lim=[0, 200]):
    plt.imshow(arr, cmap='plasma')
    plt.xlabel("Number Guessed")
    plt.ylabel("Spoken Number")
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.colorbar()
    plt.show()


def histogram_errors(data):
    num_cols = data.shape[1]
    width = 0.8 / num_cols

    offset = 0
    offset_ammount = 0.2

    for i in range(num_cols):
        loc = [(x + offset_ammount * i + offset) for x in range(10)]
        plt.bar(loc, data[:, i], width=width, label="Units: " + str(10**i))
    
    plt.xlim((-0.1, 9+num_cols*offset_ammount))
    plt.legend()
    plt.show()