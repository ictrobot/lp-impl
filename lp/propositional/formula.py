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


AND = _formula_op("AND", op_and, 2)
OR = _formula_op("OR", op_or, 2)
NOT = _formula_op("NOT", op_not, 1)
IMPLIES = _formula_op("IMPLIES", op_implies, 2)
IFF = _formula_op("IFF", op_iff, 2)

__all__ = [
    "VAR", "AND", "OR", "NOT", "IMPLIES", "IFF"
]