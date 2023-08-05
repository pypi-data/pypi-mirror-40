# coffer_mac
Tiny Python API for performing MAC address lookups using [Coffer](http://coffer.com/mac_find/).

Install: `pip install coffer_mac --user`

## Usage

```python
>>> from coffer_mac import CofferMAC
>>> client = CofferMAC()

>>> # Lookup by full MAC address
>>> client.lookup('08:00:69:02:01:FC')
[{'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}, {'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}]

>>> # Lookup by first three octets
>>> client.lookup('08:00:69')
[{'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}, {'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}]

>>> # Lookup by vendor
>>> client.lookup('trident')
[{'prefix': '001153', 'vendor': 'Trident Tek, Inc.'}, {'prefix': '00258F', 'vendor': 'Trident Microsystems, Inc.'}, {'prefix': '001153', 'vendor': 'Trident Tek, Inc.'}, {'prefix': '00258F', 'vendor': 'Trident Microsystems, Inc.'}]

>>> # Use a proxy
>>> client = CofferMAC(proxy='localhost:8080')
>>> client.lookup('foo')
[{'prefix': '001588', 'vendor': 'Balda-Thong Fook Solu'}, {'prefix': '001903', 'vendor': 'Bigfoot Networks Inc'}, {'prefix': '00609D', 'vendor': 'Pmi Food Equipment Group'}, {'prefix': '00D029', 'vendor': 'Wakefern Food Corporation'}, {'prefix': '001588', 'vendor': 'Balda-Thong Fook Solu'}, {'prefix': '001903', 'vendor': 'Bigfoot Networks Inc'}, {'prefix': '00609D', 'vendor': 'Pmi Food Equipment Group'}, {'prefix': '00D029', 'vendor': 'Wakefern Food Corporation'}, {'prefix': 'C458C2', 'vendor': 'Shenzhen TATFOOK Technology Co., Ltd.'}]
```

## Disclaimer

I am not affiliated with "Coffer Group, LLC" and I cannot vouch for the validity of the data obtained.
