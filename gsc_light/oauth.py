from google_auth_oauthlib import flow
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient import discovery

#import gsc_client as gsc
from . import gsc_client


def authenticate_to_gsc(CLIENT_SECRET_FILE, AUTH_SCOPES):
    if CLIENT_SECRET_FILE:
        appflow = flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=AUTH_SCOPES
        )
    else:
        "Please provide valid client secrets."

    appflow.run_console()

    credentials = appflow.credentials

    authed_http = AuthorizedHttp(credentials)

    api_name = "webmasters"
    api_version = "v3"

    # Build the client for Search Console API
    api_client = discovery.build(serviceName=api_name, version=api_version, http=authed_http)

    return gsc.GSCClient(api_client, credentials)
    #return gsc_client.GSCClient(api_client, credentials)