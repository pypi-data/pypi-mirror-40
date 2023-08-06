import json

import constants as Constants

class SearchParams(object):
    """ SearchParams object 

    :param window_start: Number of days in the past to start search. Default is 1 day ago.
    :param window_end: Number of days in the past to end search. Default is 0 i.e. today.
    :param offset: Offset in result set. Used for pagination. Default is to start from first record.
    :param limit: Number of records to be returned. Used for pagination. Default is all records. 
    """
    
    def __init__(self, window_start=None, window_end=None, offset=None, limit=None):
        self.__window_start = window_start if window_start is not None else 1
        self.__window_end = window_end if window_end is not None else 0
        self.__offset = offset if offset is not None else 0
        self.__limit = limit if limit is not None else -1
        self.__ratings = None
        self.__publishers = None
        self.__free_text_search = None
        self.__asset_ids = None
        self.__vuln_ids = None
        self.__products = None
        self.__threshold = None
        self.__impact_status = None
        self.__asset_id = None
        self.__asset_types = None
        self.__asset_names = None
        self.__asset_locations = None
        self.__asset_product = None
        self.__asset_patch = None
        self.__predefined_filters = []

    def add_ratings_filter(self, ratings_list):
        """ 
        :param ratings_list: A list of rating.Rating enum values to filter on.
        """
        self.__ratings = []
        for r in ratings_list:
            self.__ratings.append(str(r.value))

    def add_publishers_filter(self, publishers_list):
        """
        :param publishers_list: A list of publishers to filter on.
        """
        self.__publishers = []
        self.__publishers.extend(publishers_list)

    def add_free_text_search_filter(self, search_text):
        """
        :search_text: The text to be searched on. 
        For vulns, it applies to vuln IDs, title, summary or affected products.
        For impacts, it applies to asset IDs, asset names, vuln IDs or affected products.
        """
        self.__free_text_search = search_text

    def add_asset_ids_filter(self, asset_ids_list):
        """
        :param asset_ids_list: A list of asset IDs to filter on.
        """
        self.__asset_ids = []
        self.__asset_ids.extend(asset_ids_list)

    def add_vuln_ids_filter(self, vuln_ids_list):
        """
        :param vuln_ids_list: A list of vuln IDs to filter on.
        """
        self.__vuln_ids = []
        self.__vuln_ids.extend(vuln_ids_list)

    def add_products_filter(self, products_list):
        """
        :param products_list: A list of products to filter on.
        """
        self.__products = []
        self.__products.extend(products_list)

    def add_threshold_filter(self, threshold):
        """
        :param threshold: Return only results which cross the threshold.
        For Vulns, get vulnerabilities with relevance greater than or equal to threshold.
        For Impacts, get impact with confidence values greater than or equal to threshold.
        """
        self.__threshold = threshold

    def add_impact_status_filter(self, status_list):
        """
        :param status_list: A list of impact_status.Status enum values to filter by.
        """
        self.__impact_status = []
        for s in status_list:
            self.__impact_status.append(s.name.lower())

    def add_asset_id_filter(self, asset_id):
        """
        :param asset_id: The asset ID of the asset to retrieve
        """
        self.__asset_id = asset_id

    def add_asset_types_filter(self, types_list):
        """
        :param types_list: A list of asset types to filter by.
        """
        self.__asset_types = []
        self.__asset_types.extend(types_list)

    def add_asset_names_filter(self, names_list):
        """
        :param names_list: A list of asset names to filter by.
        """
        self.__asset_names = []
        self.__asset_names.extend(names_list)

    def add_asset_locations_filter(self, locations_list):
        """
        :param locations_list: A list of locations to filter by.
        """
        self.__asset_locations = []
        self.__asset_locations.extend(locations_list)

    def add_asset_product_filter(self, product):
        """
        :param product: Filter assets containing specified product 
        """
        self.__asset_product = product

    def add_asset_patch_filter(self, patch):
        """
        :param patch: Filter assets containing specified patch 
        """
        self.__asset_patch = patch

    def add_asset_with_open_impacts_filter(self):
        """
        Filter only assets with open impacts
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_ASSETS_WITH_OPEN_IMPACTS)

    def add_my_asset_filter(self):
        """
        Filter only my assets
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_MY_ASSETS)

    def add_recent_vulns_filter(self):
        """
        Filter only recent vulns i.e. not yet notified.
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_RECENT)

    def add_tracked_vulns_filter(self):
        """
        Filter only vulns tracked by user.
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_TRACKED_VULNS)

    def add_recent_impacts_filter(self):
        """
        Filter only recent impacts i.e. not yet notified.
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_RECENT)

    def add_threatfilter_filter(self):
        """
        Filter by threatfilter of user.
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_THREATFILTER)

    def add_exploitable_filter(self):
        """
        Filter only results with exploits.
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_EXPLOITABLE)

    def add_patch_available_filter(self):
        """
        Filter only results with patches available.
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_PATCH_AVAILABLE)

    def add_remediation_available_filter(self):
        """
        Filter only results with remediations available.
        """
        self.__predefined_filters.append(Constants.SEARCH_FILTER_REMEDIATION_AVAILABLE)

    def to_dict(self, include_window_params = True):
        """ 
        Convert the SearchParams to a dict object
        """
        dict_obj = {}
        if include_window_params == True:
            dict_obj[Constants.SEARCH_PARAM_WINDOW_START] = self.__window_start
            dict_obj[Constants.SEARCH_PARAM_WINDOW_END] = self.__window_end
            dict_obj[Constants.SEARCH_PARAM_OFFSET] = self.__offset
            dict_obj[Constants.SEARCH_PARAM_LIMIT] = self.__limit
        if self.__ratings is not None:
            dict_obj[Constants.SEARCH_PARAM_RATINGS] = self.__ratings
        if self.__publishers is not None:
            dict_obj[Constants.SEARCH_PARAM_PUBLISHERS] = self.__publishers
        if self.__free_text_search is not None:
            dict_obj[Constants.SEARCH_PARAM_FREE_TEXT_SEARCH] = self.__free_text_search
        if self.__asset_ids is not None:
            dict_obj[Constants.SEARCH_PARAM_ASSET_IDS] = self.__asset_ids
        if self.__vuln_ids is not None:
            dict_obj[Constants.SEARCH_PARAM_VULN_IDS] = self.__vuln_ids
        if self.__products is not None:
            dict_obj[Constants.SEARCH_PARAM_PRODUCTS] = self.__products
        if self.__threshold is not None:
            dict_obj[Constants.SEARCH_PARAM_THRESHOLD] = self.__threshold
        if self.__impact_status is not None:
            dict_obj[Constants.SEARCH_PARAM_IMPACT_STATUS] = self.__impact_status
        if self.__asset_id is not None:
            dict_obj[Constants.SEARCH_PARAM_ASSET_ID] = self.__asset_id
        if self.__asset_names is not None:
            dict_obj[Constants.SEARCH_PARAM_ASSET_NAMES] = self.__asset_names
        if self.__asset_types is not None:
            dict_obj[Constants.SEARCH_PARAM_ASSET_TYPES] = self.__asset_types
        if self.__asset_locations is not None:
            dict_obj[Constants.SEARCH_PARAM_ASSET_LOCATIONS] = self.__asset_locations
        if self.__asset_product is not None:
            dict_obj[Constants.SEARCH_PARAM_ASSET_PRODUCT] = self.__asset_product
        if self.__asset_patch is not None:
            dict_obj[Constants.SEARCH_PARAM_ASSET_PATCH] = self.__asset_patch
        if len(self.__predefined_filters) > 0:
            dict_obj[Constants.SEARCH_PARAM_FILTERS] = self.__predefined_filters
    
        return dict_obj

    def __str__(self):
        d = self.to_dict()
        s = json.dumps(d)
        return s

