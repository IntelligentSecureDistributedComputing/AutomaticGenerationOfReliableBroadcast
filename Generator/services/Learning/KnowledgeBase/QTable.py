
#
#   QTable
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.Learning.KnowledgeBase.KnowledgeBase import KnowledgeBase
#
import numpy
import utils.GlobalVariables.TextVariables as Vars
import configs.Configs as Configs
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class QTable(KnowledgeBase):

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, actions_space_object):
        """Constructor

        Args:
            actions_space_object (object): action space to be used by the learning process
        """
        super().__init__(actions_space_object)
        self._qtable = self.createTable(
            self._states_space.getSize(), self._actions_space.getSize())
        if Configs.runQLearningExtra(Vars.DOUBLE_QLEARNING):
            self._qtable2 = self.createTable(
                self._states_space.getSize(), self._actions_space.getSize())

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def createTable(self, state_space_size, action_space_size):
        """Create a Qtable

        Args:
            state_space_size (object): state space object
            action_space_size (_type_): action state object

        Returns:
            list: matrix representing the QTable
        """
        return numpy.zeros((state_space_size, action_space_size))

    # ----------------------------------------------------------------

    def addNewState(self, state):
        """Add a new state to the QTable

        Args:
            state (object): state object
        """
        if super().addNewState(state):
            self._qtable = numpy.append(
                self._qtable, [numpy.zeros(self._actions_space.getSize())], axis=0)
            if Configs.runQLearningExtra(Vars.DOUBLE_QLEARNING):
                self._qtable2 = numpy.append(
                    self._qtable2, [numpy.zeros(self._actions_space.getSize())], axis=0)

    # ----------------------------------------------------------------

    def updateQTable1StateActionValue(self, state, action, value):
        """Update QTable 1

        Args:
            state (object): current state
            action (object): selected action
            value (number): new value of the action on the state
        """
        state_index = self._states_space.getStateIndex(state)
        action_index = self._actions_space.getActionIndex(action)
        self._qtable[state_index][action_index] = value

    # ----------------------------------------------------------------

    def updateQTable2StateActionValue(self, state, action, value):
        """Update QTable 2

        Args:
            state (object): current state
            action (object): selected action
            value (number): new value of the action on the state
        """
        state_index = self._states_space.getStateIndex(state)
        action_index = self._actions_space.getActionIndex(action)
        self._qtable2[state_index][action_index] = value

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getQTable2(self):
        """Get QTable 2

        Returns:
            list: matrix of QTable2
        """
        return self._qtable2

    # ----------------------------------------------------------------

    def getQTable1(self):
        """Get QTable 1

        Returns:
            list: matrix of QTable1
        """
        return self._qtable

    # ----------------------------------------------------------------

    def getQTable1StateActionValue(self, state, action):
        """Get QTable 1 value of action in a state

        Args:
            state (object): current state
            action (object): selected action

        Returns:
            number: value of the action on a state
        """
        state_index = self._states_space.getStateIndex(state)
        action_index = self._actions_space.getActionIndex(action)
        return self._qtable[state_index][action_index]

    # ----------------------------------------------------------------

    def getQTable2StateActionValue(self, state, action):
        """Get QTable 2 value of action in a state

        Args:
            state (object): current state
            action (object): selected action

        Returns:
            number: value of the action on a state
        """
        if Configs.runQLearningExtra(Vars.DOUBLE_QLEARNING):
            state_index = self._states_space.getStateIndex(state)
            action_index = self._actions_space.getActionIndex(action)
            return self._qtable2[state_index][action_index]
        else:
            return 0

    # ----------------------------------------------------------------

    def getQTable1StateValues(self, state):
        """Get QTable1 values of a state

        Args:
            state (object): current state

        Returns:
            list: list with all values from a state
        """
        state_index = self._states_space.getStateIndex(state)
        return self._qtable[state_index]

    # ----------------------------------------------------------------

    def getQTable2StateValues(self, state):
        """Get QTable2 values of a state

        Args:
            state (object): current state

        Returns:
            list: list with all values from a state
        """
        if Configs.runQLearningExtra(Vars.DOUBLE_QLEARNING):
            state_index = self._states_space.getStateIndex(state)
            return self._qtable2[state_index]
        else:
            return numpy.zeros(self._actions_space.getSize())

    # ----------------------------------------------------------------

    def getQTable1BestActionValue(self, state, actions):
        """Get QTable1 best action, from the allowed actions, in a state

        Args:
            state (object): current state
            actions (list): allowed actions for the state

        Returns:
            object: action object representing the best action in the state
        """
        state_values = self.getQTable1StateValues(state)
        highest_index = None
        for action in actions:
            if(highest_index == None or state_values[highest_index] < state_values[self._actions_space.getActionIndex(action)]):
                highest_index = self._actions_space.getActionIndex(action)
        return state_values[highest_index]

    # ----------------------------------------------------------------

    def getQTable2BestActionValue(self, state, actions):
        """Get QTable2 best action, from the allowed actions, in a state

        Args:
            state (object): current state
            actions (list): allowed actions for the state

        Returns:
            object: action object representing the best action in the state
        """
        state_values = self.getQTable2StateValues(state)
        highest_index = None
        for action in actions:
            if(highest_index == None or state_values[highest_index] < state_values[self._actions_space.getActionIndex(action)]):
                highest_index = self._actions_space.getActionIndex(action)
        return state_values[highest_index]

    # ----------------------------------------------------------------

    def getStateValues(self, state):
        """Get all values from a state

        Args:
            state (object): current state

        Returns:
            list: list with all the values form the state
        """
        return self.getQTable1StateValues(state) + self.getQTable2StateValues(state)

    # ----------------------------------------------------------------

    def getStateActionValue(self, state, action):
        """Get the value of an action from state

        Args:
            state (object): current state
            action (object): selected action

        Returns:
            number: value of the action in the state
        """
        return self.getQTable1StateActionValue(state, action) + self.getQTable2StateActionValue(state, action)

    ##################################################################################################################################
    #
    #   AUXILIAR
    #
    ##################################################################################################################################
