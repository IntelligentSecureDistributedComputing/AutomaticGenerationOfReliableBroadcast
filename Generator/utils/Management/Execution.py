#
#   This file represents the Result function
#

# ola

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

import utils.Auxiliar.Graphics as Graphic
import utils.Auxiliar.Latex as Latex
import numpy
import utils.Utils as Utils
import inputs.GenerationInputs as GenerationInputs
import utils.Logger as Logger

##################################################################################################################################
#
#   VARIABLES
#
##################################################################################################################################


##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class Execution:

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    _simulations = None

    _actions = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self,):
        self._simulations = []
        self._actions = []
        Utils.createOrClearFolder(Utils.getOutputFolderPath())

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def addSimulation(self, simulation):
        self._simulations += [simulation]

    # -----------------------------------------------------------------

    def addActions(self, actions):
        self._actions = actions

    ##################################################################################################################################
    #
    #   EXPORT RESULTS
    #
    ##################################################################################################################################

    def exportResults(self):

        Logger.logDebugMessage("Exporting the execution results")

        # create Execution folder
        Utils.createOrClearFolder(Utils.getExecutionFolderPath())
        Utils.createOrClearFolder(Utils.getExecutionFolderPath()+'/LATEXData')
        Utils.createOrClearFolder(Utils.getExecutionFolderPath()+'/PDFGraphs')
        Utils.createOrClearFolder(Utils.getExecutionFolderPath()+'/TXTGraphs')
        # Actions
        self.exportAllPossibleActions()
        # States
        self.getStatesFoundStatistics()
        # Algorithms
        self.getAlgorithmsGeneratedStatistics()
        # self.getNumberOfCorrectAndIncorrectAlgorithmsGenerated()
        # Most Efficient Algorithms
        self.exportMostEfficientAlgorithmsAndStatistics()
        # Statistics
        self.exportStatistics()
        self.exportTimes()

    # -----------------------------------------------------------------

    def getNumberOfSimulations(self):
        return len(self._simulations)

    # -----------------------------------------------------------------

    def getNumberOfEpisodesPerSimulation(self):
        return self._simulations[0].getNumberOfEpisodes()

    # -----------------------------------------------------------------

    def getTotalTime(self):
        total_time = 0
        for simulation in self._simulations:
            total_time += simulation.getTotalTime()
        return total_time

    # -----------------------------------------------------------------

    def getTotalGenerationTime(self):
        total_time = 0
        for simulation in self._simulations:
            total_time += simulation.getTotalGenerationTime()
        return total_time

    # -----------------------------------------------------------------

    def getTotalValidationTime(self):
        total_time = 0
        for simulation in self._simulations:
            total_time += simulation.getTotalValidationTime()
        return total_time

    # -----------------------------------------------------------------

    def getAverageNumberOfStatesFound(self):
        total_states_found = 0
        for simulation in self._simulations:
            total_states_found += simulation.getTotalNumberOfStatesFound()
        return total_states_found/len(self._simulations)

    # -----------------------------------------------------------------

    def getAverageTimeUntilFirstValidAlgorithm(self):
        total_time = 0
        # valid_algorithms_found = 0
        for simulation in self._simulations:
            total_time += simulation.getTimeUntilFirstValidAlgorithm()
        #    if value != None:
        #        total_time += value
        #        valid_algorithms_found += 1
        # if valid_algorithms_found == 0:
        #    return 0
        # else:
        return total_time/len(self._simulations)

    # -----------------------------------------------------------------

    def getAverageNumberOfStatesExploredUntilFirstValidAlgorithm(self):
        number_of_states_explored = 0
        # valid_algorithms_found = 0
        for simulation in self._simulations:
            number_of_states_explored = simulation.getNumberOfStatesExploredUntilFirstValidAlgorithm()
        #    if value != None:
        #        number_of_states_explored += value
        #        valid_algorithms_found += 1
        # if valid_algorithms_found == 0:
        #    return 0
        # else:
        return number_of_states_explored/len(self._simulations)

    # -----------------------------------------------------------------

    def getAverageNumberOfGeneratedAlgorithms(self):
        number_of_algorithms_generated = 0
        for simulation in self._simulations:
            number_of_algorithms_generated += simulation.getTotalNumberOfGeneratedAlgorithms()
        return number_of_algorithms_generated/len(self._simulations)

    # -----------------------------------------------------------------

    def getAverageNumberOfEpisodesExploredUntilFirstValidAlgorithm(self):
        number_of_episodes = 0
        # valid_algorithms_found = 0
        for simulation in self._simulations:
            number_of_episodes += simulation.getNumberOfEpisodesExploredUntilFirstValidAlgorithm()
        #    if value != None:
        #        number_of_episodes += value
        #        valid_algorithms_found += 1
        # if valid_algorithms_found == 0:
        #    return 0
        # else:
        return number_of_episodes/len(self._simulations)

    # -----------------------------------------------------------------

    def getAverageNumberOfAlgorithmsFoundUntilFirstValidAlgorithm(self):
        number_of_algorithms = 0
        for simulation in self._simulations:
            number_of_algorithms += simulation.getNumberOfEpisodesExploredUntilFirstValidAlgorithm()
        return number_of_algorithms/len(self._simulations)

    # -----------------------------------------------------------------

    def getAverageNumberOfCorrectAlgorithms(self):
        correct_algorithms_found = 0
        for simulation in self._simulations:
            correct_algorithms_found += len(simulation.getValidAlgorithms())
        # if correct_algorithms_found == 0:
        #    return 0
        # else:
        return correct_algorithms_found/len(self._simulations)

    # -----------------------------------------------------------------

    def getAverageNumberOfIncorrectAlgorithms(self):
        incorrect_algorithms_found = 0
        for simulation in self._simulations:
            incorrect_algorithms_found += len(
                simulation.getInvalidAlgorithms())
        # if incorrect_algorithms_found == 0:
        #    return 0
        # else:
        return incorrect_algorithms_found/len(self._simulations)

    # -----------------------------------------------------------------

    def getTotalNumberOfEpisodes(self):
        return GenerationInputs.getNumberOfEpisodes()*GenerationInputs.getNumberOfSimulations()

    # -----------------------------------------------------------------

    def getStatesFoundStatistics(self):
        number_of_states_found = numpy.zeros(
            (GenerationInputs.getNumberOfEpisodes(), GenerationInputs.getNumberOfSimulations()))
        for simulation_index in range(len(self._simulations)):
            for episode_index in range(len(self._simulations[simulation_index].getEpisodes())):
                number_of_states_found[episode_index][simulation_index] = self._simulations[simulation_index].getEpisodes(
                )[episode_index].getGenerationProcessInfo().getTotalNumberOfStatesFound()
        Latex.exportTikzPictureData(number_of_states_found.mean(
            axis=1), number_of_states_found.std(axis=1), Utils.getExecutionFolderPath()+"/LATEXData/Number_Of_States_Explored.txt")

    # ----------------------------------------------------------------

    def getAlgorithmsGeneratedStatistics(self):
        number_of_algorithms_generated = numpy.zeros(
            (GenerationInputs.getNumberOfEpisodes(), GenerationInputs.getNumberOfSimulations()))
        for simulation_index in range(len(self._simulations)):
            algorithms_generated = []
            for episode_index in range(len(self._simulations[simulation_index].getEpisodes())):
                if not self._simulations[simulation_index].getEpisodes()[episode_index].getGenerationProcessInfo().getAlgorithm() in algorithms_generated:
                    algorithms_generated += [self._simulations[simulation_index].getEpisodes(
                    )[episode_index].getGenerationProcessInfo().getAlgorithm()]
                    number_of_algorithms_generated[episode_index][simulation_index] = len(
                        algorithms_generated)
        Latex.exportTikzPictureData(number_of_algorithms_generated.mean(
            axis=1), number_of_algorithms_generated.std(axis=1), Utils.getExecutionFolderPath()+"/LATEXData/Number_Of_Algorithms_Generated.txt")

    # ----------------------------------------------------------------

    # def getNumberOfCorrectAndIncorrectAlgorithmsGenerated(self):
    #     number_of_valid_algorithms_generated = numpy.zeros(
    #         GenerationInputs.getNumberOfSimulations())
    #     number_of_invalid_algorithms_generated = numpy.zeros(
    #         GenerationInputs.getNumberOfSimulations())
    #     for simulation_index in range(len(self._simulations)):
    #         number_of_invalid_algorithms_generated[simulation_index] = len(
    #             self._simulations[simulation_index].getInvalidAlgorithms())
    #         number_of_valid_algorithms_generated[simulation_index] = len(
    #             self._simulations[simulation_index].getValidAlgorithms())

    #     Latex.exportTikzPictureData([number_of_valid_algorithms_generated.mean(axis=0)], [
    #                                 number_of_valid_algorithms_generated.std(axis=0)], EXECUTION_FOLDER_PATH+"/Number_Of_Correct_Algorithms_Generated.txt")
    #     Latex.exportTikzPictureData([number_of_invalid_algorithms_generated.mean(axis=0)], [
    #                                 number_of_invalid_algorithms_generated.std(axis=0)], EXECUTION_FOLDER_PATH+"/Number_Of_Incorrect_Algorithms_Generated.txt")

    # ----------------------------------------------------------------

    def exportMostEfficientAlgorithmsAndStatistics(self):
        for simulation_index in range(len(self._simulations)):
            Graphic.writeTXTFile(self._simulations[simulation_index].getMostEfficientAlgorithm(
            ).getTextAlgorithm(), Utils.getExecutionFolderPath()+"/Final_Algorithm_Simulation_"+str(simulation_index+1)+".txt")
            Graphic.writeTXTFile(self._simulations[simulation_index].getOptimalAlgorithmStatistics(
            ), Utils.getExecutionFolderPath()+"/Statistics_Final_Algorithm_Simulation_"+str(simulation_index+1)+".txt")

    # ----------------------------------------------------------------

    def exportAllPossibleActions(self):
        Graphic.writeTXTFile(self._actions, Utils.getExecutionFolderPath() +
                             "/All_Actions.txt")

    # ----------------------------------------------------------------

    def exportStatistics(self):
        statistics = []
        statistics += ["\n########## EXECUTION STATISTICS #########\n\n"]
        statistics += ["Average number of algorithms generated: " + str(
            (self.getAverageNumberOfGeneratedAlgorithms())) + "\n"]
        statistics += ["Average number of states found: " + str(
            (self.getAverageNumberOfStatesFound())) + "\n"]
        statistics += ["Average number of states explored until first valid algorithm: " + str(
            (self.getAverageNumberOfStatesExploredUntilFirstValidAlgorithm())) + "\n"]
        statistics += ["Average number of episodes until first valid algorithm: " + str(
            (self.getAverageNumberOfEpisodesExploredUntilFirstValidAlgorithm())) + "\n"]
        statistics += ["Average number of algorithms until first valid algorithm: " + str(
            (self.getAverageNumberOfAlgorithmsFoundUntilFirstValidAlgorithm())) + "\n"]
        statistics += ["Average number of correct algorithms: " + str(
            (self.getAverageNumberOfCorrectAlgorithms())) + "\n"]
        statistics += ["Average number of incorrect algorithms: " + str(
            (self.getAverageNumberOfIncorrectAlgorithms())) + "\n"]
        statistics += ["\n################################\n"]
        Graphic.writeTXTFile(
            statistics, Utils.getExecutionFolderPath()+"/Statistics.txt")

    # ----------------------------------------------------------------

    def exportTimes(self):
        statistics = []
        statistics += ["########## EXECUTION TIMES #########\n\n"]
        statistics += ["Total time: " +
                       str(Utils.getTimePresentation(self.getTotalTime())) + "\n\n"]
        statistics += ["Average simulation time: " + str(
            Utils.getTimePresentation(self.getTotalTime()/len(self._simulations))) + "\n"]
        statistics += ["Average episode time: " + str(
            Utils.getTimePresentation(self.getTotalTime()/self.getTotalNumberOfEpisodes())) + "\n"]
        statistics += ["Average generation process time: " + str(
            Utils.getTimePresentation(self.getTotalGenerationTime()/self.getTotalNumberOfEpisodes())) + "\n"]
        statistics += ["Average validation process time: " + str(
            Utils.getTimePresentation(self.getTotalValidationTime()/self.getTotalNumberOfEpisodes())) + "\n"]
        statistics += ["Average time until the first valid algorithm: " + str(
            Utils.getTimePresentation(self.getAverageTimeUntilFirstValidAlgorithm())) + "\n"]
        statistics += ["\n########################\n"]
        Graphic.writeTXTFile(
            statistics, Utils.getExecutionFolderPath()+"/Times.txt")

    # ----------------------------------------------------------------

    def printExecutionData(self, number_of_actions):
        Logger.logInfoMessage("=== Execution Statistics")
        Logger.logInfoMessage(
            "Number of possible actions: " + str(number_of_actions))
        Logger.logInfoMessage(
            "Total time: " + str(Utils.getTimePresentation(self.getTotalTime())))
        Logger.logInfoMessage("===\n")
