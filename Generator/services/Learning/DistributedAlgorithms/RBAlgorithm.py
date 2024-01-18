#
#   This file represents the algorithm generated
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

from services.Learning.DistributedAlgorithms.Algorithm import Algorithm
import inputs.GenerationInputs as GenerationInputs
from services.Learning.DistributedAlgorithms.Events.Event import Event
import utils.GlobalVariables.TextVariables as Vars
import copy

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class RBAlgorithm(Algorithm):

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    BROADCAST_EVENT = 0

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        """Constructor
        """
        broadcast_event = Event(
            [-1]*GenerationInputs.getHeuristicExtra("6")[Vars.BROADCAST_EVENT]["Max"], Vars.BROADCAST_EVENT, GenerationInputs.getEventReward(Vars.BROADCAST_EVENT))
        receive_event = Event(
            [-1]*GenerationInputs.getHeuristicExtra("6")[Vars.RECEIVE_EVENT]["Max"], Vars.RECEIVE_EVENT, GenerationInputs.getEventReward(Vars.RECEIVE_EVENT))
        super().__init__([broadcast_event, receive_event])

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    ##################################################################################################################################
    #
    #   GET
    #
    #################################################################################################################################

    def getCopy(self):
        """Get copy of the current object

        Returns:
            object: RBAlgorithm object
        """
        return copy.deepcopy(self)

    # ----------------------------------------------------------------

    def getInitEventIndex(self):
        return self.BROADCAST_EVENT

    ##################################################################################################################################
    #
    #   LOGIC
    #
    ##################################################################################################################################

    def delivers(self):
        """Check if the algorithm contains the action deliver

        Returns:
            boolean: True if the algorithm contains the action Deliver; False if not
        """
        for action in self.getAllActions():
            if action.isDELIVERAction():
                return True
        return False

    # ----------------------------------------------------------------

    def getTextAlgorithm(self, all_content=False):
        """Get the algorithm in a text format

        Returns:
            list: list of strings containing the algorithm
        """
        algorithm_txt = []

        algorithm_txt += ["when RB-Broadcast(m) do:\n"]
        broadcast_event = self.getEventActions(self.BROADCAST_EVENT)
        for action in broadcast_event:
            if not action.isSTOPAction() or all_content:
                algorithm_txt += ["- "+action.getLabel()+"\n"]
        algorithm_txt += ["\n"]

        algorithm_txt += ["when receive(<t,m>) do:\n"]
        receive_event = self.getEventActions(self.RECEIVE_EVENT)
        for action in receive_event:
            if not action.isSTOPAction() or all_content:
                algorithm_txt += ["- "+action.getLabel()+"\n"]

        return algorithm_txt
