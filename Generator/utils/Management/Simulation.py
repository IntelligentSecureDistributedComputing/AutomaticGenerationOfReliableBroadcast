#
#   This file represents the Result function
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

import utils.Utils as Utils
import utils.Auxiliar.Graphics as Graphic
import utils.Logger as Logger
import os
import json
import configs.Configs as Configs

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


class Simulation:

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    _episodes = None

    _simulation_number = None

    _valid_algorithms = None

    _invalid_algorithms = None

    _incomplete_validation_algorithms = None

    _most_efficient_algorithm = None

    _total_number_of_actions = None

    _number_of_states_until_first_valid_algorithm = 0

    _time_until_first_valid_algorithm = 0

    _number_of_episodes_until_first_valid_algorithm = 0

    _number_of_algorithms_found_until_first_valid_algorithm = 0

    _optimal_episode = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, simulation_number, total_number_of_actions):
        self._simulation_number = simulation_number
        self._episodes = []
        self._valid_algorithms = []
        self._invalid_algorithms = []
        self._incomplete_validation_algorithms = []
        self._total_number_of_actions = total_number_of_actions

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def addEpisode(self, episode):

        # add episode
        self._episodes += [episode]

        # export middle results
        if (len(self._episodes) % Configs.getResultsBatchSize()) == 0:
            self.getResults(episode)

        # statistics until first valid algorithm
        if len(self._valid_algorithms) == 0:
            self._number_of_episodes_until_first_valid_algorithm += 1
            self._time_until_first_valid_algorithm += episode.getTime()
            self._number_of_states_until_first_valid_algorithm = episode.getGenerationProcessInfo(
            ).getTotalNumberOfStatesFound()
            self._number_of_algorithms_found_until_first_valid_algorithm = len(
                self._invalid_algorithms)+len(self._valid_algorithms)

        # validation result
        if(episode.getValidationProcessInfo().isFullyValidated() and episode.getValidationProcessInfo().isValid() and not episode.getGenerationProcessInfo().getAlgorithm() in self._valid_algorithms):
            self._valid_algorithms += [
                episode.getGenerationProcessInfo().getAlgorithm()]

        elif(episode.getValidationProcessInfo().isFullyValidated() and not episode.getValidationProcessInfo().isValid() and not episode.getGenerationProcessInfo().getAlgorithm() in self._invalid_algorithms):
            self._invalid_algorithms += [
                episode.getGenerationProcessInfo().getAlgorithm()]
        elif(not episode.getValidationProcessInfo().isFullyValidated() and not episode.getGenerationProcessInfo().getAlgorithm() in self._incomplete_validation_algorithms):
            self._incomplete_validation_algorithms += [
                episode.getGenerationProcessInfo().getAlgorithm()]

    # ----------------------------------------------------------------

    def setMostEfficientAlgorithm(self, algorithm):
        self._most_efficient_algorithm = algorithm

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getResults(self, episode=None):

        Logger.logDebugMessage("Exporting the simulation results...")

        # prepare folders
        Utils.createOrClearFolder(
            Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number))
        Utils.createOrClearFolder(Utils.getOutputFolderPath()+"/Simulation_"+str(
            self._simulation_number)+"/ValidAlgorithms")
        Utils.createOrClearFolder(Utils.getOutputFolderPath()+"/Simulation_"+str(
            self._simulation_number)+"/UnknownAlgorithms")
        Utils.createOrClearFolder(Utils.getOutputFolderPath()+"/Simulation_"+str(
            self._simulation_number)+"/TXTGraphs")
        Utils.createOrClearFolder(Utils.getOutputFolderPath()+"/Simulation_"+str(
            self._simulation_number)+"/PDFGraphs")

        # export statistics
        self.exportStatistics()
        self.exportTimes()
        self.exportValidAlgorithms()
        self.exportUnknownAlgorithms()

        # draw graphs
        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeRewardData(), "Episode",
                                 "Reward", "Cumulative reward per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/CumulativeRewardPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeRewardData(), "Episode",
                                 "Reward", "Cumulative reward per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/CumulativeRewardPerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeRegretData(), "Episode",
                                 "Regret", "Cumulative regret per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/CumulativeRegretPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeRegretData(), "Episode",
                                 "Regret", "Cumulative regret per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/CumulativeRegretPerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getScorePerEpisode(), "Episode",
                                 "Score", "Score per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/ScorePerEpisodePerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getScorePerEpisode(), "Episode",
                                 "Score", "Score per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/ScorePerEpisodePerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeRegretData(), "Episode",
                                 "Score", "Cumulative Score per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/CumulativeScoreGraphPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeRegretData(), "Episode",
                                 "Score", "Cumulative Score per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/CumulativeScoreGraphPerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeStatesFoundPerEpisode(), "Episode",
                                 "States", "Cumulative States found per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/CumulativeStatesFoundPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeStatesFoundPerEpisode(), "Episode",
                                 "States", "Cumulative States found per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/CumulativeStatesFoundPerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getStatesFoundPerEpisode(), "Episode",
                                 "States", "States found per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/StatesFoundPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getStatesFoundPerEpisode(), "Episode",
                                 "States", "States found per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/StatesFoundPerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeAlgorithmsFoundPerEpisode(), "Episode",
                                 "Algorithms", "Cumulative algorithms generated per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/CumulativeAlgorithmsGeneratedPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getCumulativeAlgorithmsFoundPerEpisode(), "Episode",
                                 "Algorithms", "Cumulative algorithms generated per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/CumulativeAlgorithmsGeneratedPerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getTimePerEpisode(), "Episode",
                                 "Time(s)", "Time per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/TimePerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getTimePerEpisode(), "Episode",
                                 "Time(s)", "Time per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/TimePerEpisode")

        Graphic.drawTXT2LineGraph(list(range(1, len(self._episodes)+1)), self.getGenerationTimePerEpisode(), "Generation Process", list(range(1, len(self._episodes)+1)), self.getValidationTimePerEpisode(), "ValidationProcess", "Episode",
                                  "Time(s)", "Time per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/ProcessesTimePerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getRewardPerEpisode(), "Episode",
                                 "Reward", "Reward per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/RewardPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getRewardPerEpisode(), "Episode",
                                 "Reward", "Reward per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/RewardPerEpisode")

        Graphic.drawTXTLineGraph(list(range(1, len(self._episodes)+1)), self.getRegretPerEpisode(), "Episode",
                                 "Regret", "Regret per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/TXTGraphs/RegretPerEpisode")
        Graphic.drawPDFLineGraph(list(range(1, len(self._episodes)+1)), self.getRegretPerEpisode(), "Episode",
                                 "Regret", "Regret per episode", Utils.getOutputFolderPath()+"/Simulation_"+str(self._simulation_number)+"/PDFGraphs/RegretPerEpisode")

        # export optimal algorithm
        if not episode == None:
            self._optimal_episode = episode
            self.exportOptimalAlgorithm(
                episode.getGenerationProcessInfo().getAlgorithm())
            self.setMostEfficientAlgorithm(
                episode.getGenerationProcessInfo().getAlgorithm())
            self.exportOptimalAlgorithmStatistics()


    # ----------------------------------------------------------------

    def getRewardPerEpisode(self):
        reward_list = []
        for episode in self._episodes:
            reward_list += [episode.getGenerationProcessInfo().getRuntimeReward() +
                            episode.getGenerationProcessInfo().getFinalReward()]
        return reward_list

    # ----------------------------------------------------------------

    def getRegretPerEpisode(self):
        regret_list = []
        for episode in self._episodes:
            regret_list += [episode.getGenerationProcessInfo().getRegret()]
        return regret_list

    # ----------------------------------------------------------------

    def getCumulativeRewardData(self):
        cumulative_reward = 0
        cumulative_reward_list = []
        for episode in self._episodes:
            cumulative_reward += episode.getTotalReward()
            cumulative_reward_list += [cumulative_reward]
        return cumulative_reward_list

    # ----------------------------------------------------------------

    def getCumulativeRegretData(self):
        cumulative_regret = 0
        cumulative_regret_list = []
        for episode in self._episodes:
            cumulative_regret += episode.getGenerationProcessInfo().getRegret()
            cumulative_regret_list += [cumulative_regret]
        return cumulative_regret_list

   # ----------------------------------------------------------------

    def getScorePerEpisode(self):
        scorePerEpisode = []
        for episode in self._episodes:
            epsilon = episode.getGenerationProcessInfo().getScore()
            scorePerEpisode += [epsilon]
        return scorePerEpisode

   # ----------------------------------------------------------------

    def getCumulativeScore(self):
        cumulative_score = []
        aux = 0
        for episode in self._episodes:
            aux += episode.getGenerationProcessInfo().getScore()
            cumulative_score += [aux]
        return cumulative_score

    # ----------------------------------------------------------------

    def getCumulativeStatesFoundPerEpisode(self):
        number_of_states_found = []
        for episode in self._episodes:
            number_of_states_found += [
                episode.getGenerationProcessInfo().getTotalNumberOfStatesFound()]
        return number_of_states_found

    # ----------------------------------------------------------------

    def getStatesFoundPerEpisode(self):
        number_of_states_found = []
        aux = 0
        for episode in self._episodes:
            number_of_states_found += [
                episode.getGenerationProcessInfo().getTotalNumberOfStatesFound()-aux]
            aux = episode.getGenerationProcessInfo().getTotalNumberOfStatesFound()
        return number_of_states_found

    # ----------------------------------------------------------------

    def getCumulativeAlgorithmsFoundPerEpisode(self):
        number_of_algorithms_found = []
        aux_algorithms = []
        for episode in self._episodes:
            if episode.getGenerationProcessInfo().getAlgorithm() not in aux_algorithms:
                aux_algorithms += [episode.getGenerationProcessInfo().getAlgorithm()]
            number_of_algorithms_found += [len(aux_algorithms)]
        return number_of_algorithms_found

    # ----------------------------------------------------------------

    def getTimePerEpisode(self):
        episodes_time = []
        for episode in self._episodes:
            episodes_time += [episode.getTime()]
        return episodes_time

    # ----------------------------------------------------------------

    def getCumulativeTimePerEpisode(self):
        episodes_time = []
        aux = 0
        for episode in self._episodes:
            aux += episode.getTime()
            episodes_time += [aux]
        return episodes_time

    # ----------------------------------------------------------------

    def getMaxRewardReceived(self):
        max_reward = None
        for episode in self._episodes:
            if max_reward == None or max_reward < episode.getTotalReward():
                max_reward = episode.getTotalReward()
        return max_reward

    # ----------------------------------------------------------------

    def getEpisodes(self):
        return self._episodes

    # ----------------------------------------------------------------

    def getMostEfficientAlgorithm(self):
        return self._most_efficient_algorithm

    # ----------------------------------------------------------------

    def getSimulationNumber(self):
        return self._simulation_number

    # ----------------------------------------------------------------

    def getValidAlgorithms(self):
        return self._valid_algorithms

    # ----------------------------------------------------------------

    def getInvalidAlgorithms(self):
        return self._invalid_algorithms

    # ----------------------------------------------------------------

    def getTotalTime(self):
        total_time = 0
        for episode in self._episodes:
            total_time += episode.getTime()
        return total_time

    # ----------------------------------------------------------------

    def getTotalGenerationTime(self):
        total_time = 0
        for episode in self._episodes:
            total_time += episode.getGenerationProcessInfo().getTime()
        return total_time

    # ----------------------------------------------------------------

    def getCumulativeGenerationTimePerEpisode(self):
        generation_time = []
        aux = 0
        for episode in self._episodes:
            aux += episode.getGenerationProcessInfo().getTime()
            generation_time += [aux]
        return generation_time

    # ----------------------------------------------------------------

    def getGenerationTimePerEpisode(self):
        generation_time = []
        for episode in self._episodes:
            generation_time += [episode.getGenerationProcessInfo().getTime()]
        return generation_time

    # ----------------------------------------------------------------

    def getTotalValidationTime(self):
        total_time = 0
        for episode in self._episodes:
            total_time += episode.getValidationProcessInfo().getTime()
        return total_time

    # ----------------------------------------------------------------

    def getCumulativeValidationTimePerEpisode(self):
        validation_time = []
        aux = 0
        for episode in self._episodes:
            aux += episode.getValidationProcessInfo().getTime()
            validation_time += [aux]
        return validation_time

    # ----------------------------------------------------------------

    def getValidationTimePerEpisode(self):
        validation_time = []
        for episode in self._episodes:
            validation_time += [episode.getValidationProcessInfo().getTime()]
        return validation_time

    # ----------------------------------------------------------------

    def getTotalNumberOfActions(self):
        return self._total_number_of_actions

    # ----------------------------------------------------------------

    def getTimeUntilFirstValidAlgorithm(self):
        if len(self._valid_algorithms) == 0:
            return 0
        else:
            return self._time_until_first_valid_algorithm

    # ----------------------------------------------------------------

    def getNumberOfStatesExploredUntilFirstValidAlgorithm(self):
        if len(self._valid_algorithms) == 0:
            return 0
        else:
            return self._number_of_states_until_first_valid_algorithm

    # ----------------------------------------------------------------

    def getNumberOfEpisodesExploredUntilFirstValidAlgorithm(self):
        if len(self._valid_algorithms) == 0:
            return 0
        else:
            return self._number_of_episodes_until_first_valid_algorithm

    # ----------------------------------------------------------------

    def getNumberOfAlgorithmsFoundUntilFirstValidAlgorithm(self):
        if len(self._valid_algorithms) == 0:
            return 0
        else:
            return self._number_of_algorithms_found_until_first_valid_algorithm

    # ----------------------------------------------------------------

    def getNumberOfEpisodes(self):
        return len(self._episodes)

    # ----------------------------------------------------------------

    def getTotalNumberOfStatesFound(self):
        return self._episodes[-1].getGenerationProcessInfo().getTotalNumberOfStatesFound()

    # ----------------------------------------------------------------

    def getTotalNumberOfGeneratedAlgorithms(self):
        return len(self._valid_algorithms) + len(self._invalid_algorithms)

    # ----------------------------------------------------------------

    def getTotalApplyHeuristicsTime(self):
        apply_heuristics_time = 0
        for episode in self._episodes:
            apply_heuristics_time += episode.getGenerationProcessInfo().getActionsAndHeuristicsTime()
        return apply_heuristics_time

    # ----------------------------------------------------------------

    def getTotalSelectActionTime(self):
        select_action_time = 0
        for episode in self._episodes:
            select_action_time += episode.getGenerationProcessInfo().getSelectActionTime()
        return select_action_time

    # ----------------------------------------------------------------

    def getTotalUpdateKnowledgeBaseTime(self):
        update_knowledge_base_time = 0
        for episode in self._episodes:
            update_knowledge_base_time += episode.getGenerationProcessInfo().getUpdateKnowledgeBaseTime()
        return update_knowledge_base_time

    # ----------------------------------------------------------------

    def getTotalValidationExtraTime(self):
        validation_extra_time = 0
        for episode in self._episodes:
            validation_extra_time += episode.getGenerationProcessInfo().getValidationAndExtraTime()
        return validation_extra_time

    ##################################################################################################################################
    #
    #   EXPORT RESULTS
    #
    ##################################################################################################################################

    def exportValidAlgorithms(self):
        for i in range(len(self._valid_algorithms)):
            Graphic.writeTXTFile(self._valid_algorithms[i].getTextAlgorithm(), Utils.getOutputFolderPath()+"/Simulation_"+str(
                self._simulation_number)+"/ValidAlgorithms/Algorithm_"+str(i)+".txt")
            Graphic.writeJSONFile(json.dumps(self._valid_algorithms[i].getJsonAlgorithm(), indent=4), Utils.getOutputFolderPath()+"/Simulation_"+str(
                self._simulation_number)+"/ValidAlgorithms/Algorithm_"+str(i)+"_json.txt")

    # ----------------------------------------------------------------

    def exportUnknownAlgorithms(self):
        for i in range(len(self._incomplete_validation_algorithms)):
            Graphic.writeTXTFile(self._incomplete_validation_algorithms[i].getTextAlgorithm(), Utils.getOutputFolderPath()+"/Simulation_"+str(
                self._simulation_number)+"/UnknownAlgorithms/Algorithm_"+str(i)+".txt")

    # ----------------------------------------------------------------

    def exportOptimalAlgorithm(self, algorithm):
        Graphic.writeTXTFile(algorithm.getTextAlgorithm(), Utils.getOutputFolderPath()+"/Simulation_"+str(
            self._simulation_number)+"/Converged_Algorithm.txt")

    # ----------------------------------------------------------------

    def exportStatistics(self):
        statistics = []
        statistics += ["########## SIMULATION STATISTICS #########\n\n"]
        statistics += ["Max total reward received: " +
                       str(self.getMaxRewardReceived())+"\n\n"]
        statistics += ["Total number of episodes executed: " +
                       str(len(self._episodes))+"\n"]
        statistics += ["Total number of states found: " +
                       str(self.getTotalNumberOfStatesFound())+"\n"]
        statistics += ["Total number of algorithms found: " +
                       str(self.getTotalNumberOfGeneratedAlgorithms())+"\n"]
        statistics += ["Total number of correct algorithms found: " +
                       str(len(self._valid_algorithms))+"\n"]
        statistics += ["Total number of incorrect algorithms found: " +
                       str(len(self._invalid_algorithms))+"\n"]
        statistics += ["Total number of incomplete validation processes: " +
                       str(len(self._incomplete_validation_algorithms))+"\n\n"]
        statistics += ["Total states found until first valid algorithm: " +
                       str(self.getNumberOfStatesExploredUntilFirstValidAlgorithm())+"\n"]
        statistics += ["Total episodes found until first valid algorithm: " +
                       str(self.getNumberOfEpisodesExploredUntilFirstValidAlgorithm())+"\n"]
        statistics += ["Total algorithms found until first valid algorithm: " +
                       str(self.getNumberOfAlgorithmsFoundUntilFirstValidAlgorithm())+"\n"]
        statistics += ["\n###########################################\n"]
        Graphic.writeTXTFile(statistics, Utils.getOutputFolderPath() +
                             "/Simulation_"+str(self._simulation_number)+"/Statistics.txt")

    # ----------------------------------------------------------------

    def exportTimes(self):
        statistics = []
        statistics += ["########## SIMULATION TIMES #########\n\n"]
        statistics += ["Total time: " +
                       str(Utils.getTimePresentation(self.getTotalTime()))+"\n\n"]
        statistics += ["Total generation time: " +
                       str(Utils.getTimePresentation(self.getTotalGenerationTime()))+"\n"]
        statistics += ["Total apply heuristics time: " +
                       str(Utils.getTimePresentation(self.getTotalApplyHeuristicsTime()))+"\n"]
        statistics += ["Total select action time: " +
                       str(Utils.getTimePresentation(self.getTotalSelectActionTime()))+"\n"]
        statistics += ["Total update knowledge base time: " +
                       str(Utils.getTimePresentation(self.getTotalUpdateKnowledgeBaseTime()))+"\n"]
        statistics += ["Total validation extra time: " +
                       str(Utils.getTimePresentation(self.getTotalValidationExtraTime()))+"\n\n"]
        statistics += ["Total validation time: " +
                       str(Utils.getTimePresentation(self.getTotalValidationTime()))+"\n\n"]
        statistics += ["Time until first valid algorithm: " +
                       str(Utils.getTimePresentation(self.getTimeUntilFirstValidAlgorithm()))+"\n\n"]
        statistics += ["Average episode time: " +
                       str(Utils.getTimePresentation(self.getTotalTime()/len(self._episodes)))+"\n"]
        statistics += ["Average generation time: " + str(Utils.getTimePresentation(
            self.getTotalGenerationTime()/len(self._episodes)))+"\n"]
        statistics += ["Average validation time: " +
                       str(Utils.getTimePresentation(self.getTotalValidationTime()/len(self._episodes)))+"\n"]
        statistics += ["\n#####################################\n"]
        Graphic.writeTXTFile(statistics, Utils.getOutputFolderPath() +
                             "/Simulation_"+str(self._simulation_number)+"/Times.txt")
    # ----------------------------------------------------------------

    def getOptimalAlgorithmStatistics(self):
        statistics = []
        statistics += ["########## OPTIMAL ALGORITHM STATISTICS #########\n\n"]
        statistics += ["Total reward: " +
                       str(self._optimal_episode.getTotalReward())+"\n"]
        statistics += ["Algorithm correctness: " +
                       str(self._optimal_episode.getValidationProcessInfo().getValidationResult())+"\n"]
        # statistics += ["Algorithm fully validated: " +
        #               str(self._optimal_episode.getValidationProcessInfo().isFullyValidated())+"\n"]
        statistics += ["\n################################################\n"]
        return statistics

    # ----------------------------------------------------------------

    def exportOptimalAlgorithmStatistics(self):
        statistics = self.getOptimalAlgorithmStatistics()
        Graphic.writeTXTFile(statistics, Utils.getOutputFolderPath() +
                             "/Simulation_"+str(self._simulation_number)+"/OptimalAlgorithmStatistics.txt")

    ##################################################################################################################################
    #
    #   AUXILIAR
    #
    ##################################################################################################################################

    def printSimulationData(self):
        Logger.logInfoMessage("=== Simulation Statistics")
        Logger.logInfoMessage(
            "Total time: " + str(Utils.getTimePresentation(self.getTotalTime())))
        Logger.logInfoMessage("Total generation time: " +
                              str(Utils.getTimePresentation(self.getTotalGenerationTime())))
        Logger.logInfoMessage("Total validation time: " +
                              str(Utils.getTimePresentation(self.getTotalValidationTime())))
        Logger.logInfoMessage("Max reward received: " +
                              str(self.getMaxRewardReceived()))
        Logger.logInfoMessage("Total number of states found: " + str(
            self._episodes[-1].getGenerationProcessInfo().getTotalNumberOfStatesFound()))
        Logger.logInfoMessage("Total number of algorithms found: " +
                              str(len(self._valid_algorithms) + len(self._invalid_algorithms)))
        Logger.logInfoMessage(
            "Correct algorithms found: " + str(len(self._valid_algorithms)))
        Logger.logInfoMessage(
            "Incorrect algorithms found: " + str(len(self._invalid_algorithms)))
        Logger.logInfoMessage("Incomplete validation processes: " +
                              str(len(self._incomplete_validation_algorithms)))
        Logger.logInfoMessage("===\n")
