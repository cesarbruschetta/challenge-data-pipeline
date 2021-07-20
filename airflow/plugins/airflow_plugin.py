from airflow.plugins_manager import AirflowPlugin
from hooks.twitter_hook import TwitterHook


class CustomAirflowPlugin(AirflowPlugin):  # type: ignore
    name = "custom"
    hooks = [TwitterHook]
