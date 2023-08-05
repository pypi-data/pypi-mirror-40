import numpy as np
from simhandler.smartsim import SmartPSLF

configuration_file = 'C:/Users/mikey/Downloads/3node.json'
sim = SmartPSLF(configuration_file)

fake_load_profile = np.ones((10,3)) # Ten timesteps, three input features
#TODO: Make it so test returns True/False flag instead of print
print(sim.map.predictWithModel(fake_load_profile))