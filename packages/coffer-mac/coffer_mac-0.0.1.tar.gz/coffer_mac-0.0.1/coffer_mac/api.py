"""coffer_mac.lookup"""

import bs4
import requests


def lookup(string):
    r = requests.get('http://coffer.com/mac_find/?string='+string)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    results = []
    for row in soup.find_all('tr', class_="table2"):
        try:
            prefix, vendor = row.find_all('td')
        except ValueError:
            continue
        results.append({'prefix':prefix.text, 'vendor':vendor.text})
    return results
