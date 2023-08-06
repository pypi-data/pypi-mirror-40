import constants as Constants

class CVEVulnCollection(list):
    
    """ CVEVulnCollection is a collection of CVEVuln objects
    :param seq: An optional seq(list) of CVEVuln objects
    """

    def __init__(self, seq = []):
        super(CVEVulnCollection, self).__init__(seq)

    def __filterVulnsWithUpdatedField(self, updated_field):
        filtered_cve_vuln_collection = CVEVulnCollection()
        filtered_vulns = []
        for cve in self:
            last_changed = cve.get_last_change()
            for changed_field in last_changed:
                if(changed_field == updated_field):
                    filtered_vulns.append(cve)
        return CVEVulnCollection(filtered_vulns)
                    
    def filterVulnsWithUpdatedPatches(self):
        """
        :Returns a CVEVulnCollection of filtered vulnerabilities with recently updated patches
        """
        return self.__filterVulnsWithUpdatedField(Constants.VULN_PATCHES)

    def filterVulnsWithUpdatedRemediations(self):
        """
        :Returns a CVEVulnCollection of filtered vulnerabilities with recently updated remediations
        """
        return self.__filterVulnsWithUpdatedField(Constants.VULN_REMEDIATIONS)

    def filterVulnsWithUpdatedExploits(self):
        """
        :Returns a CVEVulnCollection of filtered vulnerabilities with recently updated exploits
        """
        return self.__filterVulnsWithUpdatedField(Constants.VULN_EXPLOITS)

    def __str__(self):
        self_str = "[ "
        for cve in self:
            self_str = self_str + str(cve) + " , "
        self_str = self_str[:-2]
        self_str = self_str + " ]"
        return self_str
