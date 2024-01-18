#
#   This file represents the Result function
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

import utils.Utils as Utils
import utils.Logger as Logger
from utils.Parameters.ProcessInfo import ProcessInfo
from services.StatesSpace.RBState import RBSTATE

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class GenerationProcessInfo(ProcessInfo):

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    _runtime_reward = None

    _final_reward = None

    _states = None

    _regret = None

    _score = None

    _epsilon = None

    _number_of_blocked_states = None

    _total_number_of_states_discovered = None

    _apply_heuristics_time = None

    _selecting_action_time = None

    _update_knowledge_base_time = None

    _validation_extra_time = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        super().__init__()
        self._states = []
        self.setRegret(0)
        self.setScore(0)
        self.setEpsilon(-1)
        self.setTotalNumberOfStatesFound(0)
        self._apply_heuristics_time = 0
        self._selecting_action_time = 0
        self._update_knowledge_base_time = 0
        self._validation_extra_time = 0
        self._final_reward = 0
        self._runtime_reward = 0

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getState(self):
        return self.getCurrentState()

    # ----------------------------------------------------------------

    def getStates(self):
        return self._states

    # ----------------------------------------------------------------

    def getCurrentState(self):
        return self._states[-1]

    # ----------------------------------------------------------------

    def getAlgorithm(self):
        return self.getState().getAlgorithm()

    # ----------------------------------------------------------------

    def getRegret(self):
        return self._regret

    # ----------------------------------------------------------------

    def getScore(self):
        return self._score

    # ----------------------------------------------------------------

    def getEpsilon(self):
        return self._epsilon

    # ----------------------------------------------------------------

    def getTotalNumberOfBlockedStates(self):
        return self._number_of_blocked_states

    # ----------------------------------------------------------------

    def getTotalNumberOfStatesFound(self):
        return self._total_number_of_states_discovered

    # ----------------------------------------------------------------

    def getNumberOfStatesExplored(self):
        return len(self._states)

    # ----------------------------------------------------------------

    def getActionsAndHeuristicsTime(self):
        return self._apply_heuristics_time

    # ----------------------------------------------------------------

    def getSelectActionTime(self):
        return self._selecting_action_time

    # ----------------------------------------------------------------

    def getUpdateKnowledgeBaseTime(self):
        return self._update_knowledge_base_time

    # ----------------------------------------------------------------

    def getValidationAndExtraTime(self):
        return self._validation_extra_time

    # ----------------------------------------------------------------

    def getRuntimeReward(self):
        return self._runtime_reward

    # ----------------------------------------------------------------

    def getFinalReward(self):
        return self._final_reward

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def addState(self, state):
        self._states += [state]

    # ----------------------------------------------------------------

    def setRegret(self, regret):
        self._regret = regret

    # ----------------------------------------------------------------

    def setScore(self, score):
        self._score = score

    # ----------------------------------------------------------------

    def updateRegret(self, regret):
        self._regret += regret

    # ----------------------------------------------------------------

    def updateScore(self, score):
        self._score += score

    # ----------------------------------------------------------------

    def setNumberOfBlockedStates(self, value):
        self._number_of_blocked_states = value

    # ----------------------------------------------------------------

    def setTotalNumberOfStatesFound(self, value):
        self._total_number_of_states_discovered = value

    # ----------------------------------------------------------------

    def setEpsilon(self, epsilon):
        self._epsilon = epsilon

    # ----------------------------------------------------------------

    def addActionsAndHeuristicsTime(self, value):
        self._apply_heuristics_time += value

    # ----------------------------------------------------------------

    def addSelectActionTime(self, value):
        self._selecting_action_time += value

    # ----------------------------------------------------------------

    def addUpdateKnowledgeBaseTime(self, value):
        self._update_knowledge_base_time += value

    # ----------------------------------------------------------------

    def addValidationAndExtraTime(self, value):
        self._validation_extra_time += value

    # ----------------------------------------------------------------

    def addRuntimeReward(self, value):
        self._runtime_reward += value

    # ----------------------------------------------------------------

    def setRuntimeReward(self, value):
        self._runtime_reward = value

    # ----------------------------------------------------------------

    def addFinalReward(self, value):
        self._final_reward += value

    ##################################################################################################################################
    #
    #   AUXILIAR
    #
    ##################################################################################################################################

    def printGenerationProcessInfo(self):
        Logger.logInfoMessage("=== Generation Process Info")
        Logger.logInfoMessage(
            "Number of explored states: "+str(self.getNumberOfStatesExplored()))
        super().printProcessInfo()
        Logger.logInfoMessage("Runtime reward: " +
                              str(self.getRuntimeReward()))
        Logger.logInfoMessage("Final reward: " +
                              str(self.getFinalReward()))
        Logger.logInfoMessage("Regret: " + str(self.getRegret()))
        Logger.logInfoMessage("Score: " + str(self.getScore()))
        Logger.logInfoMessage("Epsilon: " + str(self.getEpsilon()))
        Logger.logInfoMessage("===\n")
