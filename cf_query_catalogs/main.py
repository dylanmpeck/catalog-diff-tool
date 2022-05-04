import subprocess
import requests
import build_reference_table
import os
import json

# API Keys referenced from secret manager
AK_VALUE = os.environ.get("AK_VALUE")
SK_VALUE = os.environ.get("SK_VALUE")
QL_URL = "https://google.qwiklabs.com/api/v2/"

CE_AK_VALUE = os.environ.get("CE_AK_VALUE")
CE_SK_VALUE = os.environ.get("CE_SK_VALUE")
CE_URL = "https://ce.qwiklabs.com/api/v2/"

def get_catalog_from_url(url):
    return(url.rsplit('/', 1)[-1])

def query_catalog(domain, catalog, token):
    MAX_ITEMS = "1000"
    ## Example URL: "https://google.qwiklabs.com/api/v2/catalogs/gcp-self-paced-labs-all-public/items?per_page=1000"
    URL = domain + 'catalogs/' + catalog + '/items?per_page=' + MAX_ITEMS
    headers = {'Authorization': 'Bearer ' + token }
    r = requests.get(URL, headers=headers)
    return(r.text)

def get_token(URL, access_key, secret_key):
    headers = {'accept': 'application/json'}
    r = requests.post(URL, headers=headers, data={'access_key': access_key, 'secret_key': secret_key})
    if r.json()['auth_token'] == None:
        raise ValueError('Token is null. Your credentials are not valid.')
    return(r.json()['auth_token'])

def get_catalog_items(catalog_url):
    catalog = get_catalog_from_url(catalog_url)
    if 'google.qwiklabs.com' in catalog_url or 'cloudskillsboost.google' in catalog_url or 'googlesolutions' in catalog_url:
        token = get_token(QL_URL + 'authenticate', AK_VALUE, SK_VALUE)
        return query_catalog(QL_URL, catalog, token)
    elif 'ce.qwiklabs.com' in catalog_url:
        token = get_token(CE_URL + 'authenticate', CE_AK_VALUE, CE_SK_VALUE)
        return query_catalog(CE_URL, catalog, token)
    else:
        raise ValueError('Catalog URL is not supported. Ensure the link is correct or contact dylanmpeck@google.com to request an addition.')
    return None

#### Hard coded variables for local testing
#catalog1_url = "https://ce.qwiklabs.com/authoring/catalogs/entire-catalog-for-ce-instance-of-qwiklab-76a67879"
#catalog2_url = "https://googlesolutions.qwiklabs.com/authoring/catalogs/google-solutions-all-free-to-google"
# print(output)
#public_items = lab_reference_df[lab_reference_df['Public Catalog']==False & lab_reference_df['Content Type'].str.contains('Lab')]['Lab Title'].tolist()


def get_diff(request):
 # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Allow GET requests to check permissions
    if request.method == 'GET':
        headers = {
            'Access-Control-Allow-Origin': '*'
        }

        return ('', 200, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
    }

    catalog1_url = request.get_json().get('catalog1_url')
    catalog2_url = request.get_json().get('catalog2_url')

    catalog_data_list = []
    catalog_data_list.append(get_catalog_items(catalog1_url))
    catalog_data_list.append(get_catalog_items(catalog2_url))

    lab_reference_df = build_reference_table.build_dataframe(catalog_data_list)

    # output = "Catalog 1 is missing these labs from Catalog 2:\n\n"

    catalog1_missing_labs = lab_reference_df[lab_reference_df['Catalog1']==False & lab_reference_df['Content Type'].str.contains('Lab')].to_dict()
    catalog2_missing_labs = lab_reference_df[lab_reference_df['Catalog2']==False & lab_reference_df['Content Type'].str.contains('Lab')].to_dict()

    d = {}
    d["catalog1"] = catalog1_missing_labs
    d["catalog2"] = catalog2_missing_labs

    # TODO: Too many unnecessary conversions between json/dict/pandas - Simplify CF to only return API output and do diff in CR?
    to_json = json.dumps(d)

    return to_json