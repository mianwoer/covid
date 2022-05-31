#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
# import scipy.signal as signal

# practice reading in complex values stored in a file
# Read in data that has been stored as raw I/Q interleaved 32-bit float samples

iqFile = "C:\\Users\\zhuliu4\\Desktop\\cw_78000_6000.dat"
sampRate = 78125
fftSize = 1024
# dat = np.fromfile(iqFile, dtype=np.complex64, count=78125, offset=0)
dat = np.fromfile(iqFile, dtype=np.complex64)

# Plot the spectogram of this data
# plt.specgram(dat[0:78125], NFFT=fftSize, Fs=sampRate)
# plt.specgram(dat, NFFT=fftSize, Fs=sampRate)
# plt.title("title")
# plt.xlabel("Time(s)")
# plt.ylabel("Frequency(Hz)")
# plt.show()

# Let's try a PSD plot of the same data
plt.psd(dat, NFFT=fftSize, Fs=sampRate)
# fig, ax = plt.subplots()
# points, = ax.plot(range(10), 'ro')
# ax.axis([-1, 10, -1, 10])
# x, y = points.get_data()
# xy_pixels = ax.transData.transform(np.vstack([x,y]).T)
# xpix, ypix = xy_pixels.T
# width, height = fig.canvas.get_width_height()
# ypix = height - ypix
# print('Coordinates of the points in pixel coordinates...')
# for xp, yp in zip(xpix, ypix):
#     print( '{x:0.2f}\t{y:0.2f}'.format(x=xp, y=yp))
# fig.savefig('test.png', dpi=fig.dpi)


plt.title("title")
plt.show()
