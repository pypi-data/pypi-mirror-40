
import unittest
import lifelib
import os

class TestRuleTrees(unittest.TestCase):

    def test_langtons_loops(self):

        filename = os.path.join(lifelib.lifelib_dir, 'rules', 'source', 'Langtons-Loops.table')
        sess = lifelib.load_rules(filename, force_compile=True)
        lt = sess.lifetree()
        ll = lt.pattern('''x = 15, y = 10, rule = Langtons-Loops
.8B$BAG.AD.ADB$B.6B.B$BGB4.BAB$BAB4.BAB$B.B4.BAB$BGB4.BAB$BA6BA5B$B.G
A.GA.G5AB$.13B!''')

        self.assertEqual(ll.getrule(), 'x9xlangtons-loops')

        self.assertEqual(ll.population, 86)
        self.assertEqual(ll[1000].population, 4154)
        self.assertEqual(ll[1000000].population, 7013241874)
