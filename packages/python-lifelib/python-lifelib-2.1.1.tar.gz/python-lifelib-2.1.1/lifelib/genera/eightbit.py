family = 6
bitplanes = 8
mantissa = {0, 1}

def create_rule(rulestring):

    with open('iterators_%s.h' % rulestring, 'w') as f:
        f.write('#pragma once\n')
        f.write('#include "../../rules/%s.h"\n' % rulestring)

