#
#   Reliable broadcast actions space
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.ActionsSpace.ActionsSpace import ActionsSpace
from services.ActionsSpace.Actions.Message.Type.Type import TYPE
from services.ActionsSpace.Actions.Message.Message import MESSAGE
#
import inputs.GenerationInputs as GenerationInputs
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class RBActionsSpace(ActionsSpace):

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        """Constructor
        """
        super().__init__(self.buildActionSpace())

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def buildActionSpace(self):
        """Get the actions space for the Consensus problem

        Returns:
            list: list with the actions
        """

        actions = []
        actions += self.createAllSTOPActions(
            [self.getTrueCondition(MESSAGE())], MESSAGE())
        for type_value in range(GenerationInputs.getMaxNumberOfMessageTypes()):
            actions += self.buildActionBasedOnMessage(
                MESSAGE("msg", TYPE(type_value)))

        return actions

    # ----------------------------------------------------------------

    def buildActionBasedOnMessage(self, message):

        # # * get conditions
        conditions = self.createAllThresholdConditions(
            message, ["1", "F+1", "(N+F)/2", "N-F"])
        tautologies = [self.getTrueCondition(MESSAGE())]
        conditions += tautologies

        # # * create all actions
        actions = self.createAllSENDActions(conditions, message)
        actions += self.createAllDELIVERActions(
            conditions, MESSAGE("msg", None))

        return actions
