import pandas as pd
import requests
import json

def append_catalog_item(item, lab_reference):
    # USED FOR CATALOG VIEWING/SYNCING
    # lab_reference.append({'Content ID': item['content_id'], 'Lab Title': item['title'], 'Content Type': item['content_type'], 'Public Catalog': False, 'Googler Catalog': False, 'Reseller Catalog': False, 'Google Solutions': False})
    lab_reference.append({'Content ID': item['content_id'], 'Lab Title': item['title'], 'Content Type': item['content_type'], 'Catalog1': False, 'Catalog2': False})
    # lab_reference.append({'Content ID': item['content_id'], 'Lab Title': item['title'], 'Description': item['description'], 'Tags': item['tags']})

def add_catalog(catalog_data, catalog_name, lab_reference, title_lookup):
    for item in catalog_data:
        if item['title'] in title_lookup.keys():
            lab_reference[title_lookup[item['title']]][catalog_name] = True
        else:
            append_catalog_item(item, lab_reference)
            lab_reference[-1][catalog_name] = True
            title_lookup[item['title']] = len(lab_reference) - 1

def build_dataframe(catalog_data):
    lab_reference = [{}]
    # store titles/indexes in dict for faster lookups
    title_lookup = {}

    #TODO: use lab name rather than index number
    for idx, catalog in enumerate(catalog_data):
        json_data = json.loads(catalog)
        add_catalog(json_data, 'Catalog' + str(idx + 1), lab_reference, title_lookup)

    df = pd.DataFrame(data=lab_reference)
    return df


### Sample JSON Object Item:

### {"content_id":"gcp-spl-content/gsp064-cloud-iam-qwik-start","content_type":"Lab","title":"Cloud IAM: Qwik Start","description":"Google Cloud IAM unifies access control for Cloud Platform services into a single system to present a consistent set of operations. Watch the short video \u003cA HREF=\"https://youtu.be/PqMGmRhKsnM\"\u003eManage Access Control with Google Cloud IAM\u003c/A\u003e.","duration":2700,"level":1,"available_locales":["en","de","es","fr","id","it","ja","ko","pl","pt_BR","tr"],"tags":["GSP064","IAM","Identity","Access Management","users","roles","permissions","Game"],"lti_uri":"https://google-run.qwiklabs.com/lti_sessions/libraries/gcp-spl-content/content/gsp064-cloud-iam-qwik-start","content_catalog_url":"https://google-run.qwiklabs.com/focuses/74?parent=catalog"}