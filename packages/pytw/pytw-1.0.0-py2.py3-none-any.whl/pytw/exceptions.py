
class PyTWError(Exception):
    """ PYTW Errors """
    """
        :param msg: Message for the exception raised
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "<pytw_error: %s>" % self.msg

    def __str__(self):
        return str(self.msg)

