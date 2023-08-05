# Utilities designed by Mike Bardwell, MSc, University of Alberta
# tied to deriving proper plots for MSc thesis 

import sys
sys.path.append('../../../')
import traceback

from simhandler.powerflowsim import PowerFlowSim
from simhandler.regressiontools import ANNRegression as AR
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
        AR(np.array(node_loads), np.array(node_voltages))
        end = time()
        return int(end-start)
    except Exception:
        traceback.print_exc(file=sys.stdout)

def plotWithPolyFit(results, max_features, savefig=False):
    """Returns plot with linear polyfit line
       :type: results: numpy array. 0th index as x, 1st index as y
    """
    
    c = np.polyfit(results[0], results[1], 1) # c is shorthand for coefficient
    print(c)
    plt.plot(results[0], results[1], 'o', 
             [i for i in range(max_features)], 
             [c[1] + c[0]*i for i in range(max_features)])
    plt.legend(['Experimental', 'Linear Fit'])
    plt.xlabel('Number of Features')
    plt.ylabel('Time (s)')
    title = 'Compute Time Required to Train ANN Versus Number of Features'
    plt.title('\n'.join(wrap(title,50)))
    if savefig:
        plt.savefig('featuresversustime_' + str(max_features) + '.pdf')
    plt.show()
    
def plotWithFamilyCurves(results, savefig=False):
    """Plots results from accuracyTest function"""
    
    features = results['features']
    samples = []
    for family in results:
        print(family)
        if family == 'features':
            continue
        plt.plot(features, 
                 results[family], 
                 label='Samples: ' + family)
        samples.append(family)
    plt.legend(['Samples: ' + sample for sample in samples])
    plt.xlabel('Number of Houses (Features)')
    plt.ylabel('RMSE (p.u)')
    title = 'ANN Regression For Power System Load Flow. RMSE Versus \
Number of Houses'
    plt.title('\n'.join(wrap(title,50)))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#    plt.axis([features[0], features[-1], 0, 0.05])
    if savefig:
        plt.savefig('annRMSEvsfeatures_familyofcurves.pdf')
    plt.show()
    
    
"""
Default test functions
"""

def basicTimingTest(features):
    """Returns polyfitted graph with time vs number of features using random
       data. Demonstrates cubic relationship.
    """
    
    results = []
    for i in features: 
        results.append([i, withRandomValues(i, 10)])
    print(results)
    plotWithPolyFit(np.array(results).T, max(features))
    return results

#annresults = basicTimingTest([i for i in range(50, 100, 50)])
    
def accuracyTest(features, samples_per_feature):
    """Returns graph with family of curves of accuracy vs number of features. 
       Each curve is dependent on number of samples of power flow data per
       feature.
       :type: features: list with number of features per iteration
       :type: samples_per_feature: list with number of powerflow time steps
       per feature
    """

    results = {'features': features}
    for no_houses in features:
        pfs = PowerFlowSim(samples_per_feature[-1], './data/montecarlo' + 
                           str(no_houses) + '.json')
        for samples in samples_per_feature:
            start = time()        
            ann_reg = AR(pfs.node_loads[0:samples], 
                         pfs.node_voltages[0:samples], 
                         optimizer='Adam')
            end = time()
            if str(samples) in results:
                results[str(samples)].append(ann_reg.evaluateModel()) # TODO: add int(end-start)
            else:
                results[str(samples)] = [ann_reg.evaluateModel()]
            print('Done sample ', str(samples))
        print('Done ', no_houses, ' features')
    plotWithFamilyCurves(results)
    return results

#result = accuracyTest([20, 40, 60], 
#                      [2000, 4000, 6000, 8000])
    
pfs = PowerFlowSim(100)
ann = AR(pfs.node_loads, pfs.node_voltages)
print(ann.evaluateModel())