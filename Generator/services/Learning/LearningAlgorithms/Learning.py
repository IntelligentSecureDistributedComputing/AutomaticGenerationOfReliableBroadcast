
#
#   QLearning
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

# classes
from services.Learning.Policies.EpsilonGreedy import EpsilonGreedy
from services.Learning.Policies.UCB import UCB
from services.Learning.Policies.Greedy import Greedy
from services.Learning.Policies.Random import Random
# auxiliar
import inputs.GenerationInputs as GenerationInputs
import configs.Configs as Configs
import utils.GlobalVariables.TextVariables as Vars


##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################

class Learning:

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, knowledge_base, actions_space_object):
        """Constructor

        Args:
            knowledge_base (object): knowledge base of the learning process
            actions_space_object (object): action space object to be used by the learning process
        """
        self._knowledge_base = knowledge_base
        self._optimal_policy = Greedy()
        if Configs.runExplorationAlgorithm(Vars.UCB):
                self._policy = UCB(actions_space_object.getSize())
        elif Configs.runExplorationAlgorithm(Vars.EPSILON_GREEDY):
                self._policy = EpsilonGreedy()
        elif Configs.runExplorationAlgorithm(Vars.RANDOM):
                self._policy = Random()
        elif Configs.runExplorationAlgorithm(Vars.GREEDY):
            self._policy = Greedy()

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getAction(self, state, actions, optimal_action=False):
        """Select an allowed action from the current state

        Args:
            state (object): current state
            actions (list): list of allowed action on the current state
            optimal_action (bool, optional): flag that defines if it must be selected the optimal action. Defaults to False.

        Returns:
            action_selected, new_state, generation_information (object,object,json): the action selected, the new state with the action 
                                                                                     selected and info about the selection process
        """

        # store state
        self._knowledge_base.addNewState(state)

        # action
        if optimal_action:
            action_selected, generation_information = self._optimal_policy.runPolicy({
                "state": state,
                "actions": actions,
                "knowledge": self._knowledge_base,
            })
        else:
            action_selected, generation_information = self.getActionByPolicy(
                state, actions)

        # new state
        new_state = state.getCopy()

        # reward
        reward = new_state.getAlgorithm().addAction(action_selected)

        # store new state
        self._knowledge_base.addNewState(new_state)
        # ---------------------
        # regret
        # ---------------------
        regret = self.getRegret(state, actions, action_selected)

        # ---------------------
        # score
        # ---------------------
        score = self._knowledge_base.getStateActionValue(
            state, action_selected)

        # ----------------
        # extra info
        # ----------------
        generation_information["reward"] = reward
        generation_information["regret"] = regret
        generation_information["score"] = score

        return action_selected, new_state, generation_information

    # ----------------------------------------------------------------

    def getBonusReward(self, is_correct):
        """Get the bonus reward, based on if the algorithm is correct or not

        Args:
            is_correct (bool): defines if the algorithm is correct or not

        Returns:
            number: reward to be given to the learner agent
        """

        # reward
        if is_correct == None:
            return 0
        elif is_correct:
            return GenerationInputs.getBonusReward("Correct")
        else:
            return GenerationInputs.getBonusReward("Incorrect")

    # ----------------------------------------------------------------

    def getActionByPolicy(self, state, actions):
        """Select and action based on the policy being used

        Args:
            state (object): current state
            actions (list): list of allowed action on the current state

        Returns:
            action, generation_information (object, json): action selected and info about the selection process
        """

        inputs = {
            "state": state,
            "actions": actions,
            "knowledge": self._knowledge_base,
        }

        action_selected, generation_information = self._policy.runPolicy(
            inputs)

        return action_selected, generation_information

    # ----------------------------------------------------------------

    def getAllActions(self):
        """Get all actions

        Returns:
            list: list with action objects
        """
        return self._knowledge_base.getAllActions()

    # ----------------------------------------------------------------

    def getRegret(self, state, actions, action_selected):
        """Get action selection regret

        Args:
            state (object): current state
            actions (list): list of allowed action on the current state
            action_selected (object): action selected

        Returns:
            number: value of the regret
        """
        return self._knowledge_base.getBestActionValue(state, actions) - self._knowledge_base.getStateActionValue(state, action_selected)

    # ----------------------------------------------------------------

    def getTotalNumberOfStatesFound(self):
        """Get total number of explored states

        Returns:
            int: number of explored states
        """
        return self._knowledge_base.getNumberOfStates()

    # ----------------------------------------------------------------

    def isQLearning(self):
        return False

    # ----------------------------------------------------------------

    def isDeepQLearning(self):
        return False

    # ----------------------------------------------------------------

    def isMonteCarlo(self):
        return False

    # ----------------------------------------------------------------

    def isREINFORCE(self):
        return False

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def updatePolicyData(self):
        """Update the policy data (if needed)
        """
        self._policy.updatePolicyData()
