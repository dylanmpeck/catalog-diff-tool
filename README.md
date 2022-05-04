# catalog-diff-tool
A UI based web tool for checking differences in Qwiklabs Catalogs. 

Try it out: https://catalog-diff-tool-kjyo252taq-uc.a.run.app/

<img width="1017" alt="Screen Shot 2022-05-04 at 12 28 36 PM" src="https://user-images.githubusercontent.com/40506467/166673131-6205a274-a5f9-4c81-b331-da4a6d968c88.png">

<img width="1638" alt="Screen Shot 2022-05-04 at 12 31 29 PM" src="https://user-images.githubusercontent.com/40506467/166673241-4250390b-7280-4d26-a83e-5e2a246e8070.png">

## How do I use it?

1. Open the [catalog-diff-tool](https://catalog-diff-tool-kjyo252taq-uc.a.run.app/) in your browser.
2. Sign in with an __@google__ email address. Access will be denied to any other type of email.
3. Select the two catalogs you wish to compare from the two dropdowns.
4. Click __Submit__.
5. After a short loading time, you'll see side-by-side tables displaying which items the respective catalog is missing compared to the other.

## How does it work?

The catalog diff tool is a Python Flask app which utilizes Firebase authentication. It exists as a Cloud Run service __exclusive to googlers__ on `qwiklabs-resources`. 

After the user is signed-in and authenticated, they submit an html form with their chosen catalogs. These catalog selections are sent to a private cloud function which queries the Catalog API and gathers the list of items for each catalog. The lists are combined into a single pandas dataframe which marks `TRUE` or `FALSE` as to whether the lab was found in `catalog1` and/or `catalog2`. This dataframe is then broken back into two dictionaries which contain the missing labs by searching for which labs were flagged `FALSE` for `catalog1` and `catalog2` respectively. The dictionaries are returned as json and displayed in scrollable tables.

![Untitled Diagram drawio (2)](https://user-images.githubusercontent.com/40506467/166684346-66ac9c19-9dea-4ad1-88ac-25942a85bf68.png)

## How is this repo organized?

Cloud Run code: `cr_frontend`

Cloud Function code: `cf_query_catalogs`

## How can I add my catalog to the dropdown list?

It's easy to add an additional catalog URL to the html code, however the catalog-diff-tool's credentials need access to each individual catalog which must be provided by a super admin.

If your catalog is not in the list, contact Dylan Peck to discuss the process in which we can add it.
