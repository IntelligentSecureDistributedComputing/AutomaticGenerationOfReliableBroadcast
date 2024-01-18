# Events labels
BROADCAST_EVENT = "RB-Broadcast"
PROPOSE_EVENT = "CS-Propose"
RECEIVE_EVENT = "Receive"
FD_RECEIVE_EVENT = "FD-Receive"

# Logic components labels
SEND_ALL = "SendAll"
SEND_MYSELF = "SendMyself"
SEND_NEIGHBORS = "SendNeighbors"
DELIVER = "Deliver"
STOP = "Stop"

DECIDE = "Decide"
SEND_TO_COORDINATOR = "SendToCoordinator"
PROPOSE = "Propose"
SET_ESTIMATE = "SetEstimate"

# Failure modes labels
NO_FAILURE_MODE = "No-Failure"
CRASH_FAILURE_MODE = "Crash-Failure"
BYZANTINE_FAILURE_MODE = "Byzantine-Failure"

# Agents labels
RB_LEARNER_AGENT = "RBLearner"
RB_ORACLE_AGENT = "RBOracle"
CS_LEARNER_AGENT = "CSLearner"
CS_ORACLE_AGENT = "CSOracle"

# Learning algorithms labels
REINFORCE = "REINFORCE"
MONTE_CARLO = "MonteCarlo"
QLEARNING = "QLearning"
DOUBLE_QLEARNING = "DoubleQLearning"
DEEP_QLEARNING = "DeepQLearning"
DOUBLE_DEEP_QLEARNING = "DoubleDeepQLearning"
DUELING_DEEP_QLEARNING = "DuelingDeepQLearning"
PRIORITIZED_EXPERIENCE_REPLAY = "PrioritizedExperienceReplay"

# Exploration algorithms labels
RANDOM = "Random"
UCB = "UCB"
EPSILON_GREEDY = "EpsilonGreedy"

# Message types
TYPE = "type"
SUSPECT_TYPE = "suspecttype"
