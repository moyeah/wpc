#!/usr/bin/env python

import copy
import numpy as np

def calc(powers):
  values = copy.deepcopy(powers)
  for value in values:
    value.pop()
  values = np.matrix(values).astype(np.float).tolist()
  print np.unique(values)
