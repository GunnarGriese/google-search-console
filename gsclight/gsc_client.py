import pandas as pd

class GSCClient:
    """ API Client for Google Search Console """

    def __init__(self, service, credentials):
        """ Instantiate service """
        self.service = service
        self.credentials = credentials

    # Retrieve list of all available properties in account
    def list_all_urls(self):
        """ 
        Retrieve all available accounts to which the provided API client has access. 
    
        INPUT:
    
            api_client - googleapiclient.discovery.Resource
    
        OUTPUT:
    
            site_list - list with available site URLs from Search Console
    
        """
        site_list = self.service.sites().list().execute()

        return site_list

    # Retrieve list of verified properties in account
    def list_verified_urls(self):
        """ 
        Retrieve all available accounts to which the provided API client has access. 
    
        INPUT:
    
            api_client - googleapiclient.discovery.Resource
    
        OUTPUT:
    
            site_urls - list with verified site URLs from Search Console
    
        """
    
        site_list = self.service.sites().list().execute()
        verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry'] \
        if s['permissionLevel'] != 'siteUnverifiedUser' \
            and s['siteUrl'][:4] == 'http']

        return verified_sites_urls

    

    def get_data(self, uri: str, start_date: str, end_date: str, *dimensions, search_type="web"):
        # TO DO: Implement filters
        """
        Build the request's payload based on the input parameters and execute request 
        to retrieve requested report.
    
        INPUT:
    
            account     - Account
            search_type - "image", "video ,"web" (default)
            uri         - URI as source of the report
            start_date  - Beginning of date range (format "%Y-%m-%d")
            end_date    - End of date range (format "%Y-%m-%d")
            dimensions  - specify the dimensions you would like report on (date, country,
                            device, page, query, searchAppearance)
    
        OUTPUT:
        
            report     - JSON storing the requested data
        """

        # Define request's body
        request = {
            'searchType': search_type,
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': list(dimensions),
            'rowLimit': 25000,
            'startRow': 0
        }
        # Send request to Search Console API
        report = self.service.searchanalytics().query(siteUrl=uri, body=request).execute()
        return report, list(dimensions)
    