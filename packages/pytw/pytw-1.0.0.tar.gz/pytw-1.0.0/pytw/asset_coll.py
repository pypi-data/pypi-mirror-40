import constants as Constants

class AssetCollection(list):
    
    """ AssetCollection is a collection of Asset objects
    :param seq: An optional seq(list) of Asset objects
    """

    def __init__(self, seq = []):
        super(AssetCollection, self).__init__(seq)
                    
    def __str__(self):
        self_str = "[ "
        for impact in self:
            self_str = self_str + str(impact) + " , "
        self_str = self_str[:-2]
        self_str = self_str + " ]"
        return self_str
