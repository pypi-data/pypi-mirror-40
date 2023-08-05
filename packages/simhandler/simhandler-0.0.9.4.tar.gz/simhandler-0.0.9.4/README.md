# intelligent-simulation-handler

### What is this repository for? ###

* Software development of an intelligent simulation handler for power system load flow simulations
* Project completed as partial requirement of attaining MSc at the University of Alberta  

### How do I get set up? ###

* *pip install simhandler*
* To run the basic 3 node example:
  1. Download [3node.json](https://github.com/mbardwell/intelligent-simulation-handler/tree/master/simhandler/data/network_configurations) file and put it under *simhandler\data\network_configurations* as *3node.json*
    *For example, C:\Users\mikey\Anaconda3\envs\microgrid_workcomp\Lib\site-packages\simhandler\data\network_configurations\3node.json
  2. In a Python 3 terminal:
    *from simhandler.intelligentsimulationhandler import IntelligentSimulationHandler as ish
    *ish('./data/network_configurations/3node.json')

### Contribution guidelines ###

* Follow PEP8 guidelines with the following exception: use lowercaseUppercase function naming instead of snake_case

### Questions? ###

* If you find a bug or want a feature. Create an issue
* Otherwise, send emails with title 'Intelligent Simulation Handler - *Question/Comment*' to bardwell@ualberta.ca
