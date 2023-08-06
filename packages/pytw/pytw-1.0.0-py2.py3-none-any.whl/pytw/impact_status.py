import enum

class Status(enum.Enum):
    """
    Status defines the enum of status values, enumeration values as follows: OPEN, RESOLVED, IGNORED
    """
    OPEN = 0
    RESOLVED = 1
    IGNORED = 2
    NOT_RELEVANT = 3

