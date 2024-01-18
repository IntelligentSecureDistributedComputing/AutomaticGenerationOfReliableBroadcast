#
#   Reliable Broadcast QTable
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.Learning.LearningAlgorithms.QLearning import QLearning
from services.Learning.Heuristics.GenerationHeuristics import GenerationHeuristics
from utils.Exceptions.GoBack import GOBACK
from utils.Exceptions.End import END
from dotenv import load_dotenv
#
import utils.Logger as Logger
import utils.Utils as Utils
import requests
import inputs.GenerationInputs as GenerationInputs
import utils.GlobalVariables.TextVariables as Vars
import configs.Configs as Configs
import os
load_dotenv()

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class Learner:

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    # Constructor
    def __init__(self, actions_space):
        """Constructor

        Args:
            actions_space (object): action space
        """
        self._heuristics = GenerationHeuristics()
        if Configs.runLearningAlgorithm(Vars.QLEARNING):
            self._learning_process = QLearning(actions_space)

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getTotalNumberOfActions(self):
        """Get total number of actions

        Returns:
            int: total number of actions
        """
        return len(self._learning_process.getAllActions())

    # ----------------------------------------------------------------

    def selectAction(self, state, actions):
        """Select an action from the current state and the allowed actions

        Args:
            state (object): current state
            actions (list): list of allowed actions

        Returns:
            object: action object
        """
        return self._learning_process.getAction(state, actions)

    # ----------------------------------------------------------------

    def selectOptimalAction(self, state, actions):
        """Select the optimal action from the state and the actions available

        Args:
            state (object): current state
            actions (list): list of allowed action on the current state

        Returns:
            action: action object selected
        """
        return self._learning_process.getAction(state, actions, True)

    # ----------------------------------------------------------------

    def getPossibleActions(self, state):
        """Get the possible actions for the current state

        Args:
            state (object): current state

        Returns:
            list: list of action objects
        """
        while True:
            try:
                actions = self.getAllActions()
                possible_actions = self._heuristics.applyHeuristics(
                    actions, state)
                return possible_actions
            except GOBACK:
                continue

    # ----------------------------------------------------------------

    def getAllActions(self):
        """Get all actions available

        Returns:
            list: list with all the action objects available
        """
        return self._learning_process.getAllActions()

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    # * store the generation process data
    def updateEpisodeLearningData(self, episode, state, generation_information):
        """Function that updated the episode object with the information from the current episode

        Args:
            episode (object): current episode object
            state (object): current state
            generation_information (json): json object containing information about the learning algorithms
        """
        episode.getGenerationProcessInfo().addState(state)
        episode.getGenerationProcessInfo().setRuntimeReward(state.getTotalReward())
        episode.getGenerationProcessInfo().updateRegret(
            generation_information["regret"])
        episode.getGenerationProcessInfo().updateScore(
            generation_information["score"])
        if "epsilon" in generation_information:
            episode.getGenerationProcessInfo().setEpsilon(
                generation_information["epsilon"])
        episode.getGenerationProcessInfo().setNumberOfBlockedStates(
            self._heuristics.getNumberOfBlockedStates())
        episode.getGenerationProcessInfo().setTotalNumberOfStatesFound(
            self._learning_process.getTotalNumberOfStatesFound())

    ##################################################################################################################################
    #
    #   GENERATION PROCESS
    #
    ##################################################################################################################################

    def runGenerationProcess(self, episode, optimal_generation_process=False):
        """Run the generation process

        Args:
            episode (object): object episode that contains the information about the episode
            optimal_generation_process (bool, optional): flag that indicates if we want the optimal algorithm. Defaults to False.
        """
        try:

            # ---------------------
            # begin of generation
            # ---------------------
            begin_of_generation = Utils.getTime()

            if optimal_generation_process:
                Logger.logInfoMessage("=== " +
                                      self.getName()+" generating the optimal algorithm...\n")
            else:
                Logger.logInfoMessage("=== " + self.getName() +
                                      " generating the algorithm...\n")

            # ---------------------
            # current state
            # ---------------------
            episode.getGenerationProcessInfo().getState(
            ).setTotalNumberOfActions(self.getTotalNumberOfActions())
            state = episode.getGenerationProcessInfo().getState().getCopy()

            # ---------------------
            # get possible actions
            # ---------------------
            aux = Utils.getTime()
            actions = self.getPossibleActions(state)
            episode.getGenerationProcessInfo().addActionsAndHeuristicsTime(Utils.getTime()-aux)

            for event_index in range(len(episode.getGenerationProcessInfo().getState().getAlgorithm().getEvents())):
                # build each event of the algorithm
                action, generation_information, state, next_state, actions = self.buildEvent(
                    event_index, state, actions, episode, optimal_generation_process)

            # ---------------------
            # end of generation
            # ---------------------
            end_of_generation = Utils.getTime()
            episode.getGenerationProcessInfo().addTime(
                (end_of_generation-begin_of_generation))  # TODO: remove the intermediate validation process from the time

            # ------------------------
            # final validation process
            # ------------------------
            self.runValidationProcess(
                state, action, actions, generation_information, next_state, episode, True)

        except END:
            return episode

    # ----------------------------------------------------------------

    def buildEvent(self, event_index, state, actions, episode, optimal_generation_process):
        """Build each event of the algorithm

        Args:
            event_index (int): event index that we are generating
            state (object): state object being analyzed
            actions (list): list of action objects
            episode (object): episode object being executed
            optimal_generation_process (boolean): check if the generation process is the optimal one

        Returns:
            action, generation_information, next_state, actions: information about the generation process of the event
        """

        while not episode.getGenerationProcessInfo(
        ).getState().getAlgorithm().getEventByIndex(event_index).isComplete():

            # ---------------------
            # select action
            # ---------------------
            aux = Utils.getTime()
            if optimal_generation_process:
                action, next_state, generation_information = self.selectOptimalAction(
                    state, actions)
            else:
                action, next_state, generation_information = self.selectAction(
                    state, actions)
            # ---------------------
            # update episode
            # ---------------------
            self.updateEpisodeLearningData(
                episode, next_state, generation_information)
            episode.getGenerationProcessInfo().addSelectActionTime(Utils.getTime()-aux)

            # ------------------------
            # middle validation process
            # ------------------------
            if GenerationInputs.runIntermediateValidationProcess() and \
                episode.getGenerationProcessInfo().getAlgorithm().getNumberOfActions() % GenerationInputs.getIntermediateValidationProcessNumberOfSteps() == 0 and \
                    not optimal_generation_process:  # do no apply the middle validation process on the optimal algorithm
                self.runValidationProcess(
                    state, action, actions, generation_information, next_state, episode, False)

            # ---------------------
            # update knowledge base
            # ---------------------
            if not episode.getGenerationProcessInfo().getAlgorithm().isComplete():

                # ---------------------
                # get possible actions
                # ---------------------
                aux = Utils.getTime()
                next_actions = self.getPossibleActions(next_state)
                episode.getGenerationProcessInfo().addActionsAndHeuristicsTime(Utils.getTime()-aux)

                aux = Utils.getTime()
                sample = {"state": state,
                          "action": action,
                          "actions": actions,
                          "reward": generation_information["reward"],
                          "next_state": next_state,
                          "next_actions": next_actions,
                          "done": False}
                self._learning_process.updateKnowledge(sample)
                episode.getGenerationProcessInfo().addUpdateKnowledgeBaseTime(Utils.getTime()-aux)

                # ---------------------
                # update data
                # ---------------------
                state = episode.getGenerationProcessInfo().getState().getCopy()
                actions = next_actions

        return action, generation_information, state, next_state, actions

    ##################################################################################################################################
    #
    #   VALIDATION PROCESS
    #
    ##################################################################################################################################

    def runValidationProcess(self, state, action, actions, generation_information, next_state, episode, final_validation):
        """Run validation process

        Args:
            state (object): current state
            action (object): current action
            actions (list): list of actions
            generation_information (json): json file with learning data
            next_state (object): next state 
            begin_of_generation (float): time of beginning of generation
            episode (object): current object
            final_validation (boolean): flag indicating if is the final validation

        Raises:
            END: exception
        """

        Logger.logDebugMessage(
            "Algorithm generated (ID="+str(state.getID())+"):\n")
        Logger.logInfoMessage(episode.getGenerationProcessInfo(
        ).getState().getAlgorithm().getPlainText(True))

        validation_result = None

        Logger.logInfoMessage("=== "+self.getOracleName() +
                              " validating the algorithm... \n")

        json_algorithm = episode.getGenerationProcessInfo(
        ).getState().getAlgorithm().getJsonAlgorithm()

        begin_of_validation = Utils.getTime()

        try:
            Logger.logDebugMessage("Send validation request to http://"+os.getenv('VALIDATOR_HOST') +
                                   ":"+os.getenv('VALIDATOR_PORT')+"/"+self.getOracleName()+"/validateAlgorithm\n")
            response = requests.post("http://"+os.getenv('VALIDATOR_HOST')+":"+os.getenv('VALIDATOR_PORT')+"/"+self.getOracleName()+"/validateAlgorithm", {}, {"algorithm_ID": state.getID(), "json_algorithm": json_algorithm, "final_validation": final_validation})
            validation_result = response.json()["result"]
        except Exception as e:
            Logger.logErrorMessage(
                "Not possible to contact the "+self.getOracleName()+" to validate the algorithm:"+str(e)+"\n")
        episode.getValidationProcessInfo().addTime(Utils.getTime()-begin_of_validation)

        # ----------------------
        # update validation info
        # ----------------------
        episode.getValidationProcessInfo().setValidationResult(validation_result)

        Logger.logInfoMessage("=== Validation result: " +
                              str(episode.getValidationProcessInfo().getValidationResult())+"\n")

        # if is the final validation or the middle validation with an invalid algorithm, the generation process is over
        if final_validation or (not final_validation and episode.getValidationProcessInfo().isFullyValidated() and not episode.getValidationProcessInfo().isValid()):

            # ---------------------
            # get final reward
            # ---------------------
            bonus_reward = self._learning_process.getBonusReward(
                episode.getValidationProcessInfo().getValidationResult())
            episode.getGenerationProcessInfo().addFinalReward(bonus_reward)

            # ---------------------
            # update knowledge base
            # ---------------------
            aux = Utils.getTime()
            sample = {"state": state,
                      "action": action,
                      "actions": actions,
                      "reward": bonus_reward + episode.getGenerationProcessInfo().getRuntimeReward(),
                      "next_state": next_state,
                      "next_actions": None,
                      "done": True}

            self._learning_process.updateKnowledge(sample)
            episode.getGenerationProcessInfo().addUpdateKnowledgeBaseTime(Utils.getTime()-aux)
            aux = Utils.getTime()
            # * used to update any data used by the policy
            self._learning_process.updatePolicyData()
            # * update the heuristics data
            if episode.getValidationProcessInfo().isFullyValidated():
                self._heuristics.applyHeuristic9(
                    state, action, episode.getValidationProcessInfo().isValid())
                self._heuristics.updateMostEfficientCorrectAlgorithmReward(
                    episode.getGenerationProcessInfo().getRuntimeReward(), episode.getValidationProcessInfo().isValid())
            episode.getGenerationProcessInfo().addValidationAndExtraTime(Utils.getTime()-aux)

            # * end of generation process
            raise END()
