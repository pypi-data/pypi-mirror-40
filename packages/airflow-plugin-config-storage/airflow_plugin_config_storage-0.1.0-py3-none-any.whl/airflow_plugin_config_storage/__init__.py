import os

from airflow import settings
from airflow.models import Connection
from airflow.plugins_manager import AirflowPlugin
from sqlalchemy.orm import exc


class LoadConfiguration(object):
    def __init__(self):
        self.session = settings.Session()

    def has_connection(self, conn_id):
        try:
            self.session.query(Connection). \
                filter(Connection.conn_id == conn_id). \
                one()
        except exc.NoResultFound:
            return False
        return True

    def load_plugin(self, conn_type, conn_id, **conn_args):
        if self.has_connection(conn_id):
            self.delete_connection(conn_id)

        self.add_connection(
            conn_id=conn_id,
            conn_type=conn_type,
            **conn_args
        )

    def delete_all_connections(self):
        self.session.query(Connection.conn_id).delete()
        self.session.commit()

    def delete_connection(self, conn_id):
        self.session.query(Connection.conn_id == conn_id).delete()
        self.session.commit()

    def add_connection(self, **conn_args):
        """
        conn_id, conn_type, extra, host, login,
        password, port, schema, uri
        """
        self.session.add(Connection(**conn_args))
        self.session.commit()


class AirflowEnvironmentVariablePlugin(AirflowPlugin):
    VARIABLE_PREFIX = 'AIRFLOW_CONN_'

    @classmethod
    def on_load(cls, *args, **kwargs):
        connections = LoadConfiguration()
        for key in os.environ.keys():
            if key.startswith(cls.VARIABLE_PREFIX):
                key_parts = key.split('_')
                if len(key_parts) < 4 is None:
                    continue
                conn_type = key_parts[2].lower()
                conn_id = '_'.join(key_parts[3:]).lower()

                connections.load_plugin(
                    conn_type=conn_type,
                    conn_id=conn_id,
                    uri=os.environ[key]
                )
