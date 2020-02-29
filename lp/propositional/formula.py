from lp.propositional.operators import *
import functools


class VAR:

    def __init__(self, var_name):
        self.var_name = var_name

    def __str__(self):
        return self.var_name

    def evaluate(self, variable_mapping):
        return variable_mapping[self.var_name]

    def variables(self):
        return {self.var_name}


def _formula_op(name, impl, arguments):
    class FormulaOp:
        def __init__(self, *data):
            if len(data) != arguments:
                raise ValueError
            self.children = tuple(VAR(d) if type(d) == str else d for d in data)

        def __str__(self):
            return "{}({})".format(name, ", ".join(map(str, self.children)))

        def evaluate(self, variable_mapping):
            return impl(*map(lambda x: x.evaluate(variable_mapping), self.children))

        def variables(self):
            return functools.reduce(set.union, (d.variables() for d in self.children))

    return FormulaOp


class AND(_formula_op("AND", op_and, 2)):
    @staticmethod
    def combine(fst, snd):
        if fst == snd:
            return fst
        if fst is True:
            return snd
        if snd is True:
            return fst
        if fst is False or snd is False:
            return False
        return None


class OR(_formula_op("OR", op_or, 2)):
    @staticmethod
    def combine(fst, snd):
        if fst == snd:
            return fst
        if fst is False:
            return snd
        if snd is False:
            return fst
        if fst is False or snd is False:
            return True
        return None


class NOT(_formula_op("NOT", op_not, 1)):
    @staticmethod
    def combine(fst):
        if fst is True:
            return False
        if fst is False:
            return True
        return None


class IMPLIES(_formula_op("IMPLIES", op_implies, 2)):
    @staticmethod
    def combine(fst, snd):
        if fst == snd:
            return True
        if fst is True:
            return snd
        if fst is False:
            return True
        return None


class IFF(_formula_op("IFF", op_iff, 2)):
    @staticmethod
    def combine(fst, snd):
        if fst == snd:
            return True
        if fst is True:
            return snd
        if snd is True:
            return fst
        return None


__all__ = [
    "VAR", "AND", "OR", "NOT", "IMPLIES", "IFF"
]