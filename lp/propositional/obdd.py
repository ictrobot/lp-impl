class Heap:

    def __init__(self):
        self._data = {}
        self._pointers = []
        self.false_ptr = self._add(False, None, None)
        self.true_ptr = self._add(True, None, None)

    def _add(self, root, p_child_t, p_child_f):
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

    def _build_formula(self, formula, fixed_variables):
        variables = formula.variables()
        remaining = variables.difference(fixed_variables.keys())
        if not remaining:
            t = formula.evaluate(fixed_variables)
            return self._get_ptr(t, None, None)
        else:
            my_var, remaining = Heap._first_var(remaining)

            fv_t = fixed_variables.copy()
            fv_t[my_var] = True
            ptr_t = self._build_formula(formula, fv_t)

            fv_f = fixed_variables.copy()
            fv_f[my_var] = False
            ptr_f = self._build_formula(formula, fv_f)

            if ptr_t == ptr_f:
                return ptr_t
            else:
                return self._get_make_ptr(my_var, ptr_t, ptr_f)

    def formula(self, formula):
        return self._build_formula(formula, {})


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
