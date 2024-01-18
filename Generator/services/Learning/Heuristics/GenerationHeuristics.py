#
#   This file represents the Heuristcs used on generation function
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

import inputs.GenerationInputs as GenerationInputs
#
from utils.Exceptions.GoBack import GOBACK
from utils.Exceptions.EmptyProblem import EMPTY_PROBLEM

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class GenerationHeuristics:

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    # GH9
    _analysed_states = None
    _allowed_actions = None
    # Extra
    _number_of_blocked_states = None
    # GH12
    _current_most_efficient_reward = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    # Constructor
    def __init__(self):
        self._analysed_states = []
        self._allowed_actions = []
        self._number_of_blocked_states = 0

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    ##################################################################################################################################
    #
    #   APPLY HEURISTICS
    #
    ##################################################################################################################################

    def applyHeuristics(self, actions, state):

        # new state to be analysed
        if state not in self._analysed_states:
            # ---------------------------------------
            #  HEURISTCS EXECUTED ONLY ONCE (static)
            # ---------------------------------------

            # add the state and all the allowed actions
            self._analysed_states += [state]
            self._allowed_actions += [actions.copy()]

            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic1(actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic2(actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic3(actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic6(
                actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic4(
                actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic7(
                actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic8(
                actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()
            self.applyHeuristic5(actions, state)
            actions = self._allowed_actions[self._analysed_states.index(
                state)].copy()

        # ------------------------------------
        #  HEURISTCS ALWAYS EXECUTED (dynamic)
        # ------------------------------------
        # this heuristic must be always analysed, because when the agent finds a new most efficient algorithm
        #   some actions can be now blocked
        actions = self._allowed_actions[self._analysed_states.index(
            state)].copy()
        self.applyHeuristic10(actions, state)

        # final update upon the allowed actions to check if now some states and empty
        self.updatePossibleAllowedActions(actions, state)
        actions = self._allowed_actions[self._analysed_states.index(
            state)].copy()

        return actions

    ##################################################################################################################################
    #
    #   HEURISTICS
    #
    ##################################################################################################################################

    def applyHeuristic1(self, actions, state):
        if(GenerationInputs.runHeuristic("1")):
            all_actions = state.getAlgorithm().getAllActions()
            for action in actions:
                if not action.isSTOPAction():  # do not remove the STOP action
                    if action in all_actions:
                        self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic2(self, actions, state):
        if(GenerationInputs.runHeuristic("2")):
            for action in actions:
                # the STOP action cannot be removed
                if not action.isSTOPAction():
                    if not GenerationInputs.getHeuristicExtra("2")[
                            state.getAlgorithm().getCurrentEventName()][action.getName()]:
                        # allow only the defined actions, based on the generations_config.jsonc file
                        self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic3(self, actions, state):
        if(GenerationInputs.runHeuristic("3")):
            for action in actions:
                # the STOP action cannot be removed
                if not action.isSTOPAction():
                    if not GenerationInputs.getHeuristicExtra("3")[
                            state.getAlgorithm().getCurrentEventName()][action.getCondition().getID()]:
                        self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic4(self, actions, state):
        if(GenerationInputs.runHeuristic("4")):
            for action in actions:
                if action.isSENDAction():
                    current_event_actions = state.getAlgorithm().getCurrentEventActions()
                    for selected_action in current_event_actions:
                        if selected_action.isSENDAction() and action.getType() == selected_action.getType() and action.getCondition() == selected_action.getCondition():
                            self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic5(self, actions, state):
        # allow only the defined type
        if(GenerationInputs.runHeuristic("5")):
            if state.getAlgorithm().isOnInitEvent():
                for action in actions:
                    if(action.isSENDAction() and action.getType().getValue() != 0 and action.getType().isType()):
                        self.removeElement(action, state)
                    elif((action.isSENDAction() and action.getType().isSuspectType()) or (action.getCondition().hasMessageType() and action.getCondition().getMessage().getType().isSuspectType())):
                        self.removeElement(action, state)
            else:
                for action in actions:
                    if(action.isSENDAction() and action.getType().getValue() == 0 and action.getType().isType()):
                        self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic6(self, actions, state):
        if(GenerationInputs.runHeuristic("6")):
            event = state.getAlgorithm().getCurrentEvent()
            if event.getTotalNumberOfActions() < GenerationInputs.getHeuristicExtra("6")[str(state.getAlgorithm().getCurrentEventName())]["Min"]-1:
                for action in actions:
                    if action.isSTOPAction():
                        self.removeElement(action, state)
            elif event.getTotalNumberOfActions() == GenerationInputs.getHeuristicExtra("6")[str(state.getAlgorithm().getCurrentEventName())]["Max"]-1:
                for action in actions:
                    if(not action.isSTOPAction()):
                        self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic7(self, actions, state):
        if GenerationInputs.runHeuristic("7"):
            # for the normal types
            types_sent = state.getAlgorithm().getMessageTypesSent()
            for action in actions:
                if action.getCondition().hasMessageType() and action.getCondition().getMessage().getType().isType():
                    # if not messages sent, allow only the type 0 | if any message sent, allow only conditions with that type
                    if len(types_sent) == 0 and not action.getCondition().getMessage().getType().getValue() == 0 or \
                            len(types_sent) > 0 and not action.getCondition().getMessage().getType() in types_sent:
                        self.removeElement(action, state)
            # for the suspect types
            suspect_types_sent = state.getAlgorithm().getSuspectMessageTypesSent()
            for action in actions:
                if action.getCondition().hasMessageType() and action.getCondition().getMessage().getType().isSuspectType():
                    # if not messages sent, allow only the type 0 | if any message sent, allow only conditions with that type
                    if len(types_sent) == 0 and not action.getCondition().getMessage().getType().getValue() == 0 or \
                            len(types_sent) > 0 and not action.getCondition().getMessage().getType() in suspect_types_sent:
                        self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic8(self, actions, state):
        if GenerationInputs.runHeuristic("8") and GenerationInputs.runHeuristic("6"):
            if not state.getAlgorithm().finishes():
                if state.getAlgorithm().isCurrentEventTheLastEvent():
                    for action in actions:
                        if len(state.getAlgorithm().getCurrentEventActions()) == GenerationInputs.getHeuristicExtra("6")[state.getAlgorithm().getCurrentEventName()]["Max"]-2:
                            if(not action.isFINISHAction()):
                                self.removeElement(action, state)
                        elif action.isSTOPAction():
                            self.removeElement(action, state)

    # ----------------------------------------------------------------

    def applyHeuristic10(self, actions, state):
        if GenerationInputs.runHeuristic("10"):
            # block actions that lead to algorithms less efficient than the most efficient correct algorithm, until the moment
            if not self._current_most_efficient_reward == None:
                for action in actions:
                    aux_state = state.getCopy()
                    aux_action = action.getCopy()
                    reward = aux_state.getAlgorithm().addAction(aux_action)
                    if aux_state.getTotalReward() < self._current_most_efficient_reward:
                        self.removeElement(action, state)

    ##################################################################################################################################
    #
    #  AUXILIAR FUNCTION
    #
    ##################################################################################################################################

    def removeElement(self, action, state):
        if action in self._allowed_actions[self._analysed_states.index(state)]:
            self._allowed_actions[self._analysed_states.index(
                state)].remove(action)
            self._number_of_blocked_states += 1

    # ----------------------------------------------------------------

    def applyHeuristic9(self, state, action, validation_result):
        if GenerationInputs.runHeuristic("9"):
            self.removeAllowedActions(state, action, validation_result)

    # ----------------------------------------------------------------

    def removeAllowedActions(self, state, action, validation_result):
        if not validation_result:
            self.removeElement(action, state)
            # * remove the last action from the algorithm
            if len(self._allowed_actions[self._analysed_states.index(state)]) == 0:
                # * if the algorithm is empty, means that we have analysed all possible algorithms
                if state.getAlgorithm().isEmpty():
                    raise EMPTY_PROBLEM
                else:
                    aux_state = state.getCopy()
                    last_action = aux_state.getAlgorithm().getLastAction().getCopy()
                    aux_state.getAlgorithm().removeLastAction()
                    self.removeAllowedActions(aux_state, last_action, False)

    # ----------------------------------------------------------------

    def updatePossibleAllowedActions(self, actions, state):
        # delete action that lead to empty states
        for action in actions:
            aux_state = state.getCopy()
            aux_state.getAlgorithm().addAction(action)
            if aux_state in self._analysed_states and len(self._allowed_actions[self._analysed_states.index(aux_state)]) == 0:
                self.removeElement(action, state)
        # empty state
        if len(self._allowed_actions[self._analysed_states.index(state)].copy()) == 0:
            aux_state = state.getCopy()
            last_action = aux_state.getAlgorithm().getLastAction().getCopy()
            aux_state.getAlgorithm().removeLastAction()
            self.removeAllowedActions(aux_state, last_action, False)
            state.getAlgorithm().removeLastAction()
            raise GOBACK

    # ----------------------------------------------------------------

    def updateMostEfficientCorrectAlgorithmReward(self, reward, isCorrect):
        if isCorrect:
            if self._current_most_efficient_reward == None or self._current_most_efficient_reward < reward:
                self._current_most_efficient_reward = reward

    # ----------------------------------------------------------------

    def getNumberOfBlockedStates(self):
        return self._number_of_blocked_states
