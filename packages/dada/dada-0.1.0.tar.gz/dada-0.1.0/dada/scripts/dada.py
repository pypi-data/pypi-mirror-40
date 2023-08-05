#!/usr/bin/env python3

from pathlib import Path
from subprocess import run

import toml
from click import echo, group, prompt, argument, option, secho, edit, style, Choice
from dada import projects
from dada.projects import Project, Kind, create_project, PROJECT_CONFIG_FILENAME, BaseConfig, print_summary, Category, \
    save_project_config
from pick import pick

PRIMARY_COLOR = 'blue'


@group()
def cli():
    pass


@cli.group()
def config():
    pass


@config.command()
@argument('shortcut', required=False)
def project(shortcut):
    local_config_path = Path('.', PROJECT_CONFIG_FILENAME)
    if shortcut or local_config_path.is_file():
        project = get_project(shortcut)
        config_path = project.path / PROJECT_CONFIG_FILENAME
        edit_command = BaseConfig.get('config-edit-command')
        run([edit_command, config_path])
    else:
        print(f'Creating new project config file {PROJECT_CONFIG_FILENAME}')
        converter = lambda kind: str(kind)
        kind_key = prompt(style('Kind', fg=PRIMARY_COLOR), type=Choice(Kind.all()), default=None, value_proc=converter)
        title = prompt('Title?')
        shortcut = prompt('Shortcut?')
        save_project_config(path=local_config_path, title=title, kind_key=kind_key, shortcut=shortcut)


@config.command()
def list():
    BaseConfig.print()


@config.command()
@argument('key')
def kind(key):
    kind = Kind.get(key)
    editor = BaseConfig.get('config-edit-command')
    run([editor, kind.config_path])


@cli.command()
@argument('shortcut', required=False)
def output(shortcut):
    project = get_project(shortcut)
    project.show_output()


@cli.command()
@argument('kind')
@option('--title', prompt=True)
def new(kind, title):
    create_project(kind_key=kind, title=title)


@cli.command()
@argument('key', required=False)
def kinds(key):
    if key:
        kind = Kind.get(key)
        print_summary(kind)
    else:
        for kind in Kind.all():
            print(kind)


@cli.command()
@argument('shortcut')
def debug(shortcut):
    project = get_project(shortcut)
    print(project.__dict__)


@cli.command()
@argument('shortcut')
def compile(shortcut):
    project = get_project(shortcut)
    project.build()


@cli.command()
@argument('shortcut', required=False)
def serve(shortcut):
    project = get_project(shortcut)
    project.serve()


@cli.command()
@argument('shortcut', required=False)
def edit(shortcut):
    get_project(shortcut).edit()
#
#
@cli.command()
@argument('shortcut', required=False)
def start(shortcut):
    project = get_project(shortcut)
    project.start()


@cli.command()
@argument('shortcut')
@argument('component')
def update(shortcut, component):
    project = get_project(shortcut)
    secho('==> ', fg='red', nl=False)
    secho(f'Updating {component} of project {project.title}.', bold=True)
    project.update_component(component)


# @cli.command()
# @argument('component_type')
# @pass_context
# def upstream(context, component_type):
#     project = context.obj['project']
#     project.update_template(component_type)


@cli.command()
@argument('shortcut', required=False)
def info(shortcut):
    project = get_project(shortcut)
    print_summary(project)


@cli.command()
def init():
    title = prompt(text='Title')
    shortcut = prompt(text='Shortcut')
    kind, _ = pick([kind.title for kind in Kind.all()], 'Please choose kind of project:')
    data = {
        'title': title,
        'shortcut': shortcut,
        'kind': kind
    }
    with Path(projects.PROJECT_CONFIG_FILENAME).open('w') as f:
        toml.dump(data, f)


@cli.group()
def list():
    pass


@list.command()
def projects():
    for project in Project.all():
        echo(f'{project.shortcut}\t{project.title}')


@list.command()
def categories():
    for category in Category.all():
        print(category)


def get_project(shortcut):
    if shortcut:
        return Project.from_shortcut(shortcut)
    elif Project.local():
        return Project.local()
    else:
        print(f'No project found.')
        exit()


