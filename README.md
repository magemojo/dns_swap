DNS swap script

Use to move DNS zone from one instance to another within the same region.

$ python3.6 dns_swap.py -h
usage: dns_swap.py [-h] -s SOURCE -d DESTINATION -z ZONE

Swap DNS zones between Stratus instances

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        UUID you want to migrate DNS zone from
  -d DESTINATION, --destination DESTINATION
                        UUID you want to migrate DNS zone to
  -z ZONE, --zone ZONE  DNS zone you want to migrate
