# type: ignore

import toml
from invoke import Context, task

import monkey_patch_invoke as _  # noqa: F401


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_name = get_pep8_compliant_name(data['tool']['poetry']['name'])
        return project_name


@task
def test(context: Context):
    context.run('pytest . --cov=moragi --cov-report=xml', pty=True)


@task
def format_code(context: Context, verbose: bool = False):
    commands = [
        f'pautoflake {get_project_path()}',
        f'ruff --fix {get_project_path()}',
        f'yapf --in-place --recursive --parallel {get_project_path()}',
    ]

    for command in commands:
        context.run(command, pty=True)


@task
def check(context: Context):
    check_code_style(context)
    check_types(context)


@task
def check_code_style(context: Context):
    commands = [
        f'ruff {get_project_path()}',
        f'yapf --diff --recursive --parallel {get_project_path()}',
    ]

    for command in commands:
        context.run(command, pty=True)


@task
def check_types(context: Context):
    context.run(f'pyright {get_project_path()}', pty=True)
