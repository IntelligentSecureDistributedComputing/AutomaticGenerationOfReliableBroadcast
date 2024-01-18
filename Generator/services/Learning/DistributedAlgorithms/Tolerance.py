#
#   This file represents the algorithm generated
#

##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################


##################################################################################################################################
#
#   CLASS
#
##################################################################################################################################

class Tolerance:

    ##################################################################################################################################
    #
    #   VARIABLES
    #
    ##################################################################################################################################

    _NoFailureTolerance = None
    _CrashFailureTolerance = None
    _ByzantineFailureTolerance = None

    ##################################################################################################################################
    #
    #   CONSTRUCTOR
    #
    ##################################################################################################################################

    def __init__(self):
        """Constructor
        """
        pass

    ##################################################################################################################################
    #
    #   SET
    #
    ##################################################################################################################################

    def setNoFailureTolerance(self, value):
        """Set the No Failure tolerance of the algorithm

        Args:
            value (boolean): True if is tolerant; False if not
        """
        self._NoFailureTolerance = value

    # ----------------------------------------------------------------

    def setCrashFailureTolerance(self, value):
        """Set the Crash Failure tolerance of the algorithm

        Args:
            value (boolean): True if is tolerant; False if not
        """
        self._CrashFailureTolerance = value

    # ----------------------------------------------------------------
    #
    def setByzantineFailureTolerance(self, value):
        """Set the Byzantine Failure tolerance of the algorithm

        Args:
            value (boolean): True if is tolerant; False if not
        """
        self._ByzantineFailureTolerance = value

    ##################################################################################################################################
    #
    #   GET
    #
    ##################################################################################################################################

    def isNoFailureTolerant(self):
        """Check if is No Failure Tolerant

        Returns:
            boolean: True if is tolerant; False if is not
        """
        return self._NoFailureTolerance

    # ----------------------------------------------------------------

    def isCrashFailureTolerant(self):
        """Check if is No Crash Tolerant

        Returns:
            boolean: True if is tolerant; False if is not
        """
        return self._CrashFailureTolerance

    # ----------------------------------------------------------------

    def isByzantineFailureTolerant(self):
        """Check if is Byzantine Failure Tolerant

        Returns:
            boolean: True if is tolerant; False if is not
        """
        return self._ByzantineFailureTolerance

    # ----------------------------------------------------------------

    def isNoFailureModeTested(self):
        """Check if the No Failure mode is tested

        Returns:
            boolean: True if is tolerant; False if is not
        """
        return not self._NoFailureTolerance == None

    # ----------------------------------------------------------------

    def isCrashFailureModeTested(self):
        """Check if the Crash Failure mode is tested

        Returns:
            boolean: True if is tolerant; False if is not
        """
        return not self._CrashFailureTolerance == None

    # ----------------------------------------------------------------

    def isByzantineFailureModeTested(self):
        """Check if the Byzantine Failure mode is tested

        Returns:
            boolean: True if is tolerant; False if is not
        """
        return not self._ByzantineFailureTolerance == None
