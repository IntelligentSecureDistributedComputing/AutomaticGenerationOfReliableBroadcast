#
#   This class represents the Speaker
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################


##################################################################################################################################
#
#   LOGIC
#
##################################################################################################################################

def getPromelaSend(promela_condition, msg, message_type, receiver):
    label = ""
    label += "if\n"
    label += "::"+promela_condition + \
        " && pr["+receiver+"].s[ID].t[" + \
        str(message_type["value"])+"].m["+msg+"]==0->\n"
    label += "pr["+receiver+"].s[ID].t[" + \
        str(message_type["value"])+"].m["+msg+"]++;\n"
    # sending a message
    label += "inputChannel["+receiver+"]!" + \
        str(message_type["value"])+","+msg + \
        ",ID;\n"
    label += "::else;\n"
    label += "fi;\n"
    return label

# ----------------------------------------------------------------


def getPromelaDeliver(promela_condition):
    label = ""
    label += "/*********** DELIVER ***********/\n"
    label += "atomic{\n"
    label += "if\n"
    label += "::"+promela_condition+" && messages_delivered[ID].m[msg]==0 ->\n"
    label += "messages_delivered[ID].m[msg]++;\n"
    label += "::else;\n"
    label += "fi;\n"
    label += "}\n"
    label += "/******************************/\n"
    return label

# ----------------------------------------------------------------


def getPromelaSendAll(promela_condition, logic):
    label = ""
    init = "0"
    end = "N"
    label += "/*********** SEND ALL ***********/\n"
    label += "i="+init+";\n"
    label += "do\n"
    label += ":: i<"+end+"->\n"
    label += "if\n"
    label += "::(failure_mode_state[ID] == NO_FAILURE || failure_mode_state[ID] == CRASH_FAILURE) ->\n"
    label += "atomic{\n"
    label += getPromelaSend(promela_condition, logic["message"]
                            ["value"], logic["message"]
                            ["message_type"], "process_neighbours[ID].n[i]")
    label += "}\n"
    label += "::(failure_mode_state[ID] == CRASH_FAILURE) ->\n"
    label += "atomic{\n"
    label += getPromelaCrashSend()
    label += "}\n"
    label += "fi;\n"
    label += "i++;\n"
    label += "::else-> break;\n"
    label += "od;\n"
    label += "/******************************/\n"
    return label

# ----------------------------------------------------------------


def getPromelaCrashSend():
    label = ""
    label += "goto end_step;\n"
    return label

# ----------------------------------------------------------------


def getPromelaSendNeighbors(promela_condition, logic):
    label = ""
    init = "1"
    end = "N"
    label += "/*********** SEND NEIGHBORS ***********/\n"
    label += "i="+init+";\n"
    label += "do\n"
    label += ":: i<"+end+"->\n"
    label += "if\n"
    label += "::(failure_mode_state[ID] == NO_FAILURE || failure_mode_state[ID] == CRASH_FAILURE) ->\n"
    label += "atomic{\n"
    label += getPromelaSend(promela_condition, logic["message"]["value"], logic["message"]
                            ["message_type"], "process_neighbours[ID].n[i]")
    label += "}\n"
    label += "::(failure_mode_state[ID] == CRASH_FAILURE) ->\n"
    label += "atomic{\n"
    label += getPromelaCrashSend()
    label += "}\n"
    label += "fi;\n"
    label += "i++;\n"
    label += "::else-> break;\n"
    label += "od;\n"
    label += "/**************************************/\n"
    return label

# ----------------------------------------------------------------


def getPromelaSendMyself(promela_condition, logic):
    label = ""
    init = "0"
    end = "1"
    label += "/*********** SEND MYSELF ***********/\n"
    label += "i="+init+";\n"
    label += "do\n"
    label += ":: i<"+end+"->\n"
    label += "if\n"
    label += "::(failure_mode_state[ID] == NO_FAILURE || failure_mode_state[ID] == CRASH_FAILURE) ->\n"
    label += "atomic{\n"
    label += getPromelaSend(promela_condition, logic["message"]["value"], logic["message"]
                            ["message_type"], "process_neighbours[ID].n[i]")
    label += "}\n"
    label += "::(failure_mode_state[ID] == CRASH_FAILURE) ->\n"
    label += "atomic{\n"
    label += getPromelaCrashSend()
    label += "}\n"
    label += "fi;\n"
    label += "i++;\n"
    label += "::else-> break;\n"
    label += "od;\n"
    label += "/***********************************/\n"
    return label

# ----------------------------------------------------------------


def getPromelaStop():
    label = ""
    return label

# ----------------------------------------------------------------


def getPromelaThresholdCondition(condition, message_type):
    return "mr.t["+str(message_type["value"])+"].m[msg] >= "+str(condition)

# ----------------------------------------------------------------


def getPromelaEmptyCondition():
    return "true"

# ----------------------------------------------------------------
