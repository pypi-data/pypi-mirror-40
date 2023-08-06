from autolens.data.array.util import array_util

import matplotlib.pyplot as plt
import numpy as np

import os

path = '{}/'.format(os.path.dirname(os.path.realpath(__file__)))
file_path = path+'/rj_lens_plots/data_original/power_law/ML_RJLens2_All_Recon_Src.dat'

file = open(file_path, 'r')

fileread = file.readlines()

image = np.zeros((422,422))

with open(file_path, "r") as f:
    for i, lineread in enumerate(fileread):
        line = str(round(float(fileread[i][0:13]), 2))
        line += ' ' * (8 - len(line))
        line += str(round(float(fileread[i][13:25]), 2))
        line += ' ' * (16 - len(line))
        line += str(float(fileread[i][25:80])) + '\n'
        image[int(fileread[i][0:13]), int(fileread[i][13:25])] = float(fileread[i][25:80])
       # print(int(fileread[i][0:13]), int(fileread[i][13:25]), float(fileread[i][25:80]))
       # f.write(line)

image = image.T
# image = np.fliplr(image)
image = np.flipud(image)

plt.imshow(image)
plt.show()

output_path = path+'/rj_lens_plots/data_fits/power_law/source_model_image.fits'

array_util.numpy_array_to_fits(array=image, path=output_path)