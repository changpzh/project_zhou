from . import api
from . import web
from . import ltemetrics


class coop(object):
    ROBOT_LIBRARY_SCOPE = 'global'

    def __init__(self):
        self._keywords = {}
        for _module in (api, web, ltemetrics):
            for kw_name in dir(_module):
                if not kw_name.startswith('_') and \
                    hasattr(getattr(_module, kw_name), 'func_name'):
                        self._keywords[kw_name] = getattr(_module, kw_name)

    def __getattr__(self, kw_name):
        try:
            return self._keywords[kw_name]
        except KeyError:
            raise AttributeError

    def get_keyword_names(self):
        return self._keywords.keys()
