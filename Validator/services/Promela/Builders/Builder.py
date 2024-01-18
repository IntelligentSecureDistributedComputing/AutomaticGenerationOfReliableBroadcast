
##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
import services.Promela.SpinAPI as SpinAPI
import pathlib
import utils.Utils as Utils
import inputs.ValidationInputs as ValidationInputs
#

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class Builder:

    ##################################################################################################################################
    #
    #   VARIBLES
    #
    ##################################################################################################################################

    _validation_tests_path = str(pathlib.Path(
        __file__).parent.absolute())+'/../Validation_Tests/'

    _test_template_path = str(pathlib.Path(
        __file__).parent.absolute()) + '/../Templates/'

    _test_filename = "test.pml"

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        super().__init__()
        Utils.createOrClearFolder(self._validation_tests_path)

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def runValidationModel(self, runtime_inputs):
        SpinAPI.runModel(self._test_filename, runtime_inputs)

    ##################################################################################################################################
    #
    #   BUILD
    #
    ##################################################################################################################################

    def buildEvent(self, runtime_inputs, event_name):
        promela = ""
        for action in runtime_inputs.getEventPromela(event_name):
            promela += action+"\n"
        return promela

# ----------------------------------------------------------------

    def buildNTypes(self, runtime_inputs, events_name):
        all_message_types_used = runtime_inputs.getHighestMessageTypeUsed(
            events_name)
        return "#define N_Types " + \
            str(all_message_types_used+1) + \
            "\n"  # ? the +1 is because the message type starts at 0

# ----------------------------------------------------------------

    def buildN(self, runtime_inputs):
        return "#define N " + \
            str(runtime_inputs.getN())+"\n"

# ----------------------------------------------------------------

    def buildF(self, runtime_inputs):
        return "#define F " + \
            str(runtime_inputs.getF())+"\n"

# ----------------------------------------------------------------

    def buildFaultyDecision(self, runtime_inputs):
        failure_mode = runtime_inputs.getCurrentFailureModeLabel()
        promela = ""
        for faulty_process in runtime_inputs.getFaultyProcesses():
            promela += "failure_mode_state[" + \
                str(faulty_process)+"]="+failure_mode+"\n"
        return promela

# ----------------------------------------------------------------

    def buildSystemArchitecture(self, runtime_inputs):
        system_architecture = Utils.generateSystemArchitecture(
            runtime_inputs.getN())
        promela = ""
        for process_index in range(len(system_architecture)):
            for neighbor_index in range(len(system_architecture[process_index])):
                promela += "process_neighbours["+str(process_index)+"].n["+str(
                    neighbor_index)+"]="+str(system_architecture[process_index][neighbor_index])+";\n"
            promela += "run Proc("+str(process_index)+");\n"
        return promela

# ----------------------------------------------------------------

    def buildIntegrityProperty(self, runtime_inputs):
        if runtime_inputs.isFinalValidation():
            if ValidationInputs.analyseIntegrityOnFinalValidation():
                return "#define INTEGRITY true"
            else:
                return "#define INTEGRITY false"
        else:
            if ValidationInputs.analyseIntegrityOnIntermediateValidation():
                return "#define INTEGRITY true"
            else:
                return "#define INTEGRITY false"

# ----------------------------------------------------------------

    def buildValidityProperty(self, runtime_inputs):
        if runtime_inputs.isFinalValidation():
            if ValidationInputs.analyseValidityOnFinalValidation():
                return "#define VALIDITY true"
            else:
                return "#define VALIDITY false"
        else:
            if ValidationInputs.analyseValidityOnIntermediateValidation():
                return "#define VALIDITY true"
            else:
                return "#define VALIDITY false"

# ----------------------------------------------------------------

    def buildAgreementProperty(self, runtime_inputs):
        if runtime_inputs.isFinalValidation():
            if ValidationInputs.analyseAgreementOnFinalValidation():
                return "#define AGREEMENT true"
            else:
                return "#define AGREEMENT false"
        else:
            if ValidationInputs.analyseAgreementOnIntermediateValidation():
                return "#define AGREEMENT true"
            else:
                return "#define AGREEMENT false"
