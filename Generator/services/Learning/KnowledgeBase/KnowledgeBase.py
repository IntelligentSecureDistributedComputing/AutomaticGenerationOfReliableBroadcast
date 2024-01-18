
#
#   QTable
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

from services.StatesSpace.StatesSpace import StatesSpace
import random

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class KnowledgeBase:

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, actions_space_object):
        self._states_space = StatesSpace()
        self._actions_space = actions_space_object

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def addNewState(self, state):
        """Add a new state to the states space
        Args:
            state (object): state object to be store
        Returns:
            boolean: True if it is a new state is store; False on if not
        """
        if(not self._states_space.stateExists(state)):
            self._states_space.addState(state)
            return True
        else:
            state.setID(self._states_space.getStateID(state))
            return False

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getEventSpace(self):
        """Get the event space object
        Returns:
            object: Event Space object
        """
        return self._event_space

    ##################################################################################################################################
    #
    #   LOGIC
    #
    #   * The possible improvement of storing Nan values for the not allowed actions could work on the QTable,
    #   *    but not on the Artificial Neural Network, so I decided to mantain this code on both QTable and ANN
    #
    ##################################################################################################################################

    def getBestAction(self, state, actions):
        """Get best action from a specific state
        Args:
            state (object): state object
            actions (list): list of action objects
        Returns:
            object: action object
        """
        state_values = self.getStateValues(state)
        highest_index = None
        possible_actions = []
        for action in actions:
            if(highest_index == None or state_values[highest_index] < state_values[self._actions_space.getActionIndex(action)]):
                highest_index = self._actions_space.getActionIndex(action)
                possible_actions = [action]
            elif(state_values[highest_index] == state_values[self._actions_space.getActionIndex(action)]):
                possible_actions += [action]
        return random.choice(possible_actions)

    # ----------------------------------------------------------------

    def getBestActionValue(self, state, actions):
        """Get the value of the best action on a specific state
        Args:
            state (object): state object
            actions (list): list of action objects
        Returns:
            number: value of the best action
        """
        state_values = self.getStateValues(state)
        highest_index = None
        for action in actions:
            if(highest_index == None or state_values[highest_index] < state_values[self._actions_space.getActionIndex(action)]):
                highest_index = self._actions_space.getActionIndex(action)
        return state_values[highest_index]

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getAllActions(self):
        """Get all the action
        Returns:
            list: list with action objects
        """
        return self._actions_space.getActions()

    # ----------------------------------------------------------------

    def getNumberOfStates(self):
        """GEt the total number of states
        Returns:
            number: number of states
        """
        return self._states_space.getSize()

    # ----------------------------------------------------------------

    def getNumberOfActions(self):
        return self._actions_space.getSize()
