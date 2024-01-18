#
#   Reliable Broadcast QTable
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.Learning.Agents.Learner import Learner
from utils.Management.Episode.RBEpisode import RBEpisode
from services.ActionsSpace.RBActionsSpace import RBActionsSpace
#
import utils.GlobalVariables.TextVariables as TextVars


##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class RBLearner(Learner):

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

    # Constructor
    def __init__(self):
        """Constructor
        """
        super().__init__(RBActionsSpace())

    # ----------------------------------------------------------------

    def reset(self):
        self.__init__()

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getName(self):
        """Get the learner agent name

        Returns:
            string: learner agent name
        """
        return TextVars.RB_LEARNER_AGENT

    # ----------------------------------------------------------------

    def getOracleName(self):
        """Get the oracle agent name

        Returns:
            string: oracle agent name
        """
        return TextVars.RB_ORACLE_AGENT

    ##################################################################################################################################
    #
    #   GENERATION PROCESS
    #
    ##################################################################################################################################

    def runGenerationProcess(self, episode_number, optimal_generation_process=False):
        """Run the generation process

        Args:
            optimal_generation_process (bool, optional): flag that indicates if we are running the optimal generation process. Defaults to False.
        """
        return super().runGenerationProcess(RBEpisode(episode_number), optimal_generation_process)
