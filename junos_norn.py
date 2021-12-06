"""Script used to interfact with some Junos gear"""
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file


def load_vars(task):
    """Loads data to be added to each host from vars files"""
    my_vars = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["info"] = my_vars.result
    template_configurations(task)


def template_configurations(task):
    """Builds network templates"""
    temp = task.run(
        name="Building device configuration",
        task=template_file,
        path="templates",
        template="base.j2",
    )
    config = temp.result
    deploy_configurations(task, config)


def deploy_configurations(task, config):
    """Loads device configurations"""
    task.run(
        name=f"Configuring {task.host}!",
        task=napalm_configure,
        configuration=config,
        replace=True,
    )


def main():
    """Used to run all the things"""
    norn = InitNornir(config_file="configs/config.yaml", core={"raise_on_error": True})
    result = norn.run(task=load_vars)
    print_result(result)


if __name__ == "__main__":
    main()
