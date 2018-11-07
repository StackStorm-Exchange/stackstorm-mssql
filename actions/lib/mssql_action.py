import _mssql

from st2common.runners.base_action import Action

__all__ = [
    'MSSQLAction'
]


class MSSQLAction(Action):

    def connect(self, database=None, server=None, user=None, password=None, port=None):
        # pylint: disable=no-member
        return _mssql.connect(**self._connect_params(database, server, user, password, port))

    def _connect_params(self, database=None, server=None, user=None, password=None, port=None):
        database = database or self.config.get('default')
        db_config = self.config['connections'].get(database, {})
        params = {
            'database': db_config.get('database') or database,
            'server': server or db_config.get('server'),
            'port': port or db_config.get('port'),
            'user': user or db_config.get('user'),
            'password': password or db_config.get('password')
        }
        unspecified = [param for param, value in params.iteritems() if value is None]
        if unspecified:
            raise Exception("Must specify or configure in mssql.yaml: %s" % ', '.join(unspecified))
        return params
