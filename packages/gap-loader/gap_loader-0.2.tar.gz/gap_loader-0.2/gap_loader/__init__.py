import sys
import imp
import os
import sage.interfaces.gap
import types

gap = sage.interfaces.gap.gap


def get_full_path(directory, name):
    full_path = os.path.join(directory, '{name}.gap'.format(name=name))
    if os.path.isfile(full_path):
        return full_path


class GapLoader(object):
    def __init__(self, gap_path):
        self.gap_path = gap_path

    @classmethod
    def find_module(cls, name, path=None):
        for d in sys.path:
            gap_path = get_full_path(d, name)
            if gap_path is not None:
                return cls(gap_path)

        if path is not None:
            name = name.split('.')[-1]
            for d in path:
                gap_path = get_full_path(d, name)
                if gap_path is not None:
                    return cls(gap_path)

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        mod = imp.new_module(name)
        mod.__file__ = self.gap_path
        mod.__loader__ = self

        with open(self.gap_path) as f:
            code = f.read()

        vars_before = eval(str(gap("NamesGVars()")))

        try:
            gap.eval(code)
        except TypeError:
            raise ImportError(
                '"{name}" does not contain valid GAP code.'.format(
                    name=self.json_path))

        vars_after = eval(str(gap("NamesGVars()")))
        diff = set(vars_after).difference(set(vars_before))
        for name in diff:
            mod.__dict__[name] = gap.new(name)

        sys.modules[name] = mod
        return mod


sys.meta_path.append(GapLoader)
