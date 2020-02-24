import re
import fnmatch
import functools
import ast

from simpleeval import EvalWithCompoundTypes, DEFAULT_FUNCTIONS

fnmatch_fnmatch = fnmatch.fnmatch
re_match = functools.partial(re.match, flags=0)
re_imatch = functools.partial(re.match, flags=re.IGNORECASE)

LOCAL_FUNCTIONS = {
    'fnmatch_fnmatch': fnmatch.fnmatch,
    're_match': re_match,
    're_imatch': re_imatch,
    'bool': bool,
    **DEFAULT_FUNCTIONS
}


class _Eval(EvalWithCompoundTypes):

    def __init__(self,  operators=None, functions=None, names=None):
        super().__init__(operators, functions, names)

        self.nodes.update({
            ast.Bytes: self._eval_bytes,
        })

    @staticmethod
    def _eval_bytes(node):
        return node.s.decode()


def _partialclass(cls, *args, **kwargs):

    class NewCls(cls):
        __init__ = functools.partialmethod(cls.__init__, *args, **kwargs)
    return NewCls


SandboxedEval = _partialclass(_Eval, functions=LOCAL_FUNCTIONS)
