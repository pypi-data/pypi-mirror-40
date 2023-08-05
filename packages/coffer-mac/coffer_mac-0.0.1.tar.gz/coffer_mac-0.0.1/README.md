# coffer_mac

Tiny Python API for performing MAC address lookups using [Coffer](http://coffer.com/mac_find/).

Install: `pip install coffer_mac --user`

## Usage

```python
>>> import coffer_mac
>>> # Lookup by full MAC address
>>> coffer_mac.lookup('08:00:69:02:01:FC')
[{'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}, {'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}]
>>> # Lookup by first three octets
>>> coffer_mac.lookup('08:00:69')
[{'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}, {'prefix': '080069', 'vendor': 'Silicon Graphics (SGI)'}]
>>> # Lookup by vendor
>>> coffer_mac.lookup('trident')
[{'prefix': '001153', 'vendor': 'Trident Tek, Inc.'}, {'prefix': '00258F', 'vendor': 'Trident Microsystems, Inc.'}, {'prefix': '001153', 'vendor': 'Trident Tek, Inc.'}, {'prefix': '00258F', 'vendor': 'Trident Microsystems, Inc.'}]
```

## Disclaimer

I am not affiliated with "Coffer Group, LLC" and I cannot vouch for the validity of the data obtained.
