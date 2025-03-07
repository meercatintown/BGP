from nornir import InitNornir
from nornir.core.task import Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko.tasks import netmiko_send_config

def configure_sflow(task: Task):
    config = task.run(
        task=template_file,
        template="sflow_config.j2",
        path="config_templates/"
    )
    task.run(task=netmiko_send_config, config_commands=config.result.split("\n"))

nr = InitNornir(config_file="config.yml")
nr.run(task=configure_sflow)
