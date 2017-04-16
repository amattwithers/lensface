import math, os, string, sys, time
import numpy as np
import matplotlib.pyplot as plt


def Lens(imgin=0, M=2000., s=3000., p=(100, 100)):
    # imgin szxsz numpy array (this can be made genaral) or 0
    # M and s Magintude and scale of Phi field (Gaussian at the moment)
    # p coordinates of centre of mass
    if imgin == 0:
        sz = 200.
        x = np.arange(sz)
        xx, yy = np.meshgrid(x, x)
        # create a simple image if you don't have one
        imgin = xx+yy
    sz = np.float(imgin.shape[0])
    x = np.arange(sz)
    xx, yy = np.meshgrid(x, x)
    # Define your Phi field
    Phi = M*np.exp(-((xx-p[0])**2+(yy-p[1])**2)/s)
    # Bend angle is -Grad(Phi)
    gy, gx = np.gradient(Phi)
    imgout = np.zeros_like(imgin)
    # Take Bend angle off pixel in imgout to find where to source it from in imgin.
    for i in range(int(sz)):
        for j in range(int(sz)):
            shift = np.absolute(x[i]+gx-xx)+np.absolute(x[j]+gy-yy)
            try:
                imgout[i, j] = imgin[np.where(shift == np.min(shift))]
            except:
                imgout[i, j] = 0.0

    plt.figure(1)
    plt.pcolor(Phi)
    plt.figure(2)
    plt.pcolor(imgin)
    plt.figure(3)
    plt.pcolor(imgout)
    plt.show()

if __name__ == "__main__":
    Lens()
