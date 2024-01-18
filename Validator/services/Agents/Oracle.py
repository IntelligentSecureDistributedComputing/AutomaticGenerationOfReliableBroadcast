#
#   This file represents the Validator
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from utils.Exceptions.Invalid import INVALID
from utils.Exceptions.Incomplete import INCOMPLETE
#
import utils.Logger as Logger
import inputs.ValidationInputs as ValidationInputs
import configs.Configs as Configs
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class Oracle:

    ##################################################################################################################################
    #
    #   VARIBLES
    #
    ##################################################################################################################################

    _algorithms_already_validated = None

    _builder = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self, builder):
        self._ID = None
        self._validation_DB = {}
        self._algorithms_already_validated = []
        self._builder = builder

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    ##################################################################################################################################
    #
    #   VALIDATION PROCESS
    #
    ##################################################################################################################################

    # algorithm, final_validation):
    def runValidationProcess(self, runtime_inputs):

        if runtime_inputs.isFinalValidation():
            Logger.logInfoMessage(
                "\n========== "+self.getAgentName()+" FINAL VALIDATION PROCESS ==========\n")
        else:
            Logger.logInfoMessage(
                "\n========== "+self.getAgentName()+" MIDDLE VALIDATION PROCESS ==========\n")

        Logger.logInfoMessage(runtime_inputs.getTextAlgorithm())

        if not Configs.getDefaultValidationResult() == "":
            Logger.logInfoMessage(
                "=== (Default) Validation result: "+Configs.getDefaultValidationResult()+"\n")
            return Configs.getDefaultValidationResult()
        else:

            Logger.logInfoMessage(
                "=== Verifying correctness of the algorithm...\n")

            # * get DB validation data
            validation_results = self.getAlgorithmValidationResults(
                runtime_inputs.getID())

            try:
                # no failure validation
                if(ValidationInputs.runNoFailuresMode()):
                    Logger.logDebugMessage(
                        ""+self.getAgentName()+": analyzing the No Failures mode...")
                    if "NoFailureTolerance" in validation_results.keys():
                        if validation_results["NoFailureTolerance"] == True:
                            Logger.logDebugMessage("Model Valid")
                        elif validation_results["NoFailureTolerance"] == False:
                            raise INVALID(runtime_inputs)
                        elif validation_results["NoFailureTolerance"] == None:
                            raise INCOMPLETE(runtime_inputs)
                    else:
                        runtime_inputs.setCurrentFailureMode(
                            True, False, False)
                        self._builder.runValidationProcess(
                            runtime_inputs)
                        if runtime_inputs.isFinalValidation():
                            validation_results["NoFailureTolerance"] = True

                # crash validation
                elif(ValidationInputs.runCrashFailuresMode()):
                    Logger.logDebugMessage(
                        ""+self.getAgentName()+": analyzing the Crash Failures mode...")
                    runtime_inputs.setCurrentFailureMode(False, True, False)
                    if "CrashFailureTolerance" in validation_results.keys():
                        if validation_results["CrashFailureTolerance"] == True:
                            Logger.logDebugMessage("Model Valid")
                        elif validation_results["CrashFailureTolerance"] == False:
                            raise INVALID(runtime_inputs)
                        elif validation_results["CrashFailureTolerance"] == None:
                            raise INCOMPLETE(runtime_inputs)
                    else:
                        self._builder.runValidationProcess(
                            runtime_inputs)
                        if runtime_inputs.isFinalValidation():
                            validation_results["CrashFailureTolerance"] = True

                # byzantine validation
                elif(ValidationInputs.runByzantineFailuresMode()):
                    Logger.logDebugMessage(
                        ""+self.getAgentName()+": analyzing the Byzantine Failures mode...")
                    if "ByzantineFailureTolerance" in validation_results.keys():
                        if validation_results["ByzantineFailureTolerance"] == True:
                            Logger.logDebugMessage("Model Valid")
                        elif validation_results["ByzantineFailureTolerance"] == False:
                            raise INVALID(runtime_inputs)
                        elif validation_results["ByzantineFailureTolerance"] == None:
                            raise INCOMPLETE(runtime_inputs)
                    else:
                        runtime_inputs.setCurrentFailureMode(
                            False, False, True)
                        self._builder.runValidationProcess(
                            runtime_inputs)
                        if runtime_inputs.isFinalValidation():
                            validation_results["ByzantineFailureTolerance"] = True

                # correct algorithm
                # Utils.clearFolder(self._validation_tests_path)
                Logger.logInfoMessage(
                    "=== Validation result: True\n")
                return True

            # incorrect algorithm
            except INVALID as error:
                # Utils.clearFolder(self._validation_tests_path)
                if error.getValidationInputs().isNoFailureMode():
                    validation_results["NoFailureTolerance"] = False
                elif error.getValidationInputs().isCrashFailureMode():
                    validation_results["CrashFailureTolerance"] = False
                elif error.getValidationInputs().isByzantineFailureMode():
                    validation_results["ByzantineFailureTolerance"] = False
                Logger.logInfoMessage(
                    "=== Validation result: False\n")
                return False

            # incorrect algorithm
            except INCOMPLETE as error:
                # Utils.clearFolder(self._validation_tests_path)
                if error.getValidationInputs().isNoFailureMode():
                    validation_results["NoFailureTolerance"] = None
                elif error.getValidationInputs().isCrashFailureMode():
                    validation_results["CrashFailureTolerance"] = None
                elif error.getValidationInputs().isByzantineFailureMode():
                    validation_results["ByzantineFailureTolerance"] = None
                Logger.logInfoMessage(
                    "=== Validation result: None\n")
                return None

    ##################################################################################################################################
    #
    #   AUXILIAR
    #
    ##################################################################################################################################

    def getAlgorithmValidationResults(self, ID):
        """Get the validation results of the algorithm

        Args:
            ID (int): ID of the algorithm

        Returns:
            json: json object with the validation result of each failure mode
        """
        if not ID in self._validation_DB.keys():
            self._validation_DB[ID] = {}
        return self._validation_DB[ID]

    # ----------------------------------------------------------------

    def resetOracle(self):
        """Reset the Oracle
        """
        self._validation_DB = {}
