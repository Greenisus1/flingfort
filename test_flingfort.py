import os
import unittest
from flingfort import *
class Physics(unittest.TestCase):
 def test_launch(self):
  p=launch(45,60);self.assertGreater(p.vx,0);self.assertAlmostEqual(p.vx,p.vy)
 def test_gravity(self):
  p=launch(45,60);v=p.vy;advance(p,[]);self.assertLess(p.vy,v)
 def test_hit(self):
  b=Block(10,3);p=Shot(10,3,0,0);self.assertEqual(advance(p,[b]),'hit');self.assertEqual(b.hp,0)
 def test_target(self):
  b=Block(10,3,1,True);self.assertEqual(advance(Shot(10,3,0,0),[b]),'hit');self.assertEqual(b.hp,0)
 def test_miss(self):self.assertEqual(advance(Shot(100,-1,0,0),[]),'end')
 def test_levels(self):
  for n in range(1,25):self.assertTrue(any(b.target for b in level(n)));self.assertLess(max(b.x for b in level(n)),96)
 def test_collapse(self):
  b=Block(50,6);settle([b]);self.assertEqual(b.y,4)
if __name__=='__main__':unittest.main()


class I18nTests(unittest.TestCase):
    def test_defaults_match_catalog(self):
        import pi18n
        self.assertTrue(DEFAULT_STRINGS["INTRO"])
        self.assertIn("{shots}", DEFAULT_STRINGS["HUD"])
    def test_overlay(self):
        S = dict(DEFAULT_STRINGS); S["PAUSED"] = "PAUSA"
        self.assertEqual(S["PAUSED"], "PAUSA")
