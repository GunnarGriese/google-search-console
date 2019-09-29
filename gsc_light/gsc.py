from apiclient import discovery
from google.oauth2.credentials import Credentials
from googleapiclient import sample_tools
import httplib2 as lib2 
from oauth2client import client

def authenticate_to_gsc(access_token, refresh_token, client_id, client_secret, token_uri, token_expiry, user_agent):
    # Instantiate API client
    credentials = client.GoogleCredentials(access_token=access_token, refresh_token=refresh_token, 
                                       client_id= client_id, client_secret=client_secret, 
                                       token_uri=token_uri, token_expiry=token_expiry, 
                                       user_agent=user_agent)

    # Initialize HTTP Protocol    
    http = lib2.Http()

    # Authorize client
    authorized = credentials.authorize(http)

    # API Name and Version, these do not change (until new api release)
    api_name = "webmasters"
    api_version = "v3"

    # Build the client for Search Console API
    api_client = discovery.build(serviceName=api_name, version=api_version, http=authorized)

    return api_client

# Retrieve list of all available properties in account
def list_all_urls(api_client):
    """ 
    Retrieve all available accounts to which the provided API client has access. 
    
    INPUT:
    
        api_client - googleapiclient.discovery.Resource
    
    OUTPUT:
    
        site_list - list with available site URLs from Search Console
    
    """
    site_list = api_client.sites().list().execute()

    return site_list

# Retrieve list of verified properties in account
def list_verified_urls(api_client):
    """ 
    Retrieve all available accounts to which the provided API client has access. 
    
    INPUT:
    
        api_client - googleapiclient.discovery.Resource
    
    OUTPUT:
    
        site_urls - list with verified site URLs from Search Console
    
    """
    
    site_list = api_client.sites().list().execute()
    verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry'] \
    if s['permissionLevel'] != 'siteUnverifiedUser' \
        and s['siteUrl'][:4] == 'http']

    return verified_sites_urls


def execute_request(api_client, uri: str, start_date: str, end_date: str, *dimensions, search_type="web"):
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
    report = api_client.searchanalytics().query(siteUrl=uri, body=request).execute()
    return report