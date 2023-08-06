import core_vuln

class AdvisoryVuln(core_vuln.CoreVuln):
    """ A vulnerability advisory object - derives from CoreVuln class
    """
    def __init__(self, vuln_json):
        super(AdvisoryVuln, self).__init__(vuln_json)

