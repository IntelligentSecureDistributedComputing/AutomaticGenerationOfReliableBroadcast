##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from flask import request
from flask import Flask
from services.Agents.RBOracle import RBOracle
from services.Inputs.RBInputs import RBInputs
from dotenv import load_dotenv
from waitress import serve
#
import utils.Utils as Utils
import utils.Logger as Logger
import os
import signal
load_dotenv()


##################################################################################################################################
#
#   VARIABLES
#
##################################################################################################################################

app = Flask(__name__)

# Create the Oracle agent
RBOracleValidator = RBOracle()

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

    Logger.logDebugMessage("RBOracle storing the inputs\n")

    Utils.writeJsonFile(request.json["inputs"],
                        'inputs/current_validation_inputs.json')

    return "OK"

# ----------------------------------------------------------------


@app.get('/')
def deafult():
    """Default endpoint

    Returns:
        string: phrase
    """
    return "FAULTAGE validator working..."

# ----------------------------------------------------------------


@app.post('/RBOracle/resetOracle')
def resetRBOracle():
    """Reset the RBOracle memory

    Returns:
        string: OK
    """
    RBOracleValidator.resetOracle()
    return "OK"

# ----------------------------------------------------------------


@app.post('/RBOracle/validateAlgorithm')
def RBOracleValidateAlgorithm():
    """endpoint to validate the algorithm

    Returns:
        OK/ERROR: simple response
    """

    # define the runtime generation inputs
    runtime_inputs = RBInputs()
    buildRuntimeInputs(runtime_inputs)

    # get the algorithm ID
    Logger.logDebugMessage(
        "RBOracle validating algorithm ID: "+str(request.json["algorithm_ID"]))

    # get the validation result
    result = RBOracleValidator.runValidationProcess(
        runtime_inputs)

    return {"result": result}

# ----------------------------------------------------------------


@app.get('/stop')
def stop():
    """endpoint that shutdown the server

    Returns:
        OK/ERROR: simple response
    """
    os.kill(os.getpid(), signal.SIGINT)
    return "Oracle server is shutting down..."

##################################################################################################################################
#
#   AUXILIARY
#
##################################################################################################################################


def buildRuntimeInputs(runtime_inputs):
    runtime_inputs.setFinalValidation(request.json["final_validation"])
    # set the number maximum number of types
    runtime_inputs.setJsonAlgorithm(request.json["json_algorithm"])
    # set algorithm ID
    runtime_inputs.setID(request.json["algorithm_ID"])


##################################################################################################################################
#
#   MAIN
#
##################################################################################################################################
if __name__ == '__main__':

    # print the environment variables
    Logger.logDebugMessage("GENERATOR_HOST: " +
                           str(os.getenv("GENERATOR_HOST")))
    Logger.logDebugMessage("GENERATOR_PORT: " +
                           str(os.getenv("GENERATOR_PORT")))
    Logger.logDebugMessage("VALIDATOR_HOST: " +
                           str(os.getenv("VALIDATOR_HOST")))
    Logger.logDebugMessage("VALIDATOR_PORT: " +
                           str(os.getenv("VALIDATOR_PORT")))
    Logger.logDebugMessage("SPIN_BFS_NUMBER_OF_CORES: " +
                           str(os.getenv("SPIN_BFS_NUMBER_OF_CORES")))
    Logger.logDebugMessage("SPIN_BFS_HASH_TABLE_SIZE: " +
                           str(os.getenv("SPIN_BFS_HASH_TABLE_SIZE")))
    Logger.logDebugMessage("SPIN_DFS_DMEMLIM: " +
                           str(os.getenv("SPIN_DFS_DMEMLIM")))
    Logger.logDebugMessage("SPIN_DFS_DVMAX: " +
                           str(os.getenv("SPIN_DFS_DVMAX")))
    Logger.logDebugMessage("SPIN_DFS_DNCORE: " +
                           str(os.getenv("SPIN_DFS_DNCORE")))
    Logger.logDebugMessage("SPIN_DVECTORSZ: " +
                           str(os.getenv("SPIN_DVECTORSZ")))
    Logger.logDebugMessage("SPIN_SWARM_CORES: " +
                           str(os.getenv("SPIN_SWARM_CORES")))

    if (os.getenv("GENERATOR_HOST") is None) or \
            (os.getenv("GENERATOR_PORT") is None) or \
    (os.getenv("VALIDATOR_HOST") is None) or \
            (os.getenv("VALIDATOR_PORT") is None) or \
        (os.getenv("SPIN_BFS_NUMBER_OF_CORES") is None) or \
    (os.getenv("SPIN_BFS_HASH_TABLE_SIZE") is None) or \
        (os.getenv("SPIN_DFS_DMEMLIM") is None) or \
    (os.getenv("SPIN_DFS_DVMAX") is None) or \
        (os.getenv("SPIN_DFS_DNCORE") is None) or \
            (os.getenv("SPIN_DVECTORSZ") is None) or\
            (os.getenv("SPIN_SWARM_CORES") is None):
        Logger.logErrorMessage("Environment variables are not set")
        exit(0)
    else:
        Logger.logInfoMessage("\nValidator component ON\n")
        serve(app, host=os.getenv('VALIDATOR_HOST'),
              port=os.getenv('VALIDATOR_PORT'))
