import functools
from lp.propositional.formula import VAR


class Heap:

    def __init__(self):
        self._data = {}
        self._pointers = []
        self.false_ptr = self._add(False, None, None)
        self.true_ptr = self._add(True, None, None)

    def _add(self, root, p_child_t, p_child_f):
        if p_child_t == p_child_f and p_child_t is not None:
            raise ValueError("T and F pointers should not be the same")
        key = (root, p_child_t, p_child_f)
        index = len(self._pointers)
        self._pointers.append(key)
        self._data[key] = index
        return index

    def _get_ptr(self, root, p_child_t, p_child_f):
        return self._data[(root, p_child_t, p_child_f)]

    def _get_make_ptr(self, root, p_child_t, p_child_f):
        try:
            return self._get_ptr(root, p_child_t, p_child_f)
        except KeyError:
            return self._add(root, p_child_t, p_child_f)

    @staticmethod
    def _first_var(var_list):
        def key(x):
            return (0 if type(x) == str else 1), x

        m = min(var_list, key=key)
        return m, {v for v in var_list if v != m}

    def _truth_table(self, formula, fixed_variables):
        variables = formula.variables()
        remaining = variables.difference(fixed_variables.keys())
        if not remaining:
            t = formula.evaluate(fixed_variables)
            return self._get_ptr(t, None, None)
        else:
            my_var, remaining = Heap._first_var(remaining)

            fv_t = fixed_variables.copy()
            fv_t[my_var] = True
            ptr_t = self._truth_table(formula, fv_t)

            fv_f = fixed_variables.copy()
            fv_f[my_var] = False
            ptr_f = self._truth_table(formula, fv_f)

            if ptr_t == ptr_f:
                return ptr_t
            else:
                return self._get_make_ptr(my_var, ptr_t, ptr_f)

    def from_truth_table(self, formula):
        return self._truth_table(formula, {})

    def _combine(self, pointers, combiner, remaining, fixed_var=None, fixed_value=None):
        def eval_ptr(ptr):
            var, ptr_t, ptr_f = self._pointers[ptr]
            if var == fixed_var:
                return ptr_t if fixed_value else ptr_f
            return ptr

        def real_bools(ptr):
            if ptr == self.true_ptr:
                return True
            elif ptr == self.false_ptr:
                return False
            else:
                return ptr

        pointers = [eval_ptr(ptr) for ptr in pointers]
        result = combiner(*(real_bools(ptr) for ptr in pointers))
        if result is True:
            return self.true_ptr
        elif result is False:
            return self.false_ptr
        elif result is None:
            fixed_var, remaining = Heap._first_var(remaining)
            ptr_t = self._combine(pointers, combiner, remaining, fixed_var, True)
            ptr_f = self._combine(pointers, combiner, remaining, fixed_var, False)
            if ptr_t == ptr_f:
                return ptr_t
            else:
                return self._get_make_ptr(fixed_var, ptr_t, ptr_f)
        elif result in pointers:
            return result
        else:
            raise ValueError("Invalid result from combining")

    def combine(self, connector, *pointers):
        variables = functools.reduce(set.union, (self.variables(ptr) for ptr in pointers), set())
        return self._combine(pointers, connector.combine, variables, None, None)

    def recursive_combine(self, formula):
        if isinstance(formula, VAR):
            return self._get_make_ptr(formula.var_name, self.true_ptr, self.false_ptr)

        children = [self.recursive_combine(f) for f in formula.children]
        return self.combine(formula.__class__, *children)

    def variables(self, ptr):
        if ptr is None or ptr == self.true_ptr or ptr == self.false_ptr:
            return set()
        var, ptr_t, ptr_f = self._pointers[ptr]
        return {var}.union(self.variables(ptr_t)).union(self.variables(ptr_f))

    def isolate(self, iso_ptr):
        output = [self._pointers[self.false_ptr], self._pointers[self.true_ptr]]
        mapping = {self.false_ptr: 0, self.true_ptr: 1}

        def _iso(ptr):
            if ptr in mapping:
                return mapping[ptr]
            else:
                root, ptr_t, ptr_f = self._pointers[ptr]
                output.append((root, _iso(ptr_t), _iso(ptr_f)))
                mapping[ptr] = i = len(output) - 1
                return i

        return output, _iso(iso_ptr)

    formula = from_truth_table


def is_tautology(formula, heap=None):
    if heap is None:
        heap = Heap()
    return heap.true_ptr == heap.formula(formula)


def is_inconsistent(formula, heap=None):
    if heap is None:
        heap = Heap()
    return heap.false_ptr == heap.formula(formula)


def are_equivalent(formula1, formula2, heap=None):
    if heap is None:
        heap = Heap()
    return heap.formula(formula1) == heap.formula(formula2)


__all__ = ["Heap", "is_tautology", "is_inconsistent", "are_equivalent"]