#!/usr/bin/env python2.5

import libxml2
from parse import get_boundary_relations
import sys
from collections import defaultdict

boundaries = {
    "4": "regioni",
    "6": "province",
    "8": "comuni",
    }

boundary_relations = defaultdict(lambda : defaultdict(int))

get_boundary_relations(sys.argv[1])

print repr(boundary_relations)
