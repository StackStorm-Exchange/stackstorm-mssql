import six
import _mssql

from st2common.runners.base_action import Action

__all__ = [
    'MSSQLAction'
]


class MSSQLAction(Action):

    def connect(self, database=None, server=None, user=None, password=None):
        # pylint: disable=no-member
        return _mssql.connect(**self._connect_params(database, server, user, password))

    def _connect_params(self, database=None, server=None, user=None, password=None):
        database = database or self.config.get('default')
        db_config = self.config['connections'].get(database, {})
        params = {
            'database': db_config.get('database') or database,
            'server': server or db_config.get('server'),
            'user': user or db_config.get('user'),
            'password': password or db_config.get('password')
        }
        unspecified = [param for param, value in six.iteritems(params) if value is None]
        if unspecified:
            raise Exception("Must specify or configure in mssql.yaml: %s" % ', '.join(unspecified))
        return params
