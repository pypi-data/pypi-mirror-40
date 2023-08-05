# Utilities designed by Mike Bardwell, MSc, University of Alberta
# tied to deriving proper plots for MSc thesis 

import sys
sys.path.append('../../../') # include package path
import traceback

from simhandler.powerflowsim import PowerFlowSim
from simhandler.regressiontools import ParametricRegression as PR
from time import time
import matplotlib.pyplot as plt
from textwrap import wrap
import numpy as np


def generateRandomArray(length):
    return np.random.rand(int(length)).tolist()    

def withRandomValues(feature_size, sim_size):
    node_loads = []
    node_voltages = []
    for i in range(sim_size):
        node_loads.append(generateRandomArray(feature_size))
        node_voltages.append(generateRandomArray(feature_size))
    start = time()
    try:
        PR(np.array(node_loads), np.array(node_voltages))
        end = time()
        return int(end-start)
    except:
        traceback.print_exc(file=sys.stdout)

def plotWithPolyFit(results, max_features, savefig=False):
    """Returns plot with 3rd degree polyfit line
       :type: results: numpy array. 0th index as x, 1st index as y
    """
    
    c = np.polyfit(results[0], results[1], 3) # c is shorthand for coefficient
    plt.plot(results[0], results[1], 'o', 
             [i for i in range(max_features)], 
             [c[3] + c[2]*i + c[1]*i**2 + c[0]*i**3 
              for i in range(max_features)])
    plt.legend(['Experimental', 'Cubic Fit'])
    plt.xlabel('Number of Features')
    plt.ylabel('Time (s)')
    title = 'Compute Time Required to Solve for Parametric Coefficients \
Versus Number of Features'
    plt.title('\n'.join(wrap(title,50)))
    if savefig:
        plt.savefig('featuresversustime_' + str(max_features) + '.pdf')
    plt.show()
    
def plotWithFamilyCurves(results, savefig=False):
    """Plots results from accuracyTest function"""
    
#    fig = plt.figure(1)
    for family in results:
        plt.plot(family[1][0], family[1][1], label='Samples: ' + str(family[0]))
    plt.legend(['Samples: ' + str(family[0]) for family in results])
    plt.xlabel('Number of Houses (Features)')
    plt.ylabel('RMSE (p.u)')
    title = 'Parametric Regression For Power System Load Flow. RMSE Versus \
Number of Houses'
    plt.title('\n'.join(wrap(title,50)))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.axis((results[0][1][0][0], results[0][1][0][-1], 0, 0.001))
    if savefig:
        plt.savefig('parametricRMSEvsfeatures_familyofcurves.pdf')
    plt.show()
    
def plotHistogram(error, no_bins):
    """
    Histogram plotting
    :type error: Array of mean absolute error values
    """
    
    for i in range(len(error)):
        plt.hist(error[i], bins = no_bins)
    plt.xlabel("Prediction Error")
    plt.ylabel("Count")
    title = 'Prediction RMSE Histogram For Normal Equation \
Regression of PSLF'
    plt.title('\n'.join(wrap(title,50)))
    plt.show()
    
    
"""
Default test functions
"""

def basicTimingTest(max_features=12000):
    """Returns polyfitted graph with time vs number of features using random
       data. Demonstrates cubic relationship.
    """
    
    results = []
    for i in range(50,max_features,1000): 
        results.append([i, withRandomValues(i, 10)])
    plotWithPolyFit(np.array(results).T, max_features)
    return results
    
#results = basicTimingTest(max_features=120)

def accuracyTest(features, samples_per_feature):
    """Returns graph with family of curves of accuracy vs number of features. 
       Each curve is dependent on number of samples of power flow data per
       feature.
       :type: features: list with number of features per iteration
       :type: samples_per_feature: list with number of powerflow time steps
       per feature
    """

    results = []
    for samples in samples_per_feature:
        sub_results = [[], [], []]
        for no_houses in features:
            pfs = PowerFlowSim(samples, './data/montecarlo' + str(no_houses) 
                               + '.json')
            start = time()        
            para_reg = PR(pfs.node_loads, pfs.node_voltages)
            end = time()
            sub_results[0].append(no_houses)
            sub_results[1].append(para_reg.evaluateModel())
            sub_results[2].append(int(end-start))
            print('At ', str(no_houses), ' features')
        print('At sample ', str(samples))
        results.append([samples, sub_results])
    plotWithFamilyCurves(results)
    return results

results = accuracyTest([i for i in range(10, 40, 10)], [200])
    
