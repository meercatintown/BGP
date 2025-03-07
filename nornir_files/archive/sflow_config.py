from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

# Initialize Nornir with your configuration file
nr = InitNornir(config_file="config.yml")

def configure_sflow(task):
    # Enable sFlow globally
    task.run(task=netmiko_send_config, config_commands=["sflow run"])

    # Configure sFlow settings
    sflow_config = [
        "sflow destination 192.168.100.20 6343",
        "sflow agent-interface Management0",  # You may need to adjust this for your environment
        "sflow polling-interval 30"
    ]
    task.run(task=netmiko_send_config, config_commands=sflow_config)

    # List the interfaces to check if they exist
    interfaces = ["et1", "et2", "et3"]
    
    for interface in interfaces:
        # Check if the interface exists by attempting to show it
        show_interface = task.run(task=netmiko_send_config, config_commands=[f"show interfaces {interface}"])

        # Check if the interface exists in the output
        if "Invalid input" not in show_interface.result:
            # Interface exists, apply sFlow configuration
            interface_config = [
                f"interface {interface}",
                "sflow enable",
                "sflow sampling-rate 1000"
            ]
            task.run(task=netmiko_send_config, config_commands=interface_config)

# Run the task across all hosts defined in the inventory
results = nr.run(task=configure_sflow)

# Print the results
print_result(results)
