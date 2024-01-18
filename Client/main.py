##################################################################################################################################
#
#   VARIABLES
#
##################################################################################################################################

#
import sys
import commentjson
import requests
import os
import utils.GlobalVariables.TextVariables as TextVariables
import utils.Logger as Logger
import json
#
from dotenv import load_dotenv
load_dotenv()
#

##################################################################################################################################
#
#   INPUTS AND CONFIG
#
##################################################################################################################################

Logger.logDebugMessage("GENERATOR_URL: " + str(os.getenv("GENERATOR_URL")))
Logger.logDebugMessage("VALIDATOR_URL: " + str(os.getenv("VALIDATOR_URL")))
if ((os.getenv("GENERATOR_HOST") is None) or
    (os.getenv("GENERATOR_PORT") is None) or
        (os.getenv("VALIDATOR_HOST") is None) or
        (os.getenv("VALIDATOR_PORT") is None)):
    Logger.logErrorMessage(
        "Environment variables, are not defined. They should be defined in the .env file.")
    exit(0)

generation_inputs_file = open(
    'inputs/Generation/generation_inputs.jsonc',)
generation_inputs = commentjson.load(generation_inputs_file)

validation_inputs_file = open(
    'inputs/Validation/validation_inputs.jsonc',)
validation_inputs = commentjson.load(validation_inputs_file)


##################################################################################################################################
#
#   -run
#
##################################################################################################################################

if len(sys.argv) == 3 and sys.argv[1] == "-run":
    """run the simulator
    """
    if sys.argv[2] == TextVariables.RB_LEARNER_AGENT:
        try:
            # sent the inputs to the Generator component
            requests.post("http://"+os.getenv('GENERATOR_HOST')+":" +
                          os.getenv('GENERATOR_PORT')+"/storeInputs", {},
                          {"inputs": generation_inputs})
            Logger.logDebugMessage("Generator received the inputs.")
        except Exception as e:
            Logger.logErrorMessage(
                "Not possible to connect with the Generator.")
            exit(0)
        try:
            # sent the inputs to the Validator component
            requests.post("http://"+os.getenv('VALIDATOR_HOST')+":" +
                          os.getenv('VALIDATOR_PORT')+"/storeInputs", {},
                          {"inputs": validation_inputs})
            Logger.logDebugMessage("Validator received the inputs.")
        except Exception as e:
            Logger.logErrorMessage(
                "Not possible to connect with the Validator.")
            exit(0)
        try:
            Logger.logInfoMessage("\n=== Running the generation process...\n")
            # generate the Reliable Broadcast algorithm
            response = requests.post("http://"+os.getenv('GENERATOR_HOST')+":" +
                                     os.getenv('GENERATOR_PORT') +
                                     "/"+sys.argv[2]+"/run", {},
                                     {})
            Logger.logInfoMessage(
                "=== Generation process is over. Check the results on the output folder inside the root folder of the Generator component.\n")
            
        except Exception as e:
            Logger.logErrorMessage(
                "Not possible to start the Generation Process.")
            exit(0)


##################################################################################################################################
#
#   -actions
#
##################################################################################################################################

elif len(sys.argv) == 3 and sys.argv[1] == "-actions":
    """get the current actions
    """
    if sys.argv[2] == TextVariables.RB_LEARNER_AGENT:
        try:
            requests.post("http://"+os.getenv('GENERATOR_HOST')+":" +
                          os.getenv('GENERATOR_PORT')+"/storeInputs", {},
                          {"inputs": generation_inputs})
            Logger.logDebugMessage("Generator received the inputs.")
        except Exception as e:
            Logger.logErrorMessage(
                "Not possible to connect with the Generator.")
            exit(0)

        try:
            Logger.logInfoMessage("Requesting the current available actions.")
            response = requests.post("http://"+os.getenv('GENERATOR_HOST')+":" +
                                     os.getenv('GENERATOR_PORT') +
                                     "/"+sys.argv[2]+"/actions", {},
                                     {})
        except Exception as e:
            Logger.logErrorMessage(
                "Not possible to start the Generation Process.")
            exit(0)

##################################################################################################################################
#
#   - tests
#
##################################################################################################################################

elif len(sys.argv) == 4 and sys.argv[1] == "-test":
    try:

        Logger.logInfoMessage(
            "\n=== Agent "+sys.argv[2]+" checking if algorithm "+sys.argv[3]+" is valid...")
        print()

        response = ""
        if sys.argv[2] == TextVariables.RB_ORACLE_AGENT:
            requests.post(os.getenv('VALIDATOR_URL')+"/storeInputs", {},
                          {"inputs": validation_inputs})
            # read the file
            json_algorithm = open(
                "tests/ReliableBroadcast/Algorithm_"+sys.argv[3]+".json", "r")
            # request the validation
            response = requests.post(os.getenv('VALIDATOR_URL')+"/"+sys.argv[2]+"/validateAlgorithm", {},
                                     {"algorithm_ID": sys.argv[3], "text_algorithm": "TBD\n", "json_algorithm": json.load(json_algorithm), "final_validation": True})
            json_algorithm.close()
            result = str(response.json()["result"])
            Logger.logInfoMessage(
                "=== Validation result: "+result+"\n")
        else:
            Logger.logErrorMessage("Input is wrong")
    except Exception as e:
        print(
            "Not possible to interact with the Generator and/or Validator: "+str(e))

##################################################################################################################################
#
#   - stop
#
##################################################################################################################################

elif len(sys.argv) == 3 and sys.argv[1] == "-stop":

    if sys.argv[2] == "Generator" or sys.argv[2] == "All":
        try:
            requests.get("http://"+os.getenv('GENERATOR_HOST')+":" +
                         os.getenv('GENERATOR_PORT')+"/stop")
            Logger.logInfoMessage("Generator shutdown.")
        except Exception as e:
                Logger.logErrorMessage(
                    "Not possible to shutdown the Generator.")
                exit(0)
    if sys.argv[2] == "Validator" or sys.argv[2] == "All":
        try:
                requests.get("http://"+os.getenv('VALIDATOR_HOST')+":" +
                         os.getenv('VALIDATOR_PORT')+"/stop")
                Logger.logInfoMessage("Validator shutdown.")
        except Exception as e:
                Logger.logErrorMessage(
                    "Not possible to shutdown the Validator.")
                exit(0)


##################################################################################################################################
#
#   - help
#
##################################################################################################################################

elif len(sys.argv) == 2 and sys.argv[1] == "-help":
    print("Available options:")
    print(
        "- python3 main.py -run [AGENT] : to run a specific Generator <AGENT>.")
    print(
        "- python3 main.py -actions [AGENT] : to check the available actions for the <AGENT>.")
    print(
        "- python3 main.py -stop [AGENT] : to stop the execution of the <AGENT> or All agents.")

##################################################################################################################################

else:
    print(
        "No command found. To see the available options, run > python3 main.py -help.")
