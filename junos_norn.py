from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file


def deploy_network(task):
    """Configures Junos device with NAPALM"""
    temp = task.run(
        name="Building device configuration", task=template_file, path="templates", template="base.j2"
    )
    configuration = temp.result
    task.run(
        name=f"Configuring {task.host.name}!",
        task=napalm_configure,
        configuration=configuration,
        replace=True,
    )


def main():
    """Used to run all the things"""
    norn = InitNornir(config_file="configs/config.yaml", core={"raise_on_error": True})
    result = norn.run(task=deploy_network)
    print_result(result)


if __name__ == "__main__":
    main()
