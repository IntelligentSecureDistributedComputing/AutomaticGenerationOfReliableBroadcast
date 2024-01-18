#
#   This file represents the Result function
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.Inputs.RuntimeInputs import RuntimeInputs
#
import utils.GlobalVariables.TextVariables as TextVariables
import services.Promela.Definitions.RBDefinitions as RBDefinitions
import utils.Utils as Utils
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class RBInputs(RuntimeInputs):

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        super().__init__()

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getLogicPromela(self, promela_condition, logic):
        if logic["name"] == "Deliver":
            return RBDefinitions.getPromelaDeliver(promela_condition)
        elif logic["name"] == "SendAll":
            return RBDefinitions.getPromelaSendAll(promela_condition, logic)
        elif logic["name"] == "SendNeighbors":
            return RBDefinitions.getPromelaSendNeighbors(promela_condition, logic)
        elif logic["name"] == "SendMyself":
            return RBDefinitions.getPromelaSendMyself(promela_condition, logic)
        elif logic["name"] == "Stop":
            return RBDefinitions.getPromelaStop()

    # ----------------------------------------------------------------

    def getConditionPromela(self, condition):
        if condition["name"] == "True":
            return RBDefinitions.getPromelaEmptyCondition()
        else:
            return RBDefinitions.getPromelaThresholdCondition(str(Utils.evaluateExpression(
                str(condition["name"]), {"F": self.getF(), "N": self.getN()})), condition["message"]["message_type"])

    # ----------------------------------------------------------------

    def getTextAlgorithm(self):
        return super().getPlainText(self.getJsonAlgorithm(),
                                    "RB-Broadcast", "Receive")
