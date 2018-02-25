from hashlib import sha1
from urllib import parse

s = 'apid=asdsd&x=z'


q = dict((k, v if len(v) > 1 else v[0]) for k, v in parse.parse_qs(s).items())
print(len(q))