import matplotlib as matplotlib
import astropy
import numpy as np
import matplotlib.pyplot as mpl
from astropy.io import fits
import pylab
# import healpy as hp
# import scipy as sp
# import Benlibv2TEST as ben#
# import faulthandler
import time
from mpl_toolkits.axes_grid.inset_locator import inset_axes as axesfiddle
import os
import sys
from pylab import cm
from scipy import misc
import imageio

matplotlib.use('Agg')


def make_gauss(centre, amp, sig, shapdim):
	# just makes a Gaussian centred on chosen coordinates to use as the grav potential in the field
	gauss=np.zeros(shapdim)
	sidelenx=shapdim[1]
	sideleny=shapdim[0]
	l=np.zeros(shapdim)

	for i in range(0, sideleny):
		for j in range(0, sidelenx):
			l[i, j]=np.sqrt((centre[0]-i)**2+(centre[1]-j)**2)
	gaussblob=amp*np.exp(-(l**2)/sig)
	return gaussblob


# image=
image2=np.zeros(image.shape)

grad1=np.gradient(gauss)

bendx=np.zeros((image.shape[0], image.shape[1]))
bendy=np.zeros((image.shape[0], image.shape[1]))
for i in range(0, image.shape[0]):
	for j in range(0, image.shape[1]):
		bendx[i,j]=grad1[1][i][j]
		bendy[i,j]=grad1[0][i][j]

for i in range(0, image.shape[0]):
	for j in range(0, image.shape[1]):
		if ((i-int(bendy[i,j]))<0):
			makeblobnew2[i,j]=0
		elif ((i-int(bendy[i,j]))>sidelen-1):
			makeblobnew2[i,j]=0
		elif ((j-int(bendx[i,j]))<0):
			makeblobnew2[i,j]=0
		elif ((j-int(bendx[i,j]))>sidelen-1):
			makeblobnew2[i,j]=0
		else:
			image2[i,j,0]=image[i-int(bendy[i,j]), j-int(bendx[i,j]), 0]
			image2[i,j,1]=image[i-int(bendy[i,j]), j-int(bendx[i,j]), 1]
			image2[i,j,2]=image[i-int(bendy[i,j]), j-int(bendx[i,j]), 2]

#image2 is the lensed result
