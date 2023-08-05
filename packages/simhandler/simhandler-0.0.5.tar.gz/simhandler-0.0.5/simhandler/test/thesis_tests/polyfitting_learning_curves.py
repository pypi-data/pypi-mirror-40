"""
Polyfitting learning curves code by Mike Bardwell, MSc
University of Alberta, 2018
"""

import sys
sys.path.append('../../../') # include package path

from simhandler.powerflowsim import PowerFlowSim
from simhandler.regressiontools import ANNRegression
import matplotlib.pyplot as plt
from textwrap import wrap
import numpy as np
from scipy.optimize import curve_fit

def train(features):
    pfs = PowerFlowSim(1000, '../../data/montecarlo' + str(features) + '.json')
    ann = ANNRegression(pfs.node_loads, pfs.node_voltages, no_epochs=10000)
    x = ann.history.epoch
    y = ann.history.history['val_loss']
    return x, y

#def modelFunc(x, a, b, c):
#    return a*np.exp(-b*x) + c
#
#p, pcov = curve_fit(modelFunc, x, y, p0=[1, 0.1, 0.1])
#print(p, pcov)

plt.figure()
plt.xlabel('Epoch')
plt.ylabel('Root Mean Square Error')
plt.title('ANN Training and Validation Loss Versus Epochs')

samples = []
for i in [10, 20, 30]:
    print('Training ', i)
    samples.append(train(i))
    plt.plot(samples[0][0], samples[0][1], 'o', label = str(i))
plt.legend()
plt.axis([0, 1000, 0, 0.2])
