import json
import copy

import constants as Constants

class Remediation(object):
    """ Remediation object
    Consisting of URL and Description fields
    """

    def __init__(self, remediation_json):
        self.__remediation_json = remediation_json
        self.__description = self.__remediation_json[Constants.VULN_REMEDIATION_DESCRIPTION]
        self.__url = self.__remediation_json[Constants.VULN_REMEDIATION_URL]

    def get_description(self):
        """
        : Returns the description for the remediation
        """
        return self.__description

    def get_url(self):
        """
        : Returns the URL for the remediation
        """
        return self.__url

    def to_json(self):
        """
        :ReturnsJSON representation of the object
        """
        return copy.deepcopy(self.__remediation_json)

    def __str__(self):
        return json.dumps(self.__remediation_json)

    def __repr__(self):
        return json.dumps(self.__remediation_json)


def json2remediations(remediations_json):
    remediations = []
    for r in remediations_json:
        remediations.append(Remediation(r))
    return remediations


