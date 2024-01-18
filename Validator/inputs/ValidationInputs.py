#
#   This class represents the Speaker
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

import utils.Utils as Utils

inputs_file_name = "current_validation_inputs.json"

##################################################################################################################################
#
#   GET
#
##################################################################################################################################


def runEventFailure(event):
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Event"][event]

# ----------------------------------------------------------------


def runNoFailuresMode():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["FailureMode"]["NO_FAILURE"]["Mode"]

# ----------------------------------------------------------------


def runCrashFailuresMode():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["FailureMode"]["CRASH_FAILURE"]["Mode"]

# ----------------------------------------------------------------


def runByzantineFailuresMode():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["FailureMode"]["BYZANTINE_FAILURE"]["Mode"]

# ----------------------------------------------------------------


def analyseValidityOnFinalValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["FinalValidation"]["validity"]

# ----------------------------------------------------------------


def analyseValidityOnIntermediateValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["IntermediateValidation"]["validity"]

# ----------------------------------------------------------------


def analyseIntegrityOnFinalValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["FinalValidation"]["integrity"]

# ----------------------------------------------------------------


def analyseIntegrityOnIntermediateValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["IntermediateValidation"]["integrity"]

# ----------------------------------------------------------------


def analyseAgreementOnFinalValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["FinalValidation"]["agreement"]

# ----------------------------------------------------------------


def analyseAgreementOnIntermediateValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["IntermediateValidation"]["agreement"]

# ----------------------------------------------------------------


def analyseTerminationOnFinalValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["FinalValidation"]["termination"]

# ----------------------------------------------------------------


def analyseTerminationOnIntermediateValidation():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["Properties"]["IntermediateValidation"]["termination"]

# ----------------------------------------------------------------


def getTestCases(failure_mode):
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["FailureMode"][failure_mode]["TestCases"]


# ----------------------------------------------------------------


def getMaxNumberOfRounds():
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["max_number_of_rounds"]

# ----------------------------------------------------------------


def getFailureDetector(class_name):
    validation_inputs = Utils.readJsonFile(
        'inputs/'+inputs_file_name)
    return validation_inputs["Validator"]["Validation"]["FailureDetector"][class_name]
