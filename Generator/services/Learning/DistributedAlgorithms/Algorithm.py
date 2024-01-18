#
#   This file represents the algorithm generated
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.Learning.DistributedAlgorithms.Tolerance import Tolerance
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class Algorithm(Tolerance):

    RECEIVE_EVENT = 1

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, algorithm):
        """Constructor

        Args:
            algorithm (list): list of event objects
        """
        self._algorithm = algorithm

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def addAction(self, action):
        """Add a new action

        Args:
            action (object): object action to be added to the algorithm
        """
        for event in self._algorithm:
            if not event.isComplete():
                return event.addAction(action)

    # ----------------------------------------------------------------

    def removeLastAction(self):
        """Remove the last element of the algorithm
        """
        for event in self._algorithm[::-1]:
            if not event.isEmpty():
                event.removeLastAction()
                return

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getPROMELAEventActions(self, index):
        """Get actions in PROMELA from a specific event

        Args:
            index (int): index of the event

        Returns:
            list: list with the actions of the event
        """
        return self.getEventByIndex(index).getPROMELAActions()

    # ----------------------------------------------------------------

    def getEventActions(self, index):
        """Get action from a specific event

        Args:
            index (int): index of the event

        Returns:
            list: list with the actions of the event
        """
        return self.getEventByIndex(index).getActions()

    # ----------------------------------------------------------------

    def getEventContent(self, index):
        """Get the entire event

        Returns:
            list: list with all the content of the event
        """
        return self.getEventByIndex(index).getContent()

    # ----------------------------------------------------------------

    def getEventMessageTypesSent(self, index):
        """Get the message types sent by the event

        Args:
            index (int): event index

        Returns:
            list: list with all the types sent on the event
        """
        return self.getEventByIndex(index).getMessageTypesSent()

    # ----------------------------------------------------------------

    def getEventConditionsMessageTypes(self, index):
        """Get the conditions message type

        Args:
            index (int): index of the event

        Returns:
            list: message types used by the conditions of the event
        """
        types = []
        event_code = self.getEventActions(index)
        for action in event_code:
            conditions = action.getConditions()
            for condition in conditions:
                if(not condition.getMessageType() in types):
                    types += [condition.getMessageType()]
        return types

    # ----------------------------------------------------------------

    def getLastAction(self):
        """Get algorithm last action

        Returns:
            object: object of type action 
        """
        for event in self._algorithm[::-1]:
            if not event.isEmpty():
                return event.getLastAction()

    # ----------------------------------------------------------------

    def getEvents(self):
        """Get the list of event of the algorithm

        Returns:
            list: list of object events
        """
        return self._algorithm

    # ----------------------------------------------------------------

    def getEventByIndex(self, index):
        """Get the list of event of the algorithm

        Returns:
            list: list of object events
        """
        return self._algorithm[index]

    # ----------------------------------------------------------------

    def getAllActions(self):
        """Get all the actions of the algorithm

        Returns:
            list: list of objects of type action
        """
        actions = []
        for event in self._algorithm:
            actions += event.getActions()
        return actions

    # ----------------------------------------------------------------

    def getAllContent(self):
        content = []
        for event in self._algorithm:
            content += event.getContent()
        return content

    # ----------------------------------------------------------------

    def getTotalNumberOfActions(self):
        """Get the total number of actions

        Returns:
            int: total number of actions
        """
        return len(self.getActions())

    # ----------------------------------------------------------------

    def getCurrentEventName(self):
        """Get the ID of the current event

        Returns:
            string: current event ID
        """
        for event in self._algorithm:
            if not event.isComplete():
                return event.getName()

    # ----------------------------------------------------------------

    def getCurrentEventActions(self):
        """Get the ID of the current event

        Returns:
            list: list with the actions of the event
        """
        for event in self._algorithm:
            if not event.isComplete():
                return event.getActions()

    # ----------------------------------------------------------------

    def getCurrentEvent(self):
        """Get the current event object

        Returns:
            object: object with the current event
        """
        for event in self._algorithm:
            if not event.isComplete():
                return event

    # ----------------------------------------------------------------

    def isEmpty(self):
        """Check if the algorithm is empty or not

        Returns:
            boolean: True if the algorithm is empty; False if not
        """
        for event in self._algorithm:
            if not event.isEmpty():
                return False
        return True

    # ----------------------------------------------------------------

    def isCurrentEventTheLastEvent(self):
        """Check if the current event is the last event of the algorithm

        Returns:
            boolean: True if is the last event; False on the contrary
        """
        return self.getCurrentEvent() == self._algorithm[-1]

    # ----------------------------------------------------------------

    def getJsonAlgorithm(self):
        """Get the algorithm in a json format

        Returns:
            json: json object
        """
        json = {}
        for event in self._algorithm:
            json[event.getName()] = event.getJsonEvent()
        return json

    # ----------------------------------------------------------------

    def getEventActions(self, index):
        """Get the rb-broadcast actions

        Returns:
            list: list with the action of the receive event
        """
        return self.getEventByIndex(index).getActions()

    # ----------------------------------------------------------------

    def isOnReceiveEvent(self):
        return not self.getEvents[self.RECEIVE_EVENT].isComplete()

    # ----------------------------------------------------------------

    def getAllMessageTypesSent(self):
        """Get all the message types sent by the algorithm

        Returns:
            list: list with all the message types sent by the algorithm
        """
        types = []
        for event in self._algorithm:
            types += event.getAllMessageTypesSent()
        return types

    # ----------------------------------------------------------------

    def getMessageTypesSent(self):
        """Get all the message types sent by the algorithm

        Returns:
            list: list with all the message types sent by the algorithm
        """
        types = []
        for event in self._algorithm:
            types += event.getMessageTypesSent()
        return types

    # ----------------------------------------------------------------

    def getSuspectMessageTypesSent(self):
        """Get all the message types sent by the algorithm

        Returns:
            list: list with all the message types sent by the algorithm
        """
        types = []
        for event in self._algorithm:
            types += event.getSuspectMessageTypesSent()
        return types

    # ----------------------------------------------------------------

    def getSortedActions(self):
        """Get the algorithm action sorted

        Returns:
            list: list of sorted actions
        """
        sorted_algorithm = []
        for event in self._algorithm:
            sorted_algorithm += event.getSortedEventActions()
        return sorted_algorithm

    # ----------------------------------------------------------------

    def getSortedContent(self):
        """Get the algorithm content sorted

        Returns:
            list: list of sorted content
        """
        sorted_algorithm = []
        sorted_algorithm = []
        for event in self._algorithm:
            sorted_algorithm += event.getSortedEventActions()
        return sorted_algorithm

    # ----------------------------------------------------------------

    def isOnInitEvent(self):
        return self.getCurrentEvent() == self.getEventByIndex(self.getInitEventIndex())

    # ----------------------------------------------------------------

    def getPlainText(self, all_content):
        txt_list_algorithm = self.getTextAlgorithm(all_content)
        plain_txt_algorithm = ""
        for txt in txt_list_algorithm:
            plain_txt_algorithm += txt
        return plain_txt_algorithm

    ##################################################################################################################################
    #
    #   LOGIC
    #
    ##################################################################################################################################

    def finishes(self):
        """Check if the algorithm contains an action with subclass FINISH

        Returns:
            boolean: True if the algorithm contains an action with subclass FINISH; False if not
        """
        return self.delivers() or self.decides()

    # ----------------------------------------------------------------

    def delivers(self):
        """Check if the algorithm contains the action deliver

        Returns:
            boolean: True if the algorithm contains the action Deliver; False if not
        """
        return False

    # ----------------------------------------------------------------

    def decides(self):
        """Check if the algorithm contains the action decide

        Returns:
            boolean: True if the algorithm contains the action Decide; False if not
        """
        return False

    # ----------------------------------------------------------------

    def isComplete(self):
        """Check if the algorithm is completed (all last actions of all event are the STOP action)

        Returns:
            boolean: True if is completed; False if is not
        """
        for event in self._algorithm:
            if not event.isComplete():
                return False
        return True

    # ----------------------------------------------------------------

    # def isInitEventComplete(self):
    #     """Check if the RB-Broadcast event is completed

    #     Returns:
    #         boolean: True if is completed; False if is not
    #     """
    #     return self.getEvent(INIT_EVENT).isComplete()

    # # ----------------------------------------------------------------

    # def isReceiveEventComplete(self):
    #     """Check if the Receive event is completed

    #     Returns:
    #         boolean: True if is completed; False if is not
    #     """
    #     return self.getEvent(RECEIVE_EVENT).isComplete()

    # ----------------------------------------------------------------

    def __eq__(self, algorithm):
        """Check if the algorithms are equal

        Args:
            algorithm (object): object of type algorithm

        Returns:
            boolean: True if the algorithms are equal; False if they are not
        """
        return self.getAllActions() == algorithm.getAllActions()
