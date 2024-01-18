#
#   Upper Confidence Bounds
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

import numpy
import random

from services.Learning.Policies.Policy import Policy
import configs.Configs as Configs

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class UCB(Policy):

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    # table with the number of times that we select an action on a specific state
    _log_table = None
    _size = None
    _conversion = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, action_space_size):
        super().__init__()
        self._log_table = numpy.zeros((0, action_space_size))
        self._size = action_space_size
        self._conversion = {}

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def isUCB(self):
        return True

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    ##################################################################################################################################
    #
    #   LOGIC
    #
    ##################################################################################################################################

    def runPolicy(self, input):

        # ------------------
        # input
        # ------------------
        state = input["state"]
        actions = input["actions"]
        knowledge = input["knowledge"]

        # ----------------------------------------------
        # get the number of times an action was selected
        # ----------------------------------------------
        if not state.getID() in self._conversion:
            self._log_table = numpy.append(
                self._log_table, [numpy.zeros(self._size)], axis=0)
            self._conversion[state.getID()] = len(self._conversion)-1

        # ------------------
        # decide action
        # ------------------
        action = self.runUCB(state, actions, knowledge)

        # ------------------
        # updates
        # ------------------
        self._log_table[self._conversion[state.getID()]][action.getID()] += 1
        #    state, action, self._log_table.getQTable1StateActionValue(state, action)+1)

        return action, {}

    ##################################################################################################################################
    #
    #   AUXILIAR
    #
    ##################################################################################################################################

    def runUCB(self, state, actions, knowledge_base):

        # ------------------
        # apply algorithm
        # ------------------
        max_upper_bound = None
        possible_actions = []
        for action in actions:
            if (self._log_table[self._conversion[state.getID()]][action.getID()] > 0):
                average_reward = knowledge_base.getStateActionValue(
                    state, action)
                delta_i = numpy.sqrt((numpy.log(sum(
                    self._log_table[self._conversion[state.getID()]]))) / self._log_table[self._conversion[state.getID()]][action.getID()])
                upper_bound = average_reward + Configs.getExplorationAlgorithmHyperparameters(
                    "UCB", "exploration_factor")*delta_i
            else:
                upper_bound = 1e400
            if max_upper_bound == None or upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                possible_actions = [action]
            elif upper_bound == max_upper_bound:
                possible_actions += [action]
        return random.choice(possible_actions)
