#!/usr/bin/env python3

'''
LensFace Module

Required packages -

python3
opencv (and python bindings)
numpy

'''

import cv2 as cv
import numpy as np


def make_gauss(centre, amp, sig, shapdim):

    '''just makes a Gaussian centred on chosen coordinates to
    use as the grav potential in the field'''

    sidelenx = shapdim[1]
    sideleny = shapdim[0]
    hx = int(sidelenx/2)
    hy = int(sideleny/2)
    l = np.zeros(shapdim)

    ceny = centre[1] * sideleny
    cenx = centre[0] * sidelenx

    for i in range(0, sideleny):

        for j in range(0, sidelenx):

            l[i, j] = np.sqrt((ceny-i)**2+(cenx-j)**2)

    gaussblob = amp*np.exp(-(l**2)/sig)
    # gaussblob = amp * l

    iter = 0
    radius = 0
    while (iter < sidelenx) :
        if (gaussblob[hy][hx+iter] < 0.2*gaussblob[hy][hx]) :
            radius = iter
            break
        else :
            iter += 1

    return -1.0*gaussblob, int(radius)


def calc_tranform(grad, lenx, leny):

    newxpos=np.zeros(lenx*leny, dtype=int)
    newypos=np.zeros(lenx*leny, dtype=int)

    index = 0

    for i in range(0, lenx):

        # print(i)

        for j in range(0, leny):

            # print(i, j)

            newxpos[index]=i-int(grad[0][i][j]) % lenx
            newypos[index]=j-int(grad[1][i][j]) % leny

            gradx = grad[0][i][j]
            grady = grad[1][i][j]

            ii = i-int(grad[0][i][j]) % lenx
            jj = j-int(grad[1][i][j]) % leny
            minx = 1000
            miny = 1000
            while True:
                if abs(grad[0][ii][jj]) < 1.0 or abs(grad[1][ii][jj]) < 1.0:
                    break
                new_minx = i - ii + int(grad[0][ii][jj])
                new_miny = j - jj + int(grad[1][ii][jj])
                deltax = minx - new_minx
                deltay = miny - new_miny
                # print (ii, jj, delta)
                if deltax < 0 or deltay < 0:
                    break
                else:
                    ii -= 1
                    jj -= 1
                    minx = new_minx
                    miny = new_miny

            newxpos[index] = (i - int(grad[0][(ii+1)%lenx][(jj+1)%leny]))%lenx
            newypos[index] = (j - int(grad[1][(ii+1)%lenx][(jj+1)%leny]))%leny

            # if grad[0][newxpos[index]][j] < gradx :
            #     delta = abs(grad[0][newxpos[index]][j] - grad[0][(newxpos[index]-1)%lenx][j])
            #     while grad[0][newxpos[index]][j] < gradx and delta > 1.0:
            #         # print(gradx-grad[0][newxpos[index]][j])
            #         # print(delta)
            #         xind = (newxpos[index] - 1)
            #         gradxx = int(grad[0][xind][j])
            #         newxpos[index]=(i-gradxx)
            #         delta = abs(grad[0][newxpos[index]][j] - grad[0][(newxpos[index]-1)%lenx][j])
            #         print(xind)
            #
            # else :
            #     delta = abs(grad[0][newxpos[index]][j] - grad[0][(newxpos[index]+1)%lenx][j])
            #     while grad[0][newxpos[index]][j] > gradx and delta < -1.0:
            #         xind = (newxpos[index] + 1) % lenx-1
            #         gradxx = int(grad[0][xind][j])
            #         newxpos[index]=(i-gradxx) % lenx-1
            #         delta = abs(grad[0][newxpos[index]][j] - grad[0][(newxpos[index]+1)%lenx][j])
            #
            #
            # if grad[1][i][newypos[index]] < grady :
            #     delta = abs(grad[1][i][newypos[index]] - grad[1][i][(newypos[index]-1)%leny])
            #     while grad[1][i][newypos[index]] < grady and delta > 1.0:
            #         yind = (newypos[index] - 1) % leny-1
            #         gradyy = grad[1][i][yind]
            #         newypos[index]=(j-gradyy) % leny-1
            #         delta = abs(grad[1][i][newypos[index]] - grad[1][i][(newypos[index]-1)%leny])
            #         # print(yind, gradyy, newypos[index])
            #
            # else :
            #     delta = abs(grad[1][i][newypos[index]] - grad[1][i][(newypos[index]+1)%leny])
            #     while grad[1][i][newypos[index]] > grady and delta < -1.0:
            #         yind = (newypos[index] + 1) % leny-1
            #         gradyy = int(grad[1][i][yind])
            #         newypos[index]=(j-gradyy) % leny-1
            #         delta = abs(grad[1][i][newypos[index]] - grad[1][i][(newypos[index]+1)%leny])

            index+=1

    return (newxpos, newypos)
