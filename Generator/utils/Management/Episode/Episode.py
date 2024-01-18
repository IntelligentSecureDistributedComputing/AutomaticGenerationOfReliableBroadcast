#
#   This file represents the Result function
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

from utils.Parameters.ValidationProcessInfo import ValidationProcessInfo
from utils.Parameters.GenerationProcessInfo import GenerationProcessInfo
import utils.Logger as Logger

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class Episode:

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    _episode_number = None

    _generation_process_info = None

    _validation_process_info = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, episode_number):
        self.setEpisodeNumber(episode_number)
        self._generation_process_info = GenerationProcessInfo()
        self._validation_process_info = ValidationProcessInfo()

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getEpisodeNumber(self):
        return self._episode_number

    # ----------------------------------------------------------------

    def getGenerationProcessInfo(self):
        return self._generation_process_info

    # ----------------------------------------------------------------

    def getValidationProcessInfo(self):
        return self._validation_process_info

    # ----------------------------------------------------------------

    def getTime(self):
        return self._generation_process_info.getTime()+self._validation_process_info.getTime()

    # ----------------------------------------------------------------

    def getTotalReward(self):
        return self._generation_process_info.getRuntimeReward()+self._generation_process_info.getFinalReward()

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def setEpisodeNumber(self, value):
        self._episode_number = value

    ##################################################################################################################################
    #
    #   AUXILIAR
    #
    ##################################################################################################################################

    def printEpisodeData(self):
        self.getGenerationProcessInfo().printGenerationProcessInfo()
        self.getValidationProcessInfo().printValidationProcessInfo()
