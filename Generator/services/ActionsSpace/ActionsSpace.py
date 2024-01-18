#
#   Actions space
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.ActionsSpace.Actions.Action import ACTION
from services.ActionsSpace.Actions.Logic.Deliver import DELIVER
from services.ActionsSpace.Actions.Logic.Send_A import SEND_A
from services.ActionsSpace.Actions.Logic.Send_N import SEND_N
from services.ActionsSpace.Actions.Logic.Send_M import SEND_M
from services.ActionsSpace.Actions.Logic.Stop import STOP
from services.ActionsSpace.Actions.Condition.IsTrue import TRUE
from services.ActionsSpace.Actions.Condition.Threshold import THRESHOLD
from copy import deepcopy
#
import utils.Logger as Logger
import utils.Utils as Utils
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class ActionsSpace:

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

    def __init__(self, actions):
        """Constructor

        Args:
            actions (list): list with all the actions
        """
        self._actions = []
        self.setActions(actions)

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    # Generate the actions
    def setActions(self, actions):
        """Store the actions

        Args:
            actions (list): list with all the action to be stored
        """
        for action in actions:
            self.addAction(action)

    # ----------------------------------------------------------------

    # Add an action
    def addAction(self, action):
        """Add a new action to the action space

        Args:
            action (object): action object to be added
        """
        action_ID = len(self.getActions())
        action.setID(action_ID)
        self._actions += [action]

    ##################################################################################################################################
    #
    #   LOGIC
    #
    ##################################################################################################################################

    def createAllDECIDEActions(self, receive_conditions, message):
        """Create all DECIDE actions

        Args:
            receive_conditions (list): list of condition objects

        Returns:
            list: list of action objects
        """
        actions = []
        for receive_condition in receive_conditions:
            actions += [self.getDECIDEAction(message,
                                             receive_condition)]
        return actions

    # ----------------------------------------------------------------

    def createAllPROPOSEActions(self, receive_conditions, message):
        """Create all Propose actions

        Args:
            receive_conditions (list): list of condition objects

        Returns:
            list: list of action objects
        """
        actions = []
        for receive_condition in receive_conditions:
            actions += [self.getPROPOSEAction(message,
                                              receive_condition)]
        return actions

    # ----------------------------------------------------------------

    def createAllSEND_TO_COORDActions(self, receive_conditions, message):
        """Create all Send to coordinator actions

        Args:
            receive_conditions (list): list of condition objects

        Returns:
            list: list of action objects
        """
        actions = []
        for receive_condition in receive_conditions:
            actions += [self.getSEND_TO_COORDAction(
                message.getCopy(), receive_condition)]
        return actions

    # ----------------------------------------------------------------

    def createAllSENDActions(self, receive_conditions, message):
        actions = []
        for receive_condition in receive_conditions:
            actions += [self.getSEND_AAction(message.getCopy(),
                                             receive_condition)]
            actions += [self.getSEND_NAction(message.getCopy(),
                                             receive_condition)]
            actions += [self.getSEND_MAction(message.getCopy(),
                                             receive_condition)]
        return actions

    # ----------------------------------------------------------------

    def createAllDELIVERActions(self, received_conditions, message):
        actions = []
        for receive_condition in received_conditions:
            actions += [self.getDELIVERAction(message.getCopy(),
                                              receive_condition)]
        return actions

    # ----------------------------------------------------------------

    def createAllSET_ESTIMATEActions(self, conditions, message):
        action = []
        for condition in conditions:
            action += [self.getSET_ESTIMATEAction(
                message, condition)]
        return action

    # ----------------------------------------------------------------

    def createAllSTOPActions(self, conditions, message):
        action = []
        for condition in conditions:
            action += [self.getSTOPAction(message, condition)]
        return action

    # ----------------------------------------------------------------

    def createAllThresholdConditions(self, message, thresholds):

        conditions = []

        # get the threshold conditions
        thresholds_conditions = []
        for threshold in thresholds:
            thresholds_conditions += [threshold]

        # add the defined expressions
        for expression in thresholds_conditions:
            conditions += [self.getThresholdCondition(
                expression, message.getCopy())]

        return conditions

    # ----------------------------------------------------------------

    def createAllIsFromCoordinatorConditions(self, message):
        actions = []
        actions += [self.getIsFromCoordinatorCondition(
            message.getCopy())]
        return actions

    # ----------------------------------------------------------------

    def createImCoordinatorCondition(self, message):
        actions = []
        actions += [self.getImCoordinatorCondition(message)]
        return actions

    # ----------------------------------------------------------------

    def createCoordinatorIsFaultyCondition(self, message):
        actions = []
        actions += [self.getCoordinatorIsFaultyCondition(message)]
        return actions

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getActionIndex(self, action):
        for i in range(len(self._actions)):
            if(self._actions[i] == action):
                return i
        return None

    # ----------------------------------------------------------------

    # get actions
    def getActions(self):
        return self._actions

    # ----------------------------------------------------------------

    # Get actions size
    def getSize(self):
        return len(self._actions)

    # ----------------------------------------------------------------

    # get action by index
    def getActionByIndex(self, index):
        return self._actions[index]

    # ----------------------------------------------------------------

    # get action by index
    def getCopyOfActionByIndex(self, index):
        return deepcopy(self._actions[index])

    # ----------------------------------------------------------------

    # get stop action
    def getSTOPAction(self, message, receive_condition):
        return ACTION(STOP(message), receive_condition)

    # ----------------------------------------------------------------

    # get send action
    def getSEND_AAction(self, message, receive_condition):
        return ACTION(SEND_A(message), receive_condition)

    # ----------------------------------------------------------------

    # get send action
    def getSEND_MAction(self, message, receive_condition):
        return ACTION(SEND_M(message), receive_condition)

    # ----------------------------------------------------------------

    # get send action
    def getSEND_NAction(self, message, receive_condition):
        return ACTION(SEND_N(message), receive_condition)

    # ----------------------------------------------------------------

    # get deliver action
    def getDELIVERAction(self, message, received_condition):
        return ACTION(DELIVER(message), received_condition)

    # ----------------------------------------------------------------

    def getThresholdCondition(self, value, message_object):
        return THRESHOLD(value, message_object)

    # ----------------------------------------------------------------

    def getTrueCondition(self, message):
        return TRUE(message)

    # ----------------------------------------------------------------

    def getActionSpace(self):
        actions_data = []
        for action in self._actions:
            actions_data.append([action.getID(), action.getLogic().getLabel(
            ), action.getCondition().getLabel(), action.getReward()])
        actions_data = sorted(actions_data.copy(), key=self.localSort)
        return Utils.getTable(["ID", "Logic", "Condition", "Reward"], actions_data)

    ##################################################################################################################################
    #
    #   AUXILIARY
    #
    ##################################################################################################################################

    def printActionSpace(self):
        actions_data = []
        for action in self._actions:
            actions_data.append([action.getID(), action.getLogic().getLabel(
            ), action.getCondition().getLabel(), action.getReward()])
        actions_data = sorted(actions_data.copy(), key=self.localSort)
        Logger.printTable(["ID", "Logic", "Condition", "Reward"], actions_data)
        
    def localSort(self, element):
        return element[0]
