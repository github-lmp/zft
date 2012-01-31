from hashlib import md5
from struct import unpack_from

NODE_COUNT = 100
DATA_TO_COUNT = 10000000

node_counts = [0] * NODE_COUNT
for data_id in xrange(DATA_TO_COUNT):
    data_id = str(data_id)
