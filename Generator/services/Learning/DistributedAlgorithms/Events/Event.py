#
#   This file represents the State
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

from services.ActionsSpace.Actions.Action import ACTION

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class Event:

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    # Create the state
    def __init__(self, event, name, reward):
        """Constructor

        Args:
            event (list): list of actions
            name (string): name of the event
            reward (int): reward of the event
        """
        self._name = name
        self._event = event
        self._reward = reward

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getEvent(self):
        """Get the list of action

        Returns:
            list: list of action on the current event
        """
        return self._event

    # ----------------------------------------------------------------

    def isEmpty(self):
        """Check if the event is not empty

        Returns:
            boolean: returns True if the event is empty and False if is not empty
        """
        return not any(isinstance(action, ACTION) for action in self._event)

    # ----------------------------------------------------------------

    def getLastAction(self):
        """Get the last action of the event

        Returns:
            object: object of type action
        """
        return self.getActionByIndex(-1)

    # ----------------------------------------------------------------

    def getActionByIndex(self, index):
        """Get the action by index

        Args:
            index (int): index of the action to return

        Returns:
            object: object of type action
        """
        return self.getActions()[index]

    # ----------------------------------------------------------------

    def getPROMELAActions(self):
        """Get the actions from the current event in PROMELA

        Returns:
            list: list of actions
        """
        actions = []
        for action in self._event:
            if action != -1:
                actions += [action.getPROMELAText({})]
        return actions

    # ----------------------------------------------------------------

    def getActions(self):
        """Get the action from the current event

        Returns:
            list: list of actions
        """
        actions = []
        for action in self._event:
            if action != -1:
                actions += [action.getCopy()]
        return actions

    # ----------------------------------------------------------------

    def getContent(self):
        """Get the entire event content

        Returns:
            list: list with all the content of the event
        """
        actions = []
        for action in self._event:
            if action == -1:
                actions += [action]
            else:
                actions += [action.getCopy()]
        return actions

    # ----------------------------------------------------------------

    def isComplete(self):
        """Check if the event is completed (if the last action is the STOP action)

        Returns:
            boolean: True if the event is completed; False if is not
        """
        return not self.isEmpty() and self.getLastAction().isSTOPAction()

    # ----------------------------------------------------------------

    def getTotalNumberOfActions(self):
        """Get total number of actions

        Returns:
            int: total number of actions
        """
        return len(self.getActions())

    # ----------------------------------------------------------------

    def getName(self):
        """Return the name of the event

        Returns:
            string: name of the event
        """
        return self._name

    # ----------------------------------------------------------------

    def getTotalReward(self):
        """Get the total reward of the event

        Returns:
            int: total reward of the event
        """
        total_reward = 0
        for action in self._event:
            if isinstance(action, ACTION):
                total_reward += action.getReward()+self._reward
        return total_reward

    # ----------------------------------------------------------------

    def getSortedEventActions(self):
        """Get sorted list of event actions

        Returns:
            list: sorted list of action objects
        """
        return sorted(self.getActions(), key=self.localSort, reverse=True)

    # ----------------------------------------------------------------

    def getSortedEventContent(self):
        """Get sorted list of the event content

        Returns:
            list: sorted list with the event content
        """
        return sorted(self.getContent(), key=self.localSort, reverse=True)

    # ----------------------------------------------------------------

    def getAllMessageTypesSent(self):
        """Get the message types sent by the event

        Args:
            index (int): event index

        Returns:
            list: list with all the types sent on the event
        """
        types = []
        actions = self.getActions()
        for action in actions:
            if(action.isSENDAction() and not action.getType() in types):
                types += [action.getType()]
        return types

    # ----------------------------------------------------------------

    def getMessageTypesSent(self):
        """Get the message types sent by the event

        Args:
            index (int): event index

        Returns:
            list: list with all the types sent on the event
        """
        types = []
        actions = self.getActions()
        for action in actions:
            if(action.isSENDAction() and not action.getType() in types and action.getType().isType()):
                types += [action.getType()]
        return types

    # ----------------------------------------------------------------

    def getSuspectMessageTypesSent(self):
        """Get the message types sent by the event

        Args:
            index (int): event index

        Returns:
            list: list with all the types sent on the event
        """
        types = []
        actions = self.getActions()
        for action in actions:
            if(action.isSENDAction() and not action.getType() in types and action.getType().isSuspectType()):
                types += [action.getType()]
        return types

    # ----------------------------------------------------------------

    def getJsonEvent(self):
        """Get the event in a json format

        Returns:
            json: json object
        """
        event = []
        actions = self.getActions()
        for action in actions:
            event += [action.getJsonAction()]
        return event

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def removeLastAction(self):
        """Remove the last action
        """
        self._event[self.getTotalNumberOfActions()-1] = -1

    # ----------------------------------------------------------------

    def addAction(self, action):
        """Add a new action to the event

        Args:
            action (object): action object to be added
        """
        self._event[self.getTotalNumberOfActions()] = action
        return action.getReward()+self._reward

    ##################################################################################################################################
    #
    #   EXTRA
    #
    ##################################################################################################################################

    def localSort(self, element):
        """Sort function

        Args:
            element (int/object): action object or -1 value

        Returns:
            int: action ID or -1 value
        """
        if isinstance(element, ACTION):
            return element.getID()
        else:
            return element
