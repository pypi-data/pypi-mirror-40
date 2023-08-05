
import os
from .rulefiles import rules_dir

def bitplanes(rulestring):

    with open(os.path.join(rules_dir, rulestring + '.h')) as f:
        for line in f:
            break

    if '16' in line:
        return 16
    else:
        return 8

def family(rulestring):

    bp = bitplanes(rulestring)
    log2bp = len(bin(bp)) - 3
    return 2 * log2bp

mantissa = {0, 1}

def create_rule(rulestring):

    with open('iterators_%s.h' % rulestring, 'w') as f:
        f.write('#pragma once\n')
        f.write('#include "../../rules/%s.h"\n' % rulestring)

