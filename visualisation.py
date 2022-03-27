import matplotlib.pyplot as plt

def matrix_heat_map(arr, x_lim, y_lim):
    plt.imshow(arr, cmap='plasma')
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.colorbar()
    plt.show()