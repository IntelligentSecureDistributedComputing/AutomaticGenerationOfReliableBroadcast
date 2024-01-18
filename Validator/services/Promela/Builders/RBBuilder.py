
##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
from services.Promela.Builders.Builder import Builder
#
import utils.Logger as Logger
import inputs.ValidationInputs as ValidationInputs
import services.Promela.Definitions.RBDefinitions as RBDefinitions
import utils.Utils as Utils
import random
import utils.GlobalVariables.TextVariables as TextVariables
#

##################################################################################################################################
#
#   VARIBLES
#
##################################################################################################################################

TEMPLATE_FILENAME = "RBtemplate.pml"

##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################


class RBBuilder(Builder):

    ##################################################################################################################################
    #
    #   VARIBLES
    #
    ##################################################################################################################################

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        super().__init__()

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def getAgentName(self):
        return TextVariables.RB_ORACLE_AGENT

    ##################################################################################################################################
    #
    #   VALIDATION FUNCTIONS
    #
    ##################################################################################################################################

    def runValidationProcess(self, runtime_inputs):
        # get all the test cases
        test_cases = ValidationInputs.getTestCases(
            runtime_inputs.getCurrentFailureModeLabel())
        # for each test case
        for test in test_cases:
            # define the inputs
            F = test["F"]
            N = test["N"]
            runtime_inputs.setN(N)
            runtime_inputs.setF(F)
            Logger.logDebugMessage(
                ""+self.getAgentName()+": modeling system with N="+str(N)+" and F="+str(F))
            # no failure validation
            if(runtime_inputs.isNoFailureMode()):
                self.buildNoFailureValidationModel(
                    runtime_inputs)
                Logger.logDebugMessage("Model Valid\n")
            # crash and byzantine failures validation
            elif(runtime_inputs.isCrashFailureMode() or runtime_inputs.isByzantineFailureMode()):
                # * the failing process is the broadcaster
                self.buildFailureValidationModel(
                    runtime_inputs, True)
                Logger.logDebugMessage("Model Valid\n")
                # * the failing process is a peer
                self.buildFailureValidationModel(
                    runtime_inputs, False)
                Logger.logDebugMessage("Model Valid\n")

    # ----------------------------------------------------------------

    def buildNoFailureValidationModel(self, runtime_inputs):
        # define the inputs
        runtime_inputs.setBroadcaster(
            random.randrange(0, runtime_inputs.getN()))
        runtime_inputs.setFaultyProcesses([])
        # run the validation model
        self.buildValidationModel(runtime_inputs)

    # ----------------------------------------------------------------

    def buildFailureValidationModel(self, runtime_inputs, broadcaster_fails):
        # define the system model
        processes = list(range(runtime_inputs.getN()))
        broadcaster = random.choice(processes)
        processes.remove(broadcaster)
        faulty_processes = []
        if broadcaster_fails:
            faulty_processes += [broadcaster]
            Logger.logDebugMessage(
                ""+self.getAgentName()+": T1 - modeling failing process as broadcaster/proposer and peer")
        else:
            Logger.logDebugMessage(
                ""+self.getAgentName()+": T2 - modeling failing process only as peer")
        # define the faulty processes
        while (len(faulty_processes)+1) <= runtime_inputs.getF():
            faulty = random.choice(processes)
            processes.remove(faulty)
            faulty_processes += [faulty]
        # define the inputs
        runtime_inputs.setBroadcaster(broadcaster)
        runtime_inputs.setFaultyProcesses(faulty_processes)
        # run the validation model
        self.buildValidationModel(runtime_inputs)

    ##################################################################################################################################
    #
    #   VALIDATION MODEL
    #
    ##################################################################################################################################

    def buildValidationModel(self, runtime_inputs):

        # inputs
        groups_to_attack = Utils.generateGroups(
            runtime_inputs.getN(), runtime_inputs.getFaultyProcesses())

        r = open(super()._test_template_path + TEMPLATE_FILENAME, 'r')

        lines = r.readlines()
        new_lines = lines.copy()

        for i in range(len(lines)):

            if(lines[i] == "/*BROADCAST_STEP*/\n"):
                new_lines[i] = super().buildEvent(
                    runtime_inputs, TextVariables.BROADCAST_EVENT)

            elif(lines[i] == "/*COMMUNICATION_STEP*/\n"):
                new_lines[i] = super().buildEvent(
                    runtime_inputs, TextVariables.RECEIVE_EVENT)

            elif(lines[i] == "/*N_Types*/\n"):
                new_lines[i] = super().buildNTypes(runtime_inputs,
                                                   [TextVariables.BROADCAST_EVENT, TextVariables.RECEIVE_EVENT])

            elif(lines[i] == "/*N*/\n"):
                new_lines[i] = super().buildN(runtime_inputs)

            elif(lines[i] == "/*F*/\n"):
                new_lines[i] = super().buildF(runtime_inputs)

            elif(lines[i] == "/*PROCESS_BROADCASTING*/\n"):
                new_lines[i] = "#define PROCESS_BROADCASTING " + \
                    str(runtime_inputs.getBroadcaster())+"\n"

            elif(lines[i] == "/*FAULTY_DECISION*/\n"):
                new_lines[i] = super().buildFaultyDecision(
                    runtime_inputs)

            elif(lines[i] == "/*SYSTEM_ARCHITECTURE*/\n"):
                new_lines[i] = super().buildSystemArchitecture(runtime_inputs)

            elif(lines[i] == "/*VALIDITY*/\n"):
                new_lines[i] = super().buildValidityProperty(runtime_inputs)

            elif(lines[i] == "/*INTEGRITY*/\n"):
                new_lines[i] = super().buildIntegrityProperty(runtime_inputs)

            elif(lines[i] == "/*AGREEMENT*/\n"):
                new_lines[i] = super().buildAgreementProperty(runtime_inputs)

            elif(lines[i] == "/*BROADCAST_ATTACKS*/\n"):
                broadcast_send_types = runtime_inputs.getLogicMessageTypesFromEvent(
                    TextVariables.BROADCAST_EVENT)
                main_txt = ""
                main_txt += "if\n"
                main_txt += "::true;\n"
                for group in groups_to_attack:  # Send messages to sub-groups
                    main_txt += "::true->\n"
                    for correct_process in group:
                        for type in broadcast_send_types:
                            main_txt += RBDefinitions.getPromelaSend("true",
                                                                     "BYZANTINE_MESSAGE", type, str(correct_process))
                main_txt += "fi;\n"
                new_lines[i] = main_txt

            elif(lines[i] == "/*COMMUNICATION_ATTACKS*/\n"):
                # get all possible types
                all_types = runtime_inputs.getAllMessageTypesUsed(
                    [TextVariables.BROADCAST_EVENT, TextVariables.RECEIVE_EVENT])
                # get all send types used on both phases
                broadcast_send_types = runtime_inputs.getLogicMessageTypesFromEvent(
                    TextVariables.BROADCAST_EVENT)
                # add to the communication send types used on the attack the possible types that are not used on both communication and broadcast phases
                message_types_to_attack = []
                for type in all_types:
                    if type not in broadcast_send_types and type not in message_types_to_attack:
                        message_types_to_attack += [type]
                main_txt = ""
                main_txt += "if\n"
                main_txt += "::true;\n"
                for group in groups_to_attack:  # Send messages to sub-groups of correct processes
                    main_txt += "::true->\n"
                    for correct_process in group:
                        for type in message_types_to_attack:
                            main_txt += RBDefinitions.getPromelaSend("true",
                                                                     "BYZANTINE_MESSAGE", type, str(correct_process))
                main_txt += "fi;\n"
                new_lines[i] = main_txt

        r.close()
        w = open(super()._validation_tests_path+super()._test_filename, 'w')
        w.write("".join(new_lines))
        w.close()

        self.runValidationModel(runtime_inputs)
