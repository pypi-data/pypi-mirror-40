""" PYTW Client module """

import datetime
import urllib
from httplib2 import Http
import json

import drest
from drest import exc

import exceptions
import constants as Constants
import rating
import cve_vuln
import cve_vuln_coll
import impact_status
import impact
import impact_coll
import search_params
from asset import Asset as Asset
import asset_coll

class Client(object):
    """ User-created PYTW Client object.

    :param email: Email to identify the user
    :param key: API key to be used
    :param host: Host name to connect to for API calls. Note by default connects to ThreatWatch Cloud SaaS
    """
    
    def __init__(self, email, key, host="api.threatwatch.io"):
        if (host == ""):
            raise exceptions.PyTWError("Invalid argument - 'host'")
        if (email == ""):
            raise exceptions.PyTWError("Invalid argument - 'email'")
        if (key == ""):
            raise exceptions.PyTWError("Invalid argument - 'key'")
        self.__host = host
        self.__email = email
        self.__key = key

    def get_vulns(self, search_params):
        """
        :param search_params: An object of type SearchParams
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        api_url = Constants.HTTPS_PREFIX + self.__host + Constants.URL_FORWARD_SLASH + Constants.API_BASE_URL + Constants.API_VERSION_1
        extra_url_params = {"handle": self.__email, "token": self.__key}
        api = drest.API(api_url, serialize=True, extra_url_params=extra_url_params)

        # Prepare request parameters
        req_params = search_params.to_dict()
        req_headers = { "Accept": "application/json"}

        try:

            # Call REST API to retrieve recent threats
            response = api.make_request('POST', Constants.VULNS_URL, params=req_params, headers=req_headers)

        except exc.dRestRequestError as req_error:
            if (req_error.response.status == 404):
                return cve_vuln_coll.CVEVulnCollection()
            else:
                raise exceptions.PyTWError("REST API call to retrieve vulns failed")
    
        cve_vuln_collection = cve_vuln_coll.CVEVulnCollection()
        response_vulns = response.data["vulns"]
        for vuln in response_vulns:
            cve_vuln_collection.append(cve_vuln.CVEVuln(vuln))

        return cve_vuln_collection

    def get_vulns_by_vuln_ids(self, vuln_ids_list, window_start=None, offset=0, limit=-1):
        """
        :param vuln_ids_list: A list of vulnerability IDs to filter for.
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_vuln_ids_filter(vuln_ids_list)

        return self.get_vulns(search_params_var)

    def get_vulns_by_rating(self, ratings, window_start=None, offset=0, limit=-1):
        """
        :param ratings: A list of ratings (rating.Rating) to filter on.
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_ratings_filter(ratings)

        return self.get_vulns(search_params_var)

    def get_vulns_by_publisher(self, publishers, window_start=None, offset=0, limit=-1):
        """
        :param ratings: A list of publishers to filter on.
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_publishers_filter(publishers)

        return self.get_vulns(search_params_var)

    def get_vulns_by_threshold(self, threshold, window_start=None, offset=0, limit=-1):
        """
        :param threshold: The threshold to filter on.
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_threshold_filter(threshold)

        return self.get_vulns(search_params_var)

    def get_vulns_with_exploits(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only vulnerabilities from window_start days with exploits will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_exploitable_filter()

        return self.get_vulns(search_params_var)

    def get_vulns_with_patches(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only vulnerabilities from window_start days with patches will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_patch_available_filter()

        return self.get_vulns(search_params_var)

    def get_vulns_with_remediations(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only vulnerabilities from window_start days with remediations will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_remediation_available_filter()

        return self.get_vulns(search_params_var)

    def get_tracked_vulns(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve vulnerabilities
                Only tracked vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_tracked_vulns_filter()

        return self.get_vulns(search_params_var)

    def get_recent_vulns(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve recent vulnerabilities
                Only recent vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns a CVEVulnCollection object containing CVEVuln instances
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_recent_vulns_filter()

        return self.get_vulns(search_params_var)

    def get_impacts(self, search_params):
        """
        :param search_params: An object of type SearchParams
        :Returns an ImpactCollection object containing instances of Impact objects.
        """

        api_url = Constants.HTTPS_PREFIX + self.__host + Constants.URL_FORWARD_SLASH + Constants.API_BASE_URL + Constants.API_VERSION_1
        extra_url_params = {"handle": self.__email, "token": self.__key, "format": "json"}
        api = drest.API(api_url, serialize=True, extra_url_params=extra_url_params)

        # Prepare request parameters
        req_params = search_params.to_dict()
        req_headers = { "Accept": "application/json"}

        try:

            # Call REST API to retrieve recent threats
            response = api.make_request('POST', Constants.IMPACTS_URL, params=req_params, headers=req_headers)

        except exc.dRestRequestError as req_error:
            if (req_error.response.status == 404):
                return impact_coll.VulnImpactCollection()
            else:
                raise exceptions.PyTWError("REST API call to retrieve impacts failed")
    
        impact_collection = impact_coll.ImpactCollection()
        response_impacts = response.data["impacts"]
        for imp in response_impacts:
            impact_collection.append(impact.Impact(imp))

        return impact_collection

    def get_recent_impacts(self, window_start=None, threshold=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve recent impacts
                Only recent impacts from window_start days will be returned if specified.
        :param threshold: An optional threshold, only impacts with confidence greater than threshold will be returned
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_recent_impacts_filter()
        if threshold is not None:
           search_params_var.add_threshold_filter(threshold)

        return self.get_impacts(search_params_var)

    def get_impacts_by_asset_ids(self, asset_ids_list, window_start=None, offset=0, limit=-1):
        """
        :param asset_ids_list: A list of asset IDs to filter for.
        :param window_start: An optional number of days argument to retrieve impacts
                Only recent vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects which meet the criteria.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_asset_ids_filter(asset_ids_list)

        return self.get_impacts(search_params_var)

    def get_impacts_by_vuln_ids(self, vuln_ids_list, window_start=None, offset=0, limit=-1):
        """
        :param vuln_ids_list: A list of vuln IDs to filter for.
        :param window_start: An optional number of days argument to retrieve impacts
                Only recent vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects which meet the criteria.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_vuln_ids_filter(vuln_ids_list)

        return self.get_impacts(search_params_var)

    def get_impacts_by_rating(self, ratings, window_start=None, offset=0, limit=-1):
        """
        :param ratings: A list of ratings (rating.Rating) to filter on.
        :param window_start: An optional number of days argument to retrieve impacts
                Only recent vulnerabilities from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects which meet the criteria.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_ratings_filter(ratings)

        return self.get_impacts(search_params_var)

    def get_impacts_with_exploits(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve impacts
                Only impacts with exploits from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_exploitable_filter()

        return self.get_impacts(search_params_var)

    def get_impacts_with_patches(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve impacts
                Only impacts with patches from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects which have patches available.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_patch_available_filter()

        return self.get_impacts(search_params_var)

    def get_impacts_with_remediations(self, window_start=None, offset=0, limit=-1):
        """
        :param window_start: An optional number of days argument to retrieve impacts
                Only impacts with remediations from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects which have patches available.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_remediation_available_filter()

        return self.get_impacts(search_params_var)

    def get_impacts_by_threshold(self, threshold, window_start=None, offset=0, limit=-1):
        """
        :param threshold: Only Impacts with confidence higher than threshold will be returned
        :param window_start: An optional number of days argument to retrieve impacts
                Only impacts with confidence higher than threshold from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects.
        """

        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_threshold_filter(threshold)

        return self.get_impacts(search_params_var)

    def get_impacts_by_status(self, status_list, window_start=None, offset=0, limit=-1):
        """
        :param threshold: Only Impacts with specified status values will be returned
        :param window_start: An optional number of days argument to retrieve impacts
                Only impacts with confidence higher than threshold from window_start days will be returned if specified.
        :param offset: An optional offset indicating from where to start in the result set.
        :param limit: An optional limit indicate how many entries from offset to return in the result set.
        :Returns an ImpactCollection object containing instances of Impact objects.
        """
        search_params_var = search_params.SearchParams(window_start=window_start, offset=offset, limit=limit)
        search_params_var.add_impact_status_filter(status_list)

        return self.get_impacts(search_params_var)

    def update_impact(self, impact):
        """
        :param impact: The impact to be updated
        : Returns Response JSON with 'status' or None if the impact had no updates
        """

        if impact.is_updated() == False:
            return None

        api_url = Constants.HTTPS_PREFIX + self.__host + Constants.URL_FORWARD_SLASH + Constants.API_BASE_URL + Constants.API_VERSION_1
        extra_url_params = {"handle": self.__email, "token": self.__key, "format": "json"}
        api = drest.API(api_url, serialize=True, extra_url_params=extra_url_params)

        # Prepare request parameters
        req_params = search_params.SearchParams()
        req_params.add_asset_ids_filter([impact.get_asset_id()])
        req_params.add_vuln_ids_filter([impact.get_vuln_id()])
        req_params.add_products_filter([impact.get_affected_product()])
        req_params = req_params.to_dict(include_window_params=False)
        req_params[Constants.IMPACT_NEW_STATUS] = impact.get_status().name
        req_headers = { "Accept": "application/json"}

        try:

            # Call REST API to retrieve recent threats
            response = api.make_request('PATCH', Constants.IMPACTS_URL, params=req_params, headers=req_headers)

        except exc.dRestRequestError as req_error:
            raise exceptions.PyTWError("REST API call to update impact failed")
    
        return response.data

    def get_assets(self, search_params):
        """
        :param search_params: The search parameters for the search
        :Returns The specified asset object
        """

        api_url = Constants.HTTPS_PREFIX + self.__host + Constants.URL_FORWARD_SLASH + Constants.API_BASE_URL + Constants.API_VERSION_2

        # Prepare request parameters
        req_params = []
        search_params_dict = search_params.to_dict(include_window_params=False)
        asset_id = search_params_dict.get(Constants.SEARCH_PARAM_ASSET_ID)
        search_params_dict["handle"] = self.__email
        search_params_dict["token"] = self.__key
        search_params_dict["format"] = "json"
        req_headers = { "Accept": "application/json"}

        try:

            # Call REST API to retrieve recent threats
            if asset_id is not None:
                asset_url = api_url + Constants.ASSETS_URL + asset_id + Constants.URL_FORWARD_SLASH
            else:
                asset_url = api_url + Constants.ASSETS_URL
            asset_url = asset_url + '?' + urllib.urlencode(search_params_dict, True)
            http_obj = Http()
            response = http_obj.request(uri=asset_url, method='GET', headers=req_headers)

        except:
            raise exceptions.PyTWError("REST API call to retrieve specified asset failed")
        if asset_id is not None:
            asset_json = json.loads(response[1])
            ret_val = Asset(asset_json=asset_json)
        else:
            assets_json = json.loads(response[1])
            ret_val = asset_coll.AssetCollection() 
            for asset_json in assets_json:
                temp_asset = Asset(asset_json=asset_json)
                ret_val.append(temp_asset)

        return ret_val

    def get_asset_by_id(self, asset_id):
        """
        :param asset_id: Specifies ID of the asset to be retrieved.
        :Returns an Asset object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_asset_id_filter(asset_id)
        return self.get_assets(search_params_var)

    def get_assets_by_types(self, types_list):
        """
        :param types_list: Specifies the types of the assets to be retrieved.
        :Returns an AssetCollection object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_asset_types_filter(types_list)
        return self.get_assets(search_params_var)

    def get_assets_by_names(self, names_list):
        """
        :param names_list: Specifies the names of the assets to be retrieved.
        :Returns an AssetCollection object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_asset_names_filter(names_list)
        return self.get_assets(search_params_var)

    def get_assets_by_locations(self, locations_list):
        """
        :param locations_list: Specifies locations of the assets to be retrieved.
        :Returns an AssetCollection object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_asset_locations_filter(locations_list)
        return self.get_assets(search_params_var)

    def get_assets_by_product(self, product):
        """
        :param product: Retrieves assets containing specified product
        :Returns an AssetCollection object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_asset_product_filter(product)
        return self.get_assets(search_params_var)

    def get_assets_by_patch(self, patch):
        """
        :param patch: Retrieves assets containing specified patch
        :Returns an AssetCollection object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_asset_patch_filter(patch)
        return self.get_assets(search_params_var)

    def get_assets_with_open_impacts(self):
        """
        :Retrieves assets with open impacts
        :Returns an AssetCollection object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_asset_with_open_impacts_filter()
        return self.get_assets(search_params_var)

    def get_my_assets(self):
        """
        :Retrieves assets for current user
        :Returns an AssetCollection object.
        """
        search_params_var = search_params.SearchParams()
        search_params_var.add_my_asset_filter()
        return self.get_assets(search_params_var)

    def create_asset(self, asset):
        """
        :param asset: The asset to be created
        : Returns Response JSON with 'status'
        """

        api_url = Constants.HTTPS_PREFIX + self.__host + Constants.URL_FORWARD_SLASH + Constants.API_BASE_URL + Constants.API_VERSION_2
        extra_url_params = {"handle": self.__email, "token": self.__key, "format": "json"}
        api = drest.API(api_url, serialize=True, extra_url_params=extra_url_params)

        # Prepare request parameters
        req_params = asset.to_json()
        # Perform basic validation of the asset
        if req_params[Constants.ASSET_ID] == "" or req_params[Constants.ASSET_OWNER] == "":
            raise exceptions.PyTWError("Asset should contain Id and Owner")
        req_headers = { "Accept": "application/json"}

        try:

            # Call REST API to retrieve recent threats
            response = api.make_request('POST', Constants.ASSETS_URL, params=req_params, headers=req_headers)

        except exc.dRestRequestError as req_error:
            raise exceptions.PyTWError("REST API call to create asset failed")
    
        return response.data

    def update_asset(self, asset):
        """
        :param asset: The asset to be updated
        : Returns Response JSON with 'status' or None if asset had no changes
        """

        if asset.is_updated() == False:
            return None

        api_url = Constants.HTTPS_PREFIX + self.__host + Constants.URL_FORWARD_SLASH + Constants.API_BASE_URL + Constants.API_VERSION_2
        extra_url_params = {"handle": self.__email, "token": self.__key, "format": "json"}
        api = drest.API(api_url, serialize=True, extra_url_params=extra_url_params)

        # Prepare request parameters
        req_params = asset.to_json()
        asset_id = req_params[Constants.ASSET_ID]
        asset_url = Constants.ASSETS_URL + asset_id + Constants.URL_FORWARD_SLASH
        req_headers = { "Accept": "application/json"}

        try:

            # Call REST API to retrieve recent threats
            response = api.make_request('PUT', asset_url, params=req_params, headers=req_headers)

        except exc.dRestRequestError as req_error:
            raise exceptions.PyTWError("REST API call to update asset failed")
    
        return response.data

