import matplotlib.pyplot as plt

def matrix_heat_map(arr):
    plt.imshow(arr, cmap='plasma')
    plt.colorbar()
    plt.show()