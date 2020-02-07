import re
import fnmatch
import functools
import sys

from simpleeval import EvalWithCompoundTypes, DEFAULT_FUNCTIONS

fnmatch_fnmatch = fnmatch.fnmatch
re_match = functools.partial(re.match, flags=0)
re_imatch = functools.partial(re.match, flags=re.IGNORECASE)

LOCAL_FUNCTIONS = {
    'fnmatch_fnmatch': fnmatch.fnmatch,
    're_match': re_match,
    're_imatch': re_imatch,
    'bool': bool
}
LOCAL_FUNCTIONS.update(DEFAULT_FUNCTIONS)


def _partialclass(cls, *args, **kwargs):

    class NewCls(cls):
        if sys.version_info.major >= 3:
            __init__ = functools.partialmethod(cls.__init__, *args, **kwargs)
        else:
            __init__ = functools.partial(cls.__init__, *args, **kwargs)

    return NewCls


SandboxedEval = _partialclass(EvalWithCompoundTypes, functions=LOCAL_FUNCTIONS)
