##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
import time
import datetime
import os
import shutil
import math
import json
import random
#
from tabulate import tabulate

##################################################################################################################################
#
#   FUNCTIONS
#
##################################################################################################################################


def createFolder(path):
    """Create a folder based on the path

    Args:
        path (string): path of the folder to be created
    """
    os.mkdir(path)

# ----------------------------------------------------------------


def clearFolder(path):
    """Clears a folder

    Args:
        path (string): path of the folder to be cleared
    """
    filelist = [f for f in os.listdir(path)]
    for f in filelist:
        try:
            os.remove(os.path.join(path, f))
        except IsADirectoryError:
            shutil.rmtree(os.path.join(path, f))

# ----------------------------------------------------------------


def createOrClearFolder(path):
    """Creates or clear a specific folder

    Args:
        path (string): path to the folder
    """
    if (not os.path.exists(path)):
        createFolder(path)
    else:
        clearFolder(path)

# ----------------------------------------------------------------


def getDateTime():
    """Returns current date with time

    Returns:
        _type_: _description_
    """
    return datetime.datetime.now()

# ----------------------------------------------------------------


def getTime():
    """Return the current time

    Returns:
        int: time in seconds
    """
    return time.time()

# ----------------------------------------------------------------


def getTimePresentation(time):
    """Function that return the time in a specific format

    Args:
        time (int): time int in seconds

    Returns:
        string: time in a specific format
    """
    return (datetime.timedelta(seconds=time))

# ----------------------------------------------------------------


def evaluateExpression(expression, variables):
    """Function that evaluates an expression based on the inputs

    Args:
        expression (string): expression in a string format
        variables (json): json object with the variables and their values

    Returns:
        int: value of the expression
    """
    expression = list(expression)
    variables_keys = variables.keys()
    for char_index in range(len(expression)):
        if expression[char_index] in variables_keys:
            new_value = variables[expression[char_index]]
            expression[char_index] = str(new_value)
    expression = ''.join(expression)
    return math.ceil(eval(expression))

# ----------------------------------------------------------------


def writeJsonFile(content, filename):
    """write a json object

    Args:
        content (json): json object to be stored
        filename (string): filename containing the path to the file
    """
    with open(filename, 'w') as outfile:
        json.dump(content, outfile)

# ----------------------------------------------------------------


def readJsonFile(filename):
    """read a json file

    Args:
        filename (string): filename contaiing the path to the file

    Returns:
        json object: json object read from the file
    """
    with open(filename) as json_file:
        return json.load(json_file)

# ----------------------------------------------------------------


def getTable(header, body):
    """Prints a table message

    Args:
        header (list): header of the table
        body (list): body of the table
    """
    return tabulate(body, headers=header)

# ----------------------------------------------------------------


def generateSystemArchitecture(N):
    architecture = []
    for process in range(N):
        architecture += [getNeighbours(process, N)]
    return architecture

# ----------------------------------------------------------------


def getNeighbours(process, N):
    neighbours = []
    for neighbour in range(N):
        if (neighbour != process):
            neighbours += [neighbour]
    random.shuffle(neighbours)
    result = [process]+neighbours
    return result

# ----------------------------------------------------------------


def generateGroups(number_of_processes, faulty_processes):
    groups = []
    processes = list(range(number_of_processes))
    correct_processes = [
        process for process in processes if process not in faulty_processes]
    g = 1
    while len(groups) < len(correct_processes):
        aux_correct_process = correct_processes.copy()
        group = []
        while len(group) < g and len(aux_correct_process) > 0:
            correct_process = random.choice(aux_correct_process)
            group += [correct_process]
            aux_correct_process.remove(correct_process)
        g += 1
        groups += [group]
    return groups

# ----------------------------------------------------------------


def getOutputFolderPath():
    return os.path.dirname(os.path.abspath(__file__))+'/../output'

# ----------------------------------------------------------------


def getExecutionFolderPath():
    return getOutputFolderPath()+"/Execution"
