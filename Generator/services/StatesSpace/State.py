#
#   This file represents the State
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

import copy

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class STATE:

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    # Create the state
    def __init__(self, algorithm):
        self._algorithm = algorithm
        self._id = None
        self._total_number_of_actions = None

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getAlgorithm(self):
        return self._algorithm

    # ----------------------------------------------------------------

    def getFeatures(self):
        algorithm = self._algorithm.getSortedContent()
        features = []
        for action in algorithm:
            local = [0] * self._total_number_of_actions
            if action != -1:
                local[action.getID()] = 1
            features += local
        return features

    # ----------------------------------------------------------------

    def getNumberOfFeatures(self):
        return len(self.getFeatures())

    # ----------------------------------------------------------------

    def getCopy(self):
        return copy.deepcopy(self)

    # ----------------------------------------------------------------

    def getID(self):
        return self._id

    # ----------------------------------------------------------------

    def getTotalReward(self):
        """Get the algorithm total reward

        Returns:
            int: algorithm total reward
        """
        total_reward = 0
        for event in self.getAlgorithm().getEvents():
            total_reward += event.getTotalReward()
        return total_reward

    # # ----------------------------------------------------------------

    # def addAction(self, action):
    #     """Add action to the current state

    #     Args:
    #         action (object): action to be added
    #     """
    #     return self.getAlgorithm().addAction(action)

    # # ----------------------------------------------------------------

    # def removeLastAction(self):
    #     """Remove last action
    #     """
    #     self.getAlgorithm().removeLastAction()

    # ----------------------------------------------------------------

    # def isOnInitEvent(self):
    #     """Check if it the current event os the Init event

    #     Returns:
    #         boolean: True if it is; False if is not
    #     """
    #     return not self.getAlgorithm().isInitEventComplete()

    # ----------------------------------------------------------------

# {    def isOnLastEvent(self):
#         """Check if it the current event is the Receive event

#         Returns:
#             boolean: True if it is; False if is not
#         """
#         return self.getAlgorithm().isOnLastEvent()}

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def setID(self, value):
        """Set the ID of the state

        Args:
            value (int): ID of the state
        """
        self._id = value

    # ----------------------------------------------------------------

    def setTotalNumberOfActions(self, value):
        self._total_number_of_actions = value

    ##################################################################################################################################
    #
    #   LOGIC
    #
    ##################################################################################################################################

    def __eq__(self, state):
        """Compare if the states are equal

        Args:
            state (object): object of type state

        Returns:
            boolean: True if the states are equal; False if not
        """
        return self.getAlgorithm() == state.getAlgorithm()
