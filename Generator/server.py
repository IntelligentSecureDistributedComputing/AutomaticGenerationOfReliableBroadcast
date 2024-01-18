##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
import requests
import utils.Utils as Utils
import utils.Logger as Logger
import inputs.GenerationInputs as GenerationInputs
import traceback
import os
import signal
#
from utils.Exceptions.EmptyProblem import EMPTY_PROBLEM
from utils.Management.Execution import Execution
from services.Learning.Agents.RBLearner import RBLearner
from utils.Management.Simulation import Simulation
from flask import Flask
from dotenv import load_dotenv
from flask import request
from waitress import serve
load_dotenv()
#

##################################################################################################################################
#
#   VARIABLES
#
##################################################################################################################################

app = Flask(__name__)

# ----------------------------------------------------------------


def runSimulation(simulation_number, generation_process, execution):
    """Run a simulation

    Args:
        simulation_number (int): number of the simulation

    Returns:
        object: simulation object
    """

    _simulation = Simulation(
        simulation_number, generation_process.getTotalNumberOfActions())

    # * store the simulation
    execution.addSimulation(_simulation)

    for episode_number in range(1, GenerationInputs.getNumberOfEpisodes()+1):

        Logger.logInfoMessage("\n========== EPISODE "+str(episode_number)+"/"+str(GenerationInputs.getNumberOfEpisodes())+" | SIMULATION " +
                              str(_simulation.getSimulationNumber())+"/"+str(GenerationInputs.getNumberOfSimulations())+" ==========\n")

        # get algorithm
        episode = generation_process.runGenerationProcess(episode_number)

        # print episode info
        episode.printEpisodeData()

        # store episode
        _simulation.addEpisode(episode)

        # print simulation info
        _simulation.printSimulationData()

        execution.printExecutionData(
            generation_process._learning_process._knowledge_base._actions_space.getSize())

    Logger.logInfoMessage("\n========== OPTIMAL EPISODE | SIMULATION " +
                          str(_simulation.getSimulationNumber())+"/"+str(GenerationInputs.getNumberOfSimulations())+" ==========\n")

    # get optimal algorithm
    optimal_episode = generation_process.runGenerationProcess(
        episode_number+1, True)

    # print episode info
    optimal_episode.printEpisodeData()

    # export results
    _simulation.getResults(optimal_episode)

    return

# ----------------------------------------------------------------


def run(generation_process):
    """endpoint to run the simulation

    Returns:
        OK/ERROR: simple response
    """

    try:

        # * create execution
        execution = Execution()

        execution.addActions(
            generation_process._learning_process._knowledge_base._actions_space.getActionSpace())

        # start from 1
        for simulation_number in range(1, GenerationInputs.getNumberOfSimulations()+1):

            generation_process.reset()

            # * run simulation
            runSimulation(
                simulation_number, generation_process, execution)

            # clear the Oracle memory after each simulation
            try:
                requests.post(
                    "http://"+os.getenv('VALIDATOR_HOST')+":"+os.getenv('VALIDATOR_PORT')+"/"+generation_process.getOracleName()+"/resetOracle", {}, {})
            except:
                pass

            # * export results
            execution.exportResults()

        return "OK"

    # * exceptions
    except KeyboardInterrupt:
        Logger.logErrorMessage("EXIT")
        return "ERROR"
    except EMPTY_PROBLEM as error:
        Logger.logErrorMessage(error.getMessage())
        return "ERROR"
    except Exception as error:
        Logger.logErrorMessage(str(error))
        traceback.print_exc()
        return "ERROR"

# ----------------------------------------------------------------


def actions(generation_process):
    """endpoint to return the current actions

    Returns:
        OK/ERROR: simple response
    """
    generation_process._learning_process._knowledge_base._actions_space.printActionSpace()

    return "OK"

##################################################################################################################################
#
#   ROUTES
#
##################################################################################################################################


@app.post('/storeInputs')
def storeInputs():
    """endpoint to store the inputs

    Returns:
        OK/ERROR: simple response
    """
    Utils.writeJsonFile(request.json["inputs"],
                        'inputs/current_generation_inputs.json')

    return "OK"

# ----------------------------------------------------------------


@app.post('/RBLearner/run')
def runRBLearner():
    """endpoint to run the RBLearner

    Returns:
        OK/ERROR: simple response
    """
    generation_process = RBLearner()
    return run(generation_process)


# ----------------------------------------------------------------


@app.post('/RBLearner/actions')
def actionsRBLearner():
    """endpoint to return the current actions

    Returns:
        OK/ERROR: simple response
    """
    generation_process = RBLearner()
    return actions(generation_process)


# ----------------------------------------------------------------


@app.get('/')
def default():
    """Default endpoint

    Returns:
        string: phrase
    """
    return "FAULTAGE generator working..."

# ----------------------------------------------------------------


@app.get('/stop')
def stop():
    """endpoint that shutdown the server

    Returns:
        OK/ERROR: simple response
    """
    os.kill(os.getpid(), signal.SIGINT)
    return "Learner server is shutting down..."


##################################################################################################################################
#
#   MAIN
#
##################################################################################################################################
if __name__ == '__main__':
    Logger.logDebugMessage("GENERATOR_HOST: " +
                           str(os.getenv("GENERATOR_HOST")))
    Logger.logDebugMessage("GENERATOR_PORT: " +
                           str(os.getenv("GENERATOR_PORT")))
    Logger.logDebugMessage("VALIDATOR_HOST: " +
                           str(os.getenv("VALIDATOR_HOST")))
    Logger.logDebugMessage("VALIDATOR_PORT: " +
                           str(os.getenv("VALIDATOR_PORT")))
    if (os.getenv("GENERATOR_HOST") is None) or \
            (os.getenv("GENERATOR_PORT") is None) or \
    (os.getenv("VALIDATOR_HOST") is None) or \
            (os.getenv("VALIDATOR_PORT") is None):
        Logger.logErrorMessage("environment variables are not set")
        exit(0)
    else:
        Logger.logInfoMessage("\nGenerator component ON\n")
        serve(app, host=os.getenv('GENERATOR_HOST'),
              port=os.getenv('GENERATOR_PORT'))
