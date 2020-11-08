# DNS swap script

Use to move DNS zone from one instance to another within the same region.

## Usage

```bash
$ python3.6 dns_swap.py -h
usage: dns_swap.py [-h] -s SOURCE_UUID -d DESTINATION_UUID -z ZONE

Swap DNS zones between Stratus instances

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_UUID, --source SOURCE_UUID
                        UUID you want to migrate DNS zone from
  -d DESTINATION_UUID, --destination DESTINATION_UUID
                        UUID you want to migrate DNS zone to
  -z ZONE, --zone ZONE  DNS zone you want to migrate
```
