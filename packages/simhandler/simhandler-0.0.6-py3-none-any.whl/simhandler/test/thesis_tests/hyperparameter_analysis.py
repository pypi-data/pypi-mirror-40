# -*- coding: utf-8 -*-
"""
Linear regression tools for Power Flow emulation

@author: Michael Bardwell, University of Alberta, Edmonton AB CAN
"""

import sys
sys.path.append('../')
from simhandler.powerflowsim import PowerFlowSim
import datetime
import json
from time import time
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.layers import Dropout
import matplotlib.pyplot as plt
import numpy as np
import talos as ta

class ANNRegression():
    """Trains feedforward ANN using power system load flow load/voltage data"""

    def __init__(self, load_profile=None, voltage_profile=None, 
                 train_percentage=0.7, save_model=False, plot_results=False):

        if load_profile is not None and voltage_profile is not None:
            _split_index = int(train_percentage * len(load_profile))
            self.train_data = load_profile[0:_split_index]
            self.train_labels = voltage_profile[0:_split_index]

            self.test_data = load_profile[_split_index+1:]
            self.test_labels = voltage_profile[_split_index+1:]
            
            self.out = None
#            self.evaluateModel()
#            self.predictWithModel(plot_results)
            if save_model:
                self.model_name = 'ann_model_' + str(datetime.datetime.now()).\
                               replace(':', '-').replace(' ', '_')
                self.saveModel(self.model_name)

    def buildModel(self, params):
        """
        :type dropout: False (bool) or number between 0-1
        :rtype self.model: class 'keras.engine.sequential.Sequential'
        """
        self.model = keras.Sequential()
        self.model.add(keras.layers.Dense(
            params['first_neuron'],
            activation=tf.nn.relu,
            input_shape=(self.train_data.shape[1],)))
        self.model.add(keras.layers.Dropout(params['dropout']))
        self.model.add(keras.layers.Dense(
                self.train_labels.shape[1],
                activation=params['last_activations']))
            
        self.model.compile(loss=params['losses'],
                           optimizer=params['optimizer'],
                           metrics=['acc'])

    def trainModel(self, params):
        """Trains ANN using Tensorflow backend"""

        self.out = self.model.fit(
                self.train_data,
                self.train_labels,
                batch_size=params['batch_size'],
                epochs=params['epochs'],
                verbose=0,
                validation_split=0.2
                )

    def evaluateModel(self, params):
        """Evalutes keras ann model against test data"""

        self.buildModel(params)
        self.trainModel(params)
        out = self.out
        model = self.model
        return out, model

    def predictWithModel(self, plot_results=True):
        """Makes predictions by applying learned ANN model on test data"""

        test_predictions = self.model.predict(self.test_data)

        if plot_results:
            plt.plot(self.test_labels, test_predictions, 'o')
            plt.xlabel('True Values')
            plt.ylabel('Predictions')
            plt.axis('equal')
            plt.xlim(plt.xlim())
            plt.ylim(plt.ylim())
            plt.plot([-100, 100], [-100, 100])
            plt.show()

            # Histogram
            error = test_predictions - self.test_labels
            for i in range(len(error[0])):
                plt.hist(error.T[i], bins=50)
            plt.xlabel("Prediction Error")
            plt.ylabel("Count")
            plt.show()
            self.plotHistory()

    def plotHistory(self, savefig=False):
        """Plot learning curve"""
        
        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Root Mean Square Error')
        plt.title('ANN Training and Validation Loss Versus Epochs')
        plt.plot(self.history.epoch, 
                 np.array(self.history.history['loss']),
                 label='Training Loss')
        plt.plot(self.history.epoch, 
                 np.array(self.history.history['val_loss']),
                 label='Validation loss')
        plt.legend()
        plt.ylim([0, 0.2])
        if savefig:
            plt.savefig('./data/print/analysis_trainandvalidationloss.pdf')
        plt.show()

    def saveModel(self, name='annmodel'):
        """Save learned ANN model"""
        
        ## TO DO: Test this function
        model_json = self.model.to_json()
        with open('./data/lookup_tables/' + name + ".json", "w") as file:
            json.dump(model_json, file)
        file.close()

        # serialize weights to HDF5
        self.model.save_weights('./data/lookup_tables/' + name + ".h5")

    def loadModel(self, model_name):
        """Decodes a JSON file into a keras model"""

        path = './data/lookup_tables/'
        try:
            with open(path + model_name + '.json', 'r') as ann_model_json:
                model_json_string = ann_model_json.read().\
                replace('\\', '')[1:-1]
                model = model_from_json(model_json_string)
            ann_model_json.close()
            model.load_weights(path + model_name + '.h5', by_name=False)
            print('Opening ANN-derived look up table')
            return model
        except BaseException as ex:
            print('Line {} - lookup table loading failed. {}'.format(
                sys.exc_info()[2].tb_lineno, ex))
            return False
        
"""
Test function
"""
from keras import backend
 
def rmse(y_true, y_pred):
	return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))

def build_model(x_train, y_train, x_val, y_val, params):

    model = Sequential()
    model.add(Dense(params['first_neuron'], input_dim=x_train.shape[1], 
                    activation=params['activation']))
    model.add(Dropout(params['dropout']))
    model.add(Dense(y_train.shape[1]))

    model.compile(optimizer=params['optimizer'],
                  loss=params['losses'],
                  metrics=['mae'])

    out = model.fit(x_train, y_train,
                    batch_size=params['batch_size'],
                    epochs=params['epochs'],
                    verbose=0,
                    validation_data=[x_val, y_val])

    return out, model

p = {'lr': [0.001, 0.00001],
     'first_neuron':[64],
     'hidden_layers':[1],
     'batch_size': [None],
     'epochs': [i for i in range(10,10000,1000)],
     'dropout': [0],
     'weight_regulizer':[None],
     'emb_output_dims': [None],
     'optimizer': ['Adam'],
     'losses': ['mse'],
     'activation':['relu']}

pfs = PowerFlowSim(100)
x = pfs.node_loads
y = pfs.node_voltages

h = ta.Scan(x, y,
          params=p,
          dataset_name='first_test',
          experiment_no='2',
          model=build_model,
          grid_downsample=1)