#
#   This class represents the Speaker
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
import utils.Utils as Utils
#

inputs_file_name = "current_generation_inputs.json"

##################################################################################################################################
#
#   FUNCTIONS
#
##################################################################################################################################


def getNumberOfEpisodes():
    """Get the number of episodes to run

    Returns:
        int: number of episodes to run
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Learning"]["NumberOfEpisodes"]

# ----------------------------------------------------------------


def getNumberOfSimulations():
    """Get the number of simulations

    Returns:
        int: number of simulation to run
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Learning"]["NumberOfSimulations"]

# ----------------------------------------------------------------


def runAgent(agent):
    """Check if the agent is ON or OFF

    Args:
        agent (string): agent to check

    Returns:
        boolean: True if the Agent is ON; False if not
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Generation"]["Agents"][agent]

# ----------------------------------------------------------------


def runHeuristic(index):
    """Check if the heuristic is to be used

    Args:
        index (string): index of the heuristic

    Returns:
        boolean: True if the heuristic is to be used; False if not
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Generation"]["Heuristics"][index]["Mode"]


# ----------------------------------------------------------------


def getAlgorithmCharacteristics():
    """Get the weights of each characteristic of the algorithm

    Returns:
        json object: json object with each characteristic and it value
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Generation"]["AlgorithmCharacteristics"]

# ----------------------------------------------------------------


def getMaxNumberOfMessageTypes():
    """Get the maximum number of allowed message types

    Returns:
        int: max number of allowed types
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Generation"]["MaxNumberOfMessageTypes"]

# ----------------------------------------------------------------


def getMaxNumberOfSuspectMessageTypes():
    """Get the maximum number of allowed message types

    Returns:
        int: max number of allowed types
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Generation"]["MaxNumberOfSuspectMessageTypes"]

# ----------------------------------------------------------------


def isActionAllowed(action):
    """Check if a specific action is allowed

    Args:
        action (string): name of the action 

    Returns:
        boolean: True if the action is allowed; False if is not
    """
    try:
        generation_inputs = Utils.readJsonFile(
            'inputs/'+inputs_file_name)
        return generation_inputs["Generator"]["Generation"]["LogicComponents"][action]
    except Exception:
        return False

# ----------------------------------------------------------------


def isThresholdAllowed(threshold):
    """Check if a specific threshold is allowed or not

    Args:
        threshold (string): threshold to check

    Returns:
        boolean: True if the threshold is allowed; False if not
    """
    try:
        generation_inputs = Utils.readJsonFile(
            'inputs/'+inputs_file_name)
        return generation_inputs["Generator"]["Generation"]["ConditionComponents"]["Thresholds"][threshold]
    except Exception:
        return False

# ----------------------------------------------------------------


def isConditionAllowed(condition):
    """Check if a specific condition is allowed or not

    Args:
        condition (string): condition to check

    Returns:
        boolean: True if the condition is allowed; False if not
    """
    try:
        generation_inputs = Utils.readJsonFile(
            'inputs/'+inputs_file_name)
        return generation_inputs["Generator"]["Generation"]["ConditionComponents"][condition]
    except Exception:
        return False

# ----------------------------------------------------------------


def getAllInputs():
    """Get all the inputs

    Returns:
        json object: all the inputs defined
    """
    generation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_inputs["Generator"]["Generation"]

# ----------------------------------------------------------------


def getHeuristicExtra(index):
    """Get heuristic extra configurations

    Args:
        index (string): index of the heuristic

    Returns:
        any: data with the extra configurations of the heuristic
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Heuristics"][index]["Extra"]

# ----------------------------------------------------------------


def getLogicReward(component):
    """Get the reward of a logic componenet

    Args:
        component (string): name of the component

    Returns:
        number: value of the reward
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Rewards"]["Logic"][component]*getAlgorithmCharacteristics()["NumberOfMessagesSent"]

# ----------------------------------------------------------------


def getThresholdReward(component):
    """Get the reward of a threshold

    Args:
        component (string): name of the threshold

    Returns:
        number: value of the reward
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Rewards"]["Condition"]["Thresholds"][component]*getAlgorithmCharacteristics()["NumberOfMessagesRequired"]

# ----------------------------------------------------------------


def getConditionReward(component):
    """Get the reward of a condition

    Args:
        component (string): name of the condition

    Returns:
        number: value of the reward
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Rewards"]["Condition"][component]

# ----------------------------------------------------------------


def getMessageTypeReward():
    """Get the message type reward

    Returns:
        number: value of the reward
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Rewards"]["MessageType"]*getAlgorithmCharacteristics()["NumberOfCommunicationSteps"]

# ----------------------------------------------------------------


def getEventReward(event):
    """Get the reward of the event

    Args:
        event (string): name of the event

    Returns:
        number: value of the event
    """
    # get configurations
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Rewards"]["Event"][event]

# ----------------------------------------------------------------


def getBonusReward(reward):
    """Get the bonus reward

    Args:
        reward (string): name of the bonus

    Returns:
        number: value of the reward
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["BonusRewards"][reward]

# ----------------------------------------------------------------


def runIntermediateValidationProcess():
    """Check if it is to run the intermediate validation process

    Returns:
        boolean: True if it is to run the intermediate validation process; False if is not
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["IntermediateValidationProcess"]["Mode"]


# ----------------------------------------------------------------


def getIntermediateValidationProcessNumberOfSteps():
    """Get the batch size of the intermediate validation process

    Returns:
        number: number of the batch size
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["IntermediateValidationProcess"]["NumberOfSteps"]

# ----------------------------------------------------------------


def isRBLearner():
    """Check if the RBLearner is ON/OFF

    Returns:
        boolean: true if the agent is ON; False if is OFF
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Agents"]["RBLearner"]


# ----------------------------------------------------------------


def isCSLearner():
    """Check if the CSLearner is ON/OFF

    Returns:
        boolean: true if the agent is ON; False if is OFF
    """
    generation_configs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return generation_configs["Generator"]["Generation"]["Agents"]["CSLearner"]


# ----------------------------------------------------------------

def getCurrentAlgorithmMaxSize():
    size = 0
    if isCSLearner():
        size += getHeuristicExtra("6")["CS-Propose"]["Max"]
    elif isRBLearner():
        size += getHeuristicExtra("6")["RB-Broadcast"]["Max"]
    size += getHeuristicExtra("6")["Receive"]["Max"]
    return size
