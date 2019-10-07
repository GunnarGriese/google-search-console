import pandas as pd

def parse_report(report, dimensions) -> pd.DataFrame:
    """ Function to parse date reports from Search Console 
    INPUT:
        report     - JSON storing the API response
        dimensions - dimensions passed to the request
    OUTPUT:
        df         - pd.DataFrame with response data
    """
    key_values = []
    clicks = []
    impressions = []
    ctr = []
    position = []

    for row in report["rows"]:
        key_values.append(row["keys"])
        clicks.append(row["clicks"])
        impressions.append(row["impressions"])
        ctr.append(row["ctr"])
        position.append(row["position"])

    df = pd.DataFrame(
        {'key_values': key_values,
        'clicks': clicks,
        'impressions': impressions,
        'ctr': ctr,
        'position': position
        })

    df[dimensions] = pd.DataFrame(df.key_values.values.tolist(), index= df.index)
    df.drop('key_values', axis=1, inplace=True)

    return df