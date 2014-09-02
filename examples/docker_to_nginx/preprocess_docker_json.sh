#!/bin/bash

# This script works on the assumption that the names given to containers are in the format of <app_name>_<uuid>

python -c 'import json; import sys; print json.dumps([ dict(map(lambda (k, v): (k, v) if k != "Names" else ("Name", v[0].split("_")[0][1:]), c.iteritems())) for c in json.load(sys.stdin) ]);'
