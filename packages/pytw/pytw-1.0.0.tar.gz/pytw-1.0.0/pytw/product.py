import json
import copy

import constants as Constants

class Product(object):
    """ Product object
    Consists of {name, version, vendor} fields
    """
    def __init__(self, product_json):
        self.__product_json = product_json
        self.__name = self.__product_json[Constants.VULN_PRODUCT_NAME]
        self.__vendor = self.__product_json[Constants.VULN_PRODUCT_VENDOR]
        self.__version = self.__product_json[Constants.VULN_PRODUCT_VERSION]

    def get_name(self):
        """
        :Returns the name of the product
        """
        return self.__name

    def get_vendor(self):
        """
        :Returns the name of the vendor for the product
        """
        return self.__vendor

    def get_version(self):
        """
        :Returns the version of the product
        """
        return self.__version

    def to_json(self):
        """
        :Returns JSON representation of the object
        """
        return copy.deepcopy(self.__product_json)

    def __str__(self):
        return json.dumps(self.__product_json)

    def __repr__(self):
        return json.dumps(self.__product_json)


def json2products(products_json):
    products = []
    for p in products_json:
        products.append(Product(p))
    return products
