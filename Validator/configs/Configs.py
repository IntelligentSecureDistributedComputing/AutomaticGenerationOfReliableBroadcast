
##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################
#
import commentjson
#
configurations_file = open('configs/configs.jsonc',)
configurations = commentjson.load(configurations_file)

##################################################################################################################################
#
#   GET
#
##################################################################################################################################


def getValidationProcess():
    return configurations["ValidationProcess"]

# ----------------------------------------------------------------


def getDefaultValidationResult():
    return configurations["DefaultValidationResult"]

# ----------------------------------------------------------------


def getValidationTimeout():
    return configurations["ValidationTimeout"]
