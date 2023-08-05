"""coffer_mac.lookup"""

import bs4
import requests


class CofferMAC:
    def __init__(self, proxy=None):
        self.base_url = 'http://coffer.com/mac_find/?string={s}'
        self.session = requests.Session()
        self.session.proxies = {'http': proxy}

    def lookup(self, string):
        """
        Perform a MAC address lookup using Coffer.
        """

        url = self.base_url.format(s=string)
        request = self.session.get(url)

        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        rows = soup.find_all('tr', class_="table2")[1:]

        results = []
        for row in rows:
            prefix, vendor = row.find_all('td')
            results.append({'prefix': prefix.text, 'vendor': vendor.text})
        return results
