#
#   This file represents the Result function
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class RuntimeInputs:

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    _json_algorithm = None

    _ID = None

    _no_failure_mode = False

    _crash_failure_mode = False

    _byzantine_failure_mode = False

    _N = None

    _F = None

    _final_validation = None

    _broadcaster = None

    _processes = None

    _faulty_processes = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        pass

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def isNoFailureMode(self):
        return self._no_failure_mode

    # ----------------------------------------------------------------

    def isCrashFailureMode(self):
        return self._crash_failure_mode

    # ----------------------------------------------------------------

    def isByzantineFailureMode(self):
        return self._byzantine_failure_mode

    # ----------------------------------------------------------------

    def getCurrentFailureModeLabel(self):
        if self.isNoFailureMode():
            return "NO_FAILURE"
        elif self.isCrashFailureMode():
            return "CRASH_FAILURE"
        elif self.isByzantineFailureMode():
            return "BYZANTINE_FAILURE"

    # ----------------------------------------------------------------

    def getN(self):
        return self._N

    # ----------------------------------------------------------------

    def getF(self):
        return self._F

    # ----------------------------------------------------------------

    def isFinalValidation(self):
        return self._final_validation

    # ----------------------------------------------------------------

    def getFaultyProcesses(self):
        return self._faulty_processes

    # ----------------------------------------------------------------

    def getBroadcaster(self):
        return self._broadcaster

    # ----------------------------------------------------------------

    def getJsonAlgorithm(self):
        return self._json_algorithm

    # ----------------------------------------------------------------

    def getID(self):
        return self._ID

    # ----------------------------------------------------------------

    def getAllMessageTypesUsed(self, events_name):
        """Get the highest message type of the event

        Args:
            highest_message_type (int): current highest message types
            json_algorithm (json): algorithm in a json format
            event_name (string): name of the event

        Returns:
            int: highest message types based on an initial message type and on the event being analyses
        """
        message_types = []
        for event_name in events_name:
            message_types += self.getLogicMessageTypesFromEvent(
                event_name)
            message_types += self.getConditionMessageTypesFromEvent(
                event_name)
        # remove duplicates
        final_message_types = []
        for message_type in message_types:
            if message_type not in final_message_types:
                final_message_types += [message_type]
        return final_message_types
    # ----------------------------------------------------------------

    def getEventPromela(self, event_name):
        json_algorithm = self.getJsonAlgorithm()
        event_actions = json_algorithm[event_name]
        promela = []
        for action in event_actions:
            label = ""
            label += self.getLogicPromela(self.getConditionPromela(
                action["condition"]), action["logic"])
            promela += [label]
        return promela

    # ----------------------------------------------------------------

    def getLogicMessageTypesFromEvent(self, event_name):
        json_algorithm = self.getJsonAlgorithm()
        event_actions = json_algorithm[event_name]
        local_message_types = []
        for action in event_actions:
            if not action["logic"]["message"]["message_type"]["status"] == 'None' and \
                not action["logic"]["message"]["message_type"]["value"] == 'None' and \
                action["logic"]["message"]["message_type"] not in \
                    local_message_types:
                local_message_types += [action["logic"]
                                        ["message"]["message_type"]]
        return local_message_types

    # ----------------------------------------------------------------

    def getConditionMessageTypesFromEvent(self, event_name):
        json_algorithm = self.getJsonAlgorithm()
        event_actions = json_algorithm[event_name]
        local_message_types = []
        for action in event_actions:
            if not action["condition"]["message"]["message_type"]["status"] == 'None' and \
                not action["condition"]["message"]["message_type"]["value"] == 'None' and \
                action["condition"]["message"]["message_type"] not in \
                    local_message_types:
                local_message_types += [action["condition"]
                                        ["message"]["message_type"]]
        return local_message_types

    # ----------------------------------------------------------------

    def getHighestMessageTypeUsed(self, events_name):
        message_types_used = self.getAllMessageTypesUsed(events_name)
        highest_message_type = 0
        for message_type in message_types_used:
            if int(message_type["value"]) > int(highest_message_type):
                highest_message_type = message_type["value"]
        return int(highest_message_type)

    # ----------------------------------------------------------------

    def getPlainText(self, algorithm_list, first_event_name, second_event_name):
        plain_text = ""
        plain_text += self.getPlainTextEvent(first_event_name, algorithm_list)
        plain_text += "\n"
        plain_text += self.getPlainTextEvent(second_event_name, algorithm_list)
        return plain_text

    # ----------------------------------------------------------------

    def getPlainTextEvent(self, event_name, algorithm_list):
        plain_text = ""
        plain_text += "when "+event_name+" do:\n"
        for action in algorithm_list[event_name]:
            plain_text += "- "+action["logic"]["name"]+" <" +\
                str(action["logic"]["message"]["value"])+","+str(action["logic"]["message"]["message_type"]["value"])+","+action["logic"]["message"]["message_type"]["status"]+"> if "+action["condition"]["name"]+" <" +\
                str(action["condition"]["message"]["value"])+","+str(action["condition"]["message"]
                                                                     ["message_type"]["value"])+","+action["condition"]["message"]["message_type"]["status"]+">\n"
        return plain_text

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def setCurrentFailureMode(self, no_failure_mode, crash_failure_mode, byzantine_failure_mode):
        self.setNoFailureMode(no_failure_mode)
        self.setCrashFailureMode(crash_failure_mode)
        self.setByzantineFailureMode(byzantine_failure_mode)

    # ----------------------------------------------------------------

    def setNoFailureMode(self, value):
        self._no_failure_mode = value

    # ----------------------------------------------------------------

    def setCrashFailureMode(self, value):
        self._crash_failure_mode = value

    # ----------------------------------------------------------------

    def setByzantineFailureMode(self, value):
        self._byzantine_failure_mode = value

    # ----------------------------------------------------------------

    def setN(self, N):
        self._N = N

    # ----------------------------------------------------------------

    def setF(self, F):
        self._F = F

    # ----------------------------------------------------------------

    def setFinalValidation(self, value):
        self._final_validation = value

    # ----------------------------------------------------------------

    def setBroadcaster(self, value):
        self._broadcaster = value

    # ----------------------------------------------------------------

    def setFaultyProcesses(self, value):
        self._faulty_processes = value

    # ----------------------------------------------------------------

    def setTextAlgorithm(self, text_algorithm):
        self._text_algorithm = text_algorithm

    # ----------------------------------------------------------------

    def setJsonAlgorithm(self, json_algorithm):
        self._json_algorithm = json_algorithm

    # ----------------------------------------------------------------

    def setID(self, value):
        self._ID = value
