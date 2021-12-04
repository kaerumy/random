import pandas
import requests
from tqdm import tqdm,trange

HEADERS = {'Accept': 'application/json'}
BASE_URL = "https://politikus.sinarproject.org/@search?" \
          "portal_type=Person&" \
          "fullobjects=1"

# default batch is 25 items
BATCH = 25
total_items = requests.get(BASE_URL,
                           headers=HEADERS).json()['items_total']

peps = []

for i in tqdm(range(0, total_items, 25), desc="Download Progress"):
    b_start = i+1
    URL = BASE_URL + "&b_start=" + str(b_start)
    r = requests.get(URL, headers=HEADERS)

    for person in r.json()['items']:
        pep = {}
        pep['name'] = person['name']
        pep['summary'] = person['summary']
        pep['pepStatusDetails'] = person['pepStatusDetails']
        pep['birth_date'] = person['birth_date']
        if person['gender']:
            pep['gender'] = person['gender']['title']
        else:
            pep['gender'] = None

        #tax residencies
        taxResidencies = []
        if person['taxResidencies']:
            for tax_country in person['taxResidencies']:
                taxResidencies.append(tax_country['title'])
        if taxResidencies:
            pep['taxResidencies'] = ",".join(taxResidencies)
        else:
            pep['taxResidencies'] = None

        nationalities = []
        if person['nationalities']:
            for nationality in person['nationalities']:
                nationalities.append(nationality['title'])
        if nationalities:
            pep['nationalities'] = ",".join(taxResidencies)
        else:
            pep['nationalities'] = None

        #ids
        pep['UID'] = person['UID']
        pep['rdf_id'] = person['@id']


        peps.append(pep)


df = pandas.DataFrame(peps)
print("Exporting politikus-persons.csv in current directory")
df.to_csv('politikus-persons.csv')
