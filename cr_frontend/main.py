import subprocess
import requests
import os
import urllib
import json
import pandas as pd

import google.auth.transport.requests
import google.oauth2.id_token

from flask import Flask, request, render_template
app = Flask(__name__)

CATALOG_DIFF_CF_URL = "https://us-central1-qwiklabs-resources.cloudfunctions.net/catalog-diff"

def get_catalog_from_url(url):
    return(url.rsplit('/', 1)[-1])

def catalog_diff_request(catalog1_url, catalog2_url):
    """
    new_request creates a new HTTP request with IAM ID Token credential.
    This token is automatically handled by private Cloud Run (fully managed)
    and Cloud Functions.
    """

    url = CATALOG_DIFF_CF_URL
    # if not url:
    #   raise Exception(CATALOG_DIFF_CF_URL + " missing")

    auth_req = google.auth.transport.requests.Request()
    target_audience = url

    id_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)

    headers = {'Authorization': f"Bearer {id_token}", "Content-Type": "application/json" }
    return requests.post(url, headers=headers, json={"catalog1_url": catalog1_url, "catalog2_url": catalog2_url})

    

#catalog1_url = "https://ce.qwiklabs.com/authoring/catalogs/entire-catalog-for-ce-instance-of-qwiklab-76a67879"
#catalog2_url = "https://googlesolutions.qwiklabs.com/authoring/catalogs/google-solutions-all-free-to-google"

@app.route('/', methods=['GET'])
def home_page():
    return render_template('my-form.html')

@app.route('/noaccess', methods=['GET'])
def access_denied():
    return render_template('access-denied.html')

@app.route('/display', methods=['POST'])
def display_diff():
    catalog1_url = request.form['catalog1_url']
    catalog2_url = request.form['catalog2_url']

    # call cloud function
    r = catalog_diff_request(catalog1_url, catalog2_url)

    catalog1_missing_labs = pd.DataFrame.from_dict(r.json()['catalog1'])
    catalog2_missing_labs = pd.DataFrame.from_dict(r.json()['catalog2'])

    pd.set_option('display.max_colwidth', None)
    print(catalog1_missing_labs['Content ID'])

    catalog1_missing_labs.drop('Content ID', axis=1, inplace=True)
    catalog1_missing_labs.drop('Catalog1', axis=1, inplace=True)
    catalog1_missing_labs.drop('Catalog2', axis=1, inplace=True)

    catalog2_missing_labs.drop('Content ID', axis=1, inplace=True)
    catalog2_missing_labs.drop('Catalog1', axis=1, inplace=True)
    catalog2_missing_labs.drop('Catalog2', axis=1, inplace=True)

    return render_template("diff-table.html", catalog1_name=get_catalog_from_url(catalog1_url), 
                                            catalog2_name=get_catalog_from_url(catalog2_url), 
                                            catalog1_col_names=catalog1_missing_labs.columns.values, 
                                            catalog1_row_data=list(catalog1_missing_labs.values.tolist()),
                                            catalog2_col_names=catalog2_missing_labs.columns.values, 
                                            catalog2_row_data=list(catalog2_missing_labs.values.tolist())                                            )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))