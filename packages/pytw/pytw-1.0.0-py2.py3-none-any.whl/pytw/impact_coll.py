import constants as Constants

class ImpactCollection(list):
    
    """ ImpactCollection is a collection of Impact objects
    :param seq: An optional seq(list) of Impact objects
    """

    def __init__(self, seq = []):
        super(ImpactCollection, self).__init__(seq)

    def filterImpactsByAsset(self, asset_id):
        """
        :Returns a ImpactCollection of filtered Impact by given asset 
        """
        filtered_impact_collection = ImpactCollection()
        for impact in self:
            if (impact.get_asset_id() == asset_id):
                filtered_impact_collection.append(impact)
        return filtered_impact_collection

    def filterImpactsByProduct(self, product):
        """
        :Returns a ImpactCollection of filtered Impact by given product
        """
        filtered_impact_collection = ImpactCollection()
        for impact in self:
            if (impact.get_product() == product):
                filtered_impact_collection.append(impact)
        return filtered_impact_collection
                    
    def __str__(self):
        self_str = "[ "
        for impact in self:
            self_str = self_str + str(impact) + " , "
        self_str = self_str[:-2]
        self_str = self_str + " ]"
        return self_str
