import unittest
from lp.propositional.obdd import *
from lp.propositional.formula import *


class TestOBDD(unittest.TestCase):

    def test_equivalent(self):
        self.assertTrue(are_equivalent(IMPLIES("A", "B"), OR(NOT("A"), "B")))
        self.assertTrue(are_equivalent(IMPLIES(AND("A", "B"), "C"), IMPLIES("A", IMPLIES("B", "C"))))

        self.assertFalse(are_equivalent(IMPLIES("A", "B"), AND(NOT("A"), "B")))

    def test_is_inconsistent(self):
        self.assertTrue(is_inconsistent(AND("X", NOT("X"))))

    def test_is_tautology(self):
        self.assertTrue(is_tautology(IFF(IMPLIES(AND("A", "B"), "C"), IMPLIES("A", IMPLIES("B", "C")))))
