import click

from airflow_plugin_config_storage import AirflowEnvironmentVariablePlugin, LoadConfiguration


@click.command()
@click.option('--env-var-prefix', default='AIRFLOW_CONN_')
def run_env_var(env_var_prefix):
    plugin = AirflowEnvironmentVariablePlugin()
    plugin.VARIABLE_PREFIX = env_var_prefix
    plugin.on_load()


@click.command()
def run_delete_all_connections():
    LoadConfiguration().delete_all_connections()
