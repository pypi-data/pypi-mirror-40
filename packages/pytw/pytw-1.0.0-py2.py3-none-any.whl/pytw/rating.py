import enum

class Rating(enum.Enum):
    """
    Rating defines the enum of ratings, enumeration values as follows: Unknown = 0, Low = 1, Medium = 2, Severe = 3, Critical = 4, Urgent = 5.
    """
    Unknown = 0
    Low = 1
    Medium = 2
    Severe = 3
    Critical = 4
    Urgent = 5

