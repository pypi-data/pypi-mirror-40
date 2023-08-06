import datetime

import core_vuln
import advisory_vuln
import constants as Constants

class CVEVuln(core_vuln.CoreVuln):
    """ CVE vulnerability object - derives from CoreVuln class
    """
    def __init__(self, vuln_json):
        super(CVEVuln, self).__init__(vuln_json)
        self.__related_vulns = vuln_json[Constants.VULN_RELATED_VULNS] if vuln_json.get(Constants.VULN_RELATED_VULNS) is not None else []
        self.__notional_last_modified_datetime = datetime.datetime.strptime(vuln_json[Constants.VULN_NOTIONAL_LAST_MODIFIED_DATETIME], "%Y-%m-%d %H:%M:%S") if vuln_json.get(Constants.VULN_NOTIONAL_LAST_MODIFIED_DATETIME) is not None else None
        self.__advisories = []
        for advisory in vuln_json[Constants.VULN_ADVISORIES]:
            self.__advisories.append(advisory_vuln.AdvisoryVuln(advisory))

    def get_related_vulns(self):
        """
        : Returns a list containing IDs of the related vulnerabilities
        """
        return self.__related_vulns

    def get_notional_last_modified_datetime(self):
        """
        : Returns the notional last modified datetime for the CVE and its advisories
          Note notional last modified datetime is the most recent last modified datetime for the CVE and its advisories
        """
        return self.__notional_last_modified_datetime

    def get_advisories(self):
        """
        : Returns an array of AdvisoryVulns which are referring to this CVE
        """
        return self.__advisories

    def get_patches(self, publisher=None):
        """
        : Returns the consolidated patches for this CVE across all its advisories.
        """
        patches = []
        for vuln in self.get_advisories():
            patches.extend(vuln.get_patches(publisher))
        return patches

    def get_remediations(self, publisher=None):
        """
        : Returns the consolidated remediations for this CVE across all its advisories.
        """
        remediations = []
        for vuln in self.get_advisories():
            remediations.extend(vuln.get_remediations(publisher))
        return remediations

    def get_exploits(self):
        """
        : Returns the consolidated exploits for this CVE across all its advisories.
        """
        exploits = []
        for vuln in self.get_advisories():
            exploits.extend(vuln.get_exploits())
        return exploits

    def get_references(self):
        """
        : Returns the consodlidated references for this CVE across all its advisories.
        """
        refs_list = []
        cve_references = super(CVEVuln, self).get_references()
        if (cve_references is not None):
            refs_list.extend(cve_references)
        for vuln in self.get_advisories():
            refs_list.extend(vuln.get_references())
        refs_set = set(refs_list)
        return list(refs_set)

