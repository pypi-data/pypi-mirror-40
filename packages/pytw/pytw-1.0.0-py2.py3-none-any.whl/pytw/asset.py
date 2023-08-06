import json
import copy

import constants as Constants
import exceptions

class Asset(object):

    """ Asset object.

    :param asset_json: Asset JSON (which should contain 'id' at minimum)
    :param id: Specifies the Id for the asset.
    Note either parameter should be present.
    """
    def __init__(self, id=None, asset_json=None):
        self.__is_dirty = False
        if id is not None:
            self.__id = id
        elif asset_json is not None and asset_json.get(Constants.ASSET_ID) is not None:
            self.__id = asset_json[Constants.ASSET_ID] if asset_json is not None else None
        else:
            raise exceptions.PyTWError("Unable to instantiate Asset without Id")
        self.__name = asset_json[Constants.ASSET_NAME] if asset_json is not None and asset_json.get(Constants.ASSET_NAME) is not None else ""
        self.__type = asset_json[Constants.ASSET_TYPE] if asset_json is not None and asset_json.get(Constants.ASSET_TYPE) is not None else ""
        self.__description = asset_json[Constants.ASSET_DESCRIPTION] if asset_json is not None and asset_json.get(Constants.ASSET_DESCRIPTION) is not None else ""
        self.__location = asset_json[Constants.ASSET_LOCATION] if asset_json is not None and asset_json.get(Constants.ASSET_LOCATION) is not None else ""
        self.__owner = asset_json[Constants.ASSET_OWNER] if asset_json is not None and asset_json.get(Constants.ASSET_OWNER) is not None else ""
        self.__notify = asset_json[Constants.ASSET_NOTIFY] if asset_json is not None and asset_json.get(Constants.ASSET_NOTIFY) is not None else []
        self.__products = asset_json[Constants.ASSET_PRODUCTS] if asset_json is not None and asset_json.get(Constants.ASSET_PRODUCTS) is not None else []
        self.__patches = asset_json[Constants.ASSET_PATCHES] if asset_json is not None and asset_json.get(Constants.ASSET_PATCHES) is not None else []
        self.__tags = asset_json[Constants.ASSET_TAGS] if asset_json is not None and asset_json.get(Constants.ASSET_TAGS) is not None else []

    def get_id(self):
        """
        :Returns a string containing the Asset ID
        """
        return self.__id

    def get_asset_name(self):
        """
        :Returns a string containing the asset name
        """
        return self.__name

    def set_asset_name(self, name):
        """
        :Sets the asset name
        """
        self.__name = name
        self.__is_dirty = True

    def get_type(self):
        """
        :Returns a string containing the type of the asset
        """
        return self.__type

    def set_type(self, type):
        """
        :Set the type of the asset
        """
        self.__type = type
        self.__is_dirty = True

    def get_description(self):
        """
        :Returns a string containing the description of the asset
        """
        return self.__description

    def set_description(self, description):
        """
        :Set the description of the asset
        """
        self.__description = description
        self.__is_dirty = True

    def get_location(self):
        """
        :Returns the location for the asset
        """
        return self.__location

    def set_location(self, location):
        """
        :Set the location for the asset
        """
        self.__location = location
        self.__is_dirty = True

    def get_owner(self):
        """
        :Returns a string containing the owner of the asset
        """
        return self.__owner

    def set_owner(self, owner):
        """
        :Set the owner of the asset
        """
        self.__owner = owner
        self.__is_dirty = True

    def get_notify(self):
        """
        :Returns the notification list for the asset
        """
        return self.__notify

    def set_notify(self, notify_list):
        """
        :Set the notification list for the asset
        """
        self.__notify = notify_list
        self.__is_dirty = True

    def get_products(self):
        """
        :Returns the list of products for the asset
        """
        return self.__products

    def set_products(self, products_list):
        """
        :Set the list of products for the asset
        """
        self.__products = products_list
        self.__is_dirty = True

    def get_patches(self):
        """
        :Returns the list of patches for the asset
        """
        return self.__patches

    def set_patches(self, patches_list):
        """
        :Set the list of patches for the asset
        """
        self.__patches = patches_list
        self.__is_dirty = True

    def get_tags(self):
        """
        :Returns the list of tags for the asset
        """
        return self.__tags

    def set_tags(self, tags_list):
        """
        :Set the list of tags for the asset
        """
        self.__tags = tags_list
        self.__is_dirty = True

    def is_updated(self):
        """
        :Returns True if asset has been modified
        """
        return self.__is_dirty

    def to_json(self):
        """
        :Returns JSON representation of the object
        """
        self.__asset_json = {}
        self.__asset_json[Constants.ASSET_ID] = self.__id
        self.__asset_json[Constants.ASSET_NAME] = self.__name
        self.__asset_json[Constants.ASSET_TYPE] = self.__type
        self.__asset_json[Constants.ASSET_DESCRIPTION] = self.__description
        self.__asset_json[Constants.ASSET_LOCATION] = self.__location
        self.__asset_json[Constants.ASSET_OWNER] = self.__owner
        self.__asset_json[Constants.ASSET_NOTIFY] = self.__notify
        self.__asset_json[Constants.ASSET_PRODUCTS] = self.__products
        self.__asset_json[Constants.ASSET_PATCHES] = self.__patches
        self.__asset_json[Constants.ASSET_TAGS] = self.__tags

        return self.__asset_json

    def __str__(self):
        return json.dumps(self.to_json())

