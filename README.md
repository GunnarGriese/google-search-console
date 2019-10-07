A simplified, object-oriented helper library for the [Google Search Console API](https://developers.google.com/webmaster-tools/search-console-api-original). This package only covers basic API calls and was mainly created for practice purposes. To get the full Google Search Console API experience see Josh Carty's [python wrapper](https://github.com/joshcarty/google-searchconsole).


## Getting Started

Install the library on your local machine.

```bash
pip3 install gsclight
```

Use a Google account to create application credentials, download the JSON file and put it in the same directory as your script with the name `client_secret.json`. Every execution of any API-dependent library code,will prompt to perform the auth flow.

```python
from gsclight import oauth

CLIENT_SECRET = "../client_secret.json"
AUTH_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
account = oauth.authenticate_to_gsc(CLIENT_SECRET, AUTH_SCOPE)
```

Use the Google Search Console wrapper to get an overview of all sites your personal account has access as well as all sites your account is verified for (meaning you can request data via the API).

```python
account.list_all_urls()
account.list_verified_urls()
```

To access data programmatically via the API specify the URI, date range as well as the dimensions your report should contain (metrics always consist of `clicks`, `impressions`, `ctr` and `position`). Filters are currently not implemented. The row limit is set to 25,000 rows and can not be adjusted. If you exceed the row limit try to request smaller chunks of data (e.g. apply smaller date range). Per default the search type `web` is used, but this can be adjusted to `image` or `video`.

```python
report, dimensions = account.get_data('https://www.my-website.com/', "2019-09-02", "2019-09-03", 'date', 'device')
```

In order to use the Google Search Console API response for further analysis the library comes with a built-in function to parse the reports to human-readable dataframes.

```python
from gsclight import parse_report as p
df = p.parse_report(report, dimensions)

df.head()
```

## Authentication & Client Secrets

This library currently only supports user-based OAuth crendentials. Service accounts can not be used.

The Google OAuth flows requires you to provide a [client id and secret](https://cloud.google.com/docs/authentication/end-user) in the from of a `JSON` file. You can create these in any Google Cloud or Google Developer project:

> 1. Open the [Google API Console Credentials](https://console.developers.google.com/apis/credentials) page.
> 2. Optional: From the project drop-down, choose Create a new project, enter a name for the project, and optionally, edit the provided Project ID. Click `Create`.
> 3. On the Credentials page, select `Create credentials`, then select `OAuth client ID`.
> 4. Select `Other` for the Application type, and enter any additional information required.
> 5. Click `Create`.
> 6. On the page that appears, you can download client id and secret as a JSON file.
