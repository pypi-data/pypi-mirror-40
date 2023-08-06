import json


class LogstashJsonEncoder(json.JSONEncoder):
    def __init__(self, skipkeys=True, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        super(
            LogstashJsonEncoder,
            self).__init__(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default,
            )
