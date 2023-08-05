
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

    def test_brew(self):

        filename = os.path.join(lifelib.lifelib_dir, 'rules', 'source', 'Brew.rule')
        sess = lifelib.load_rules(filename, force_compile=True)
        lt = sess.lifetree()
        p150 = lt.pattern('''x = 30, y = 21, rule = Brew
11.2B4.2B$10.B2.B2.B2.B$11.2B4.2B2$13.4C$2.C9.C4.C9.C$3.2C4.BCB6.BCB
4.2C$2C.C5.BCBC4.CBCB5.C.2C$2.2C3.2B.2A6.2A.2B3.2C$.C4.C.AB2CBA2.AB2C
BA.C4.C$.C3.2BCA4BA2.A4BAC2B3.C$.C4.C.AB2CBA2.AB2CBA.C4.C$2.2C3.2B.2A
6.2A.2B3.2C$2C.C5.BCBC4.CBCB5.C.2C$3.2C4.BCB6.BCB4.2C$2.C9.C4.C9.C$
13.4C2$11.2B4.2B$10.B2.B2.B2.B$11.2B4.2B!''')

        self.assertEqual(p150.period, 150)
        self.assertEqual(p150.apgcode, 'xp150_y3coa4aoczy4vxvzy33152513_o4oy0cen9necy0o4ozg9gy2vfvy2g9gz121y037e9e73y0121')
