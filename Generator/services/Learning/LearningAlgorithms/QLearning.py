
#
#   QLearning
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.Learning.LearningAlgorithms.Learning import Learning
from services.Learning.KnowledgeBase.QTable import QTable
#
import random
import utils.GlobalVariables.TextVariables as Vars
import configs.Configs as Configs
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class QLearning(Learning):

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

    def __init__(self, actions_space_object):
        """Constructor

        Args:
            actions_space_object (Object): Actions Space object
        """
        super().__init__(QTable(actions_space_object), actions_space_object)

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def updateKnowledge(self, sample):
        """Update the Q-Table

        Args:
            sample (json): json object with 5 keys (state,action,reward,next_state,next_actions)
        """

        # double Q-Learning
        if Configs.runQLearningExtra(Vars.DOUBLE_QLEARNING):
            # update QTable1
            if(random.uniform(0, 1) > 0.5):
                self._knowledge_base.updateQTable1StateActionValue(sample["state"],
                                                                   sample["action"],
                                                                   self._knowledge_base.getQTable1StateActionValue(sample["state"], sample["action"]) + Configs.getLearningAlgorithmHyperparameter("QLearning", "learning_rate") * (sample["reward"] + Configs.getLearningAlgorithmHyperparameter("QLearning", "gamma") *
                                                                                                                                                                                                                                             self._knowledge_base.getQTable2BestActionValue(sample["next_state"], sample["next_actions"]) -
                                                                                                                                                                                                                                             self._knowledge_base.getQTable1StateActionValue(sample["state"], sample["action"])))
            # update QTable2
            else:
                self._knowledge_base.updateQTable2StateActionValue(sample["state"],
                                                                   sample["action"],
                                                                   self._knowledge_base.getQTable2StateActionValue(sample["state"], sample["action"]) + Configs.getLearningAlgorithmHyperparameter("QLearning", "learning_rate") * (sample["reward"] + Configs.getLearningAlgorithmHyperparameter("QLearning", "gamma") *
                                                                                                                                                                                                                                             self._knowledge_base.getQTable1BestActionValue(sample["next_state"], sample["next_actions"]) -
                                                                                                                                                                                                                                             self._knowledge_base.getQTable2StateActionValue(sample["state"], sample["action"])))
        # single Q-Learning
        else:

            if sample["done"]:
                target = sample["reward"]
            else:
                target = sample["reward"] + Configs.getLearningAlgorithmHyperparameter("QLearning", "gamma") * self._knowledge_base.getQTable1BestActionValue(
                    sample["next_state"], sample["next_actions"]) - self._knowledge_base.getQTable1StateActionValue(sample["state"], sample["action"])
            # update QTable
            self._knowledge_base.updateQTable1StateActionValue(sample["state"], sample["action"], self._knowledge_base.getQTable1StateActionValue(
                sample["state"], sample["action"]) + Configs.getLearningAlgorithmHyperparameter("QLearning", "learning_rate") * target)

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def isQLearning(self):
        """Check if this is the Q-Learning

        Returns:
            boolean: True
        """
        return True
