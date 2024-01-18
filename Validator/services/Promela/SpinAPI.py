##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
import configs.Configs as Configs
from utils.Exceptions.Invalid import INVALID
from utils.Exceptions.Incomplete import INCOMPLETE
from utils.Exceptions.Timeout import TIMEOUT
from dotenv import load_dotenv
#
import utils.Logger as Logger
import subprocess
import pathlib
import os
import psutil
load_dotenv()
#

##################################################################################################################################
#
#   VARIABLES
#
##################################################################################################################################

validation_tests_path = str(pathlib.Path(
    __file__).parent.absolute()) + '/Validation_Tests/'

##################################################################################################################################
#
#   RUN EXECUTION
#
##################################################################################################################################


def runModel(filename, validation_inputs):
    try:
        if Configs.getValidationProcess() == "BFS":
            result = runBFS(filename)
            validateResult(result, validation_inputs)
        elif Configs.getValidationProcess() == "DFS":
            result = runDFS(filename)
            validateResult(result, validation_inputs)
        elif Configs.getValidationProcess() == "SWARM":
            result = runSWARM(filename)
            validateResult(result, validation_inputs)
    except TIMEOUT:
        raise INCOMPLETE(validation_inputs)

##################################################################################################################################
#
#   AUXILIAR
#
##################################################################################################################################


def runBFS(filename):
    Logger.logDebugMessage("Running BFS technique...")
    subprocess.run(['spin', '-a', validation_tests_path +
                   filename], cwd=validation_tests_path)
    subprocess.run(['gcc', '-Wformat-overflow=0', '-O2', '-DVECTORSZ='+str(os.getenv('SPIN_DVECTORSZ')),
                   '-DBISTATE', '-DBFS_PAR', '-o', 'csoracle', 'pan.c'], cwd=validation_tests_path)
    subprocess.run(['chmod', '+x', 'csoracle'], cwd=validation_tests_path)
    result = executeValidation(['./csoracle', '-v', '-u'+str(os.getenv('SPIN_BFS_NUMBER_OF_CORES')),
                                '-w'+str(os.getenv('SPIN_BFS_HASH_TABLE_SIZE'))], validation_tests_path)
    return result


# ----------------------------------------------------------------

def runDFS(filename):
    Logger.logDebugMessage("Running DFS technique...")
    subprocess.run(['spin', '-a', validation_tests_path +
                   filename], cwd=validation_tests_path)
    subprocess.run(['gcc', '-Wformat-overflow=0', '-O2', '-DUSE_DISK', '-DVECTORSZ='+str(os.getenv('SPIN_DVECTORSZ')), '-DBISTATE', '-DNCORE='+str(os.getenv('SPIN_DFS_DNCORE')), '-DMEMLIM='+str(os.getenv('SPIN_DFS_DMEMLIM')), '-DVMAX='+str(os.getenv('SPIN_DFS_DVMAX')), '-o',
                    'csoracle', 'pan.c'], cwd=validation_tests_path)
    subprocess.run(['chmod', '+x', 'csoracle'], cwd=validation_tests_path)
    return executeValidation(['./csoracle'], validation_tests_path)

# ----------------------------------------------------------------


def runSWARM(filename):
    Logger.logDebugMessage("Running SWARM technique...")
    local_env = os.environ.copy()
    local_env["CCOMMON"] = "-O2 -DVECTORSZ=" + \
        str(os.getenv('SPIN_DVECTORSZ'))
    subprocess.run([str(pathlib.Path(__file__).parent.absolute())+'/../../utils/Swarm/Src/' + 'swarm', '-c'+str(os.getenv('SPIN_SWARM_CORES')), '-f', validation_tests_path +
                   filename], cwd=validation_tests_path, env=local_env)
    executeValidation(['./'+filename+'.swarm'],
                      validation_tests_path, local_env)
    output = ""
    for file in os.listdir(validation_tests_path):
        if file.endswith(".out"):
            with open(validation_tests_path+"/"+file) as f:
                output += f.read()
    return output


# ----------------------------------------------------------------

def executeValidation(args, path, env=None):
    for proc in psutil.process_iter():
        if proc.name() == "csoracle":
            proc.kill()
            Logger.logDebugMessage("Process aborted...")
    try:
        result = subprocess.run(args, cwd=path, env=env, stdout=subprocess.PIPE,
                                timeout=float(Configs.getValidationTimeout()))
        Logger.logDebugMessage("Validation concluded.")
        return result.stdout.decode('utf-8')
    except subprocess.TimeoutExpired:
        Logger.logDebugMessage("Validation incomplete.\n")
        for proc in psutil.process_iter():
            if proc.name() == "csoracle":
                proc.kill()
                Logger.logDebugMessage("Process aborted...")
        raise TIMEOUT()


##################################################################################################################################
#
#   VALIDATE OUTPUT
#
##################################################################################################################################


def validateResult(output, validation_inputs):
    # print the output
    Logger.logDebugMessage("SPIN Output:\n")
    Logger.logDebugMessage(output)
    incomplete_search = False
    output = output.splitlines()
    for line in output:
        if ("assertion violated") in line:
            raise INVALID(validation_inputs)
        elif("Search incomplete" in line):
            #raise INVALID(validation_inputs)
            incomplete_search = True
    if(incomplete_search):
        raise INCOMPLETE(validation_inputs)
