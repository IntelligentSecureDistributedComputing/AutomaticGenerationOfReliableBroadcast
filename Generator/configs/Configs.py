##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################
#
import commentjson
#
configurations_file = open('configs/configs.jsonc',)
configurations = commentjson.load(configurations_file)

##################################################################################################################################
#
#   FUNCTIONS
#
##################################################################################################################################


def getResultsBatchSize():
    return configurations["ResultsBatch"]

# ----------------------------------------------------------------


def runExplorationAlgorithm(algorithm):
    """Check the exploration algorithm to be used

    Args:
        algorithm (string): algorithm name to be used

    Returns:
        boolean: True if the algorithm is to be used; False if not
    """
    return configurations["ExplorationAlgorithm"][algorithm]["Mode"]

# ----------------------------------------------------------------


def getExplorationAlgorithmHyperparameters(algorithm, parameter):
    """Get the parameters of the exploration algorithm

    Args:
        algorithm (string): algorithm to get the parameters
        parameter (string): parameter to get the value

    Returns:
        int: value of the hyperparameter
    """
    return configurations["ExplorationAlgorithm"][algorithm]["Hyperparameters"][parameter]

# ----------------------------------------------------------------


def runLearningAlgorithm(algorithm):
    """Check if the learning algorithm is to be used

    Args:
        algorithm (string): algorithm to check

    Returns:
        boolean: True if the specific algorithm is to be used; False if not
    """
    return configurations["LearningAlgorithm"][algorithm]["Mode"]

# ----------------------------------------------------------------


def getLearningAlgorithmHyperparameter(algorithm, parameter):
    """Get learning algorithm hyperparameters

    Args:
        algorithm (string): learning algorithm name
        parameter (string): hyperparameter

    Returns:
        int: value of the hyperparameter
    """
    return configurations["LearningAlgorithm"][algorithm]["Hyperparameters"][parameter]

# ----------------------------------------------------------------


def runQLearningExtra(extra):
    """Check if the QLearning extra process is to be used

    Args:
        extra (string): name of the extra configuration

    Returns:
        boolean: True if is going to be used; False if not
    """
    return configurations["LearningAlgorithm"]["QLearning"]["Extra"][extra]["Mode"]
