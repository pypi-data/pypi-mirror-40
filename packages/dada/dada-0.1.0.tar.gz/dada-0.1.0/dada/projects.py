from datetime import date
from os import environ
from pathlib import Path
from shutil import copy, copytree
from subprocess import run, Popen
from typing import List

import toml
from click import secho, confirm, echo

PROJECT_CONFIG_FILENAME = '.dadaproject.toml'

APP_CONFIG_DIR = Path(__file__).parent / 'config'
APP_BASE_CONFIG_PATH = APP_CONFIG_DIR / 'base.toml'
APP_KINDS_CONFIG_PATH = APP_CONFIG_DIR / 'kinds.toml'
APP_KINDS_DIR = Path(__file__).parent / 'kinds'

USER_CONFIG_DIR = environ.get('$XDG_CONFIG_HOME', Path.home() / '.config' / 'dada')
if not USER_CONFIG_DIR.exists():
    USER_CONFIG_DIR.mkdir(parents=True)
USER_BASE_CONFIG_PATH = USER_CONFIG_DIR / 'base.toml'
if not USER_BASE_CONFIG_PATH.exists():
    USER_BASE_CONFIG_PATH.touch()
USER_KINDS_DIR = USER_CONFIG_DIR / 'kinds'

TEMPLATES_PATH = '' #todo


class BaseConfig:

    with APP_BASE_CONFIG_PATH.open() as f:
        base_config = toml.load(f)

    if USER_BASE_CONFIG_PATH.exists():
        with USER_BASE_CONFIG_PATH.open() as f:
            user_base_config = toml.load(f)
    else:
        USER_BASE_CONFIG_PATH.touch()
        user_base_config = {}

    @classmethod
    def keys(cls):
        app_config_keys = list(cls.base_config)
        user_config_keys = list(cls.user_base_config)
        return app_config_keys + user_config_keys

    @classmethod
    def get(cls, key: str):
        if key in cls.user_base_config:
            return cls.user_base_config[key]
        elif key in cls.base_config:
            return cls.base_config[key]

    @classmethod
    def print(cls):
        for key in cls.keys():
            print(f'{key}: {cls.get(key)}')


class Project:
    store = {}
    ready = False

    @classmethod
    def init(cls):
        config_paths = Project.project_config_paths()
        for path in config_paths:
            Project.add_from_config_path(path)
        cls.ready = True

    @classmethod
    def project_config_paths(cls):
        if not BaseConfig.get('project-dirs'):
            print('Could not look for projects because no project directories are defined.')
            return []
        config_paths = []
        dirs = [Path(dir).expanduser() for dir in BaseConfig.get('project-dirs')]
        for dir in dirs:
            for config in dir.glob(f'*/{PROJECT_CONFIG_FILENAME}'):
                config_paths.append(config)
        return config_paths

    @staticmethod
    def local():
        path = Path('.') / PROJECT_CONFIG_FILENAME
        with path.open() as f:
            dictionary = toml.load(f)
        return Project(dictionary, path=Path.cwd())

    @classmethod
    def from_shortcut(cls, shortcut):
        if shortcut == 'local':
            return Project.local()
        else:
            return cls.store.get(shortcut, None)

    @classmethod
    def shortcuts(cls):
        return cls.store.keys()

    @classmethod
    def add_from_config_path(cls, config_path: Path):
        with config_path.open() as f:
            try:
                dictionary = toml.load(f)
            except Exception:
                print(f'Could not read config file {config_path}.')
                return
        project_path = config_path.parent
        project = Project(dictionary, project_path)
        shortcut = project.shortcut
        Project.store[shortcut] = project

    @classmethod
    def all(cls):
        return Project.store.values()

    @classmethod
    def from_path(cls, path: Path):
        with open(path / PROJECT_CONFIG_FILENAME) as f:
            dictionary = toml.load(f)
        return Project(dictionary, path=path)

    def __init__(self, config_dictionary: dict, path: Path):

        if not config_dictionary:
            print(f'Problem with reading project config from {path}')
            return
        else:
            self.config_dictionary = config_dictionary

        if 'kind' in config_dictionary:
            self.kind = Kind.get(config_dictionary['kind'])
        else:
            self.kind = 'undefined'

        self.path = path.absolute()

        self.config_path = self.path / PROJECT_CONFIG_FILENAME

        self.title = config_dictionary.get('title', None)

        if 'code-path' in config_dictionary:
            setattr(self, 'code_path', path / config_dictionary['code-path'])
        else:
            setattr(self, 'code_path', self.path)

        if 'web-path' in config_dictionary:
            setattr(self, 'web_path', path / config_dictionary['web-path'])
        else:
            setattr(self, 'web_path', self.path)

        # if 'live_path' in config_dictionary:
        #     self.live_path = Path(config_dictionary['live_path'])

    def __getattr__(self, item):
        item = item.replace('_', '-')
        if item in self.config_dictionary:
            return self.config_dictionary[item]
        elif hasattr(self, 'kind') and hasattr(self.kind, item):
            return getattr(self.kind, item)
        elif BaseConfig.get(item):
            return BaseConfig.get(item)

    def build(self):
        Popen([self.build_command], cwd=self.code_path)
        # if self.taskrunner == 'grunt':
        #     run(['dkill', 'grunt']) # todo
        #     Popen(['grunt'], cwd=self.code_path)
        #
        # if self.taskrunner == 'make':
        #     run(['make'], cwd=self.code_path)

    def serve(self):

        # if hasattr(self, 'mamp') and self.mamp:
        #     run(['mamp', 'switch', self.web_path])
        #
        # elif str(self.kind) == 'harp':
        #     run(['dkill', 'harp']) # todo: change
        #     Popen(['harp', 'server'], cwd=self.code_path)


        Popen(self.serve_command.split(' '), cwd=self.code_path)

        self.show_in_browser()

    def show_in_browser(self):
        run(['open', '-a', BaseConfig.get('browser'), self.development_url])

    def open_document(self):
        run(['open', '-a', BaseConfig.get('pdf-viewer'), 'document.pdf'], cwd=self.code_path)

    def update_component(self, component: str):

        relative_path = self.kind.get_component_path(component)
        path = self.path / relative_path
        template_path = self.kind.get_template_path(component)
        if not path or confirm('Do you want to override existing files?'):
            copy(path, path.with_suffix('.backup' + path.suffix))
            copy(template_path, path)

    # def update_template(self, component_type: str):
    #     installed = self.get_component(component_type)
    #     template = get_component_template(component_type, self.type)
    #     if confirm(f'Do you want to override {template}?'):
    #         project_type_config = Kind.from_string(self.type)
    #         if component_type in project_type_config:
    #             copy(template, template.with_suffix('.backup.coffee'))
    #             copy(installed, template)

    def edit(self):
        if self.edit_command == 'code':
            workspaces = list(self.path.glob('*.code-workspace'))
            if workspaces:
                run([self.edit_command, workspaces[0]])
            else:
                run([self.edit_command, self.code_path])
        if self.edit_path:
            path = self.code_path / self.edit_path
        else:
            path = self.code_path
        run([self.edit_command, path])


    def start(self):
        print_summary(self)
        self.edit()
        self.build()
        self.show_output()

    def show_output(self):

        if self.kind.category == 'web':
            self.serve()
            self.show_in_browser()

        elif self.kind.category == 'document':
            self.open_document()

        else:
            raise Exception('')


class Kind:
    _store = {}
    ready = False

    @classmethod
    def init(cls):
        for kind_dir in USER_KINDS_DIR.iterdir():
            key = kind_dir.name
            try:
                with open(kind_dir / 'config.toml') as f:
                    config_dict = toml.load(f)
            except:
                continue
            kind = Kind(dictionary=config_dict, key=key)
            cls._store[key] = kind
        cls.ready = True


        # with USER_KINDS_CONFIG_PATH.open() as f:
        #     try:
        #         config = toml.load(f)
        #     except Exception:
        #         print_error(f'We could not read the config file {USER_KINDS_CONFIG_PATH}')
        #         return
        #     for title, kind_dictionary in config.items():
        #         kind = Kind(dictionary=kind_dictionary, title=title)
        #         cls.store[title] = kind

    @staticmethod
    def get(key):
        return Kind._store.get(key, None)

    @classmethod
    def all(cls):
        return cls._store.values()

    def __init__(self, dictionary, key):
        if 'root' in dictionary:
            self.root = Path(dictionary['root'])
        self._dictionary = dictionary
        self.key = key
        if 'category' in dictionary:
            self.category = Category.get(dictionary['category'])
        self.template_directory = USER_KINDS_DIR / key / 'template'
        self.config_path = USER_KINDS_DIR / key / 'config.toml'

    def __getattr__(self, item):
        if item in self._dictionary:
            return self._dictionary[item]
        else:
            raise AttributeError

    def __str__(self):
        return self.key

    def print(self):
        print(self.__dict__)


    # def get_template_path(self, component: str) -> Path:
    #     if component in self.dictionary:
    #         return TEMPLATES_PATH / self.dictionary[component]['template']
    #     else:
    #         print(f'No template defined for {component} in {self}')
    #         exit()
    # todo

    def get_component_path(self, component: str) -> Path:
        if component in self.dictionary:
            return self.dictionary[component]['path']
        else:
            print(f'No {component} defined for {self}')
            exit()


class Category:
    _store = {}
    ready = False

    @classmethod
    def init(cls):
        with USER_BASE_CONFIG_PATH.open() as f:
            config = toml.load(f)
            categories_dict = config['category']
        for key, category_dict in categories_dict.items():
            cls._store[key] = Category(dictionary=category_dict, key=key)
        cls.ready = True

    @classmethod
    def all(cls):
        return cls._store.values()

    @classmethod
    def get(cls, key):
        if key in cls._store:
            return cls._store[key]
        else:
            raise KeyError

    def __init__(self, dictionary: dict, key: str):
        self._dictionary = dictionary
        self.key = key

    def __getattr__(self, item):
        if item in self._dictionary:
            return self._dictionary[item]
        else:
            raise AttributeError

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.key


def create_project(kind_key:str, title: str):
    kind = Kind.get(kind_key)
    root = Path('.')

    directory_name = title.replace(' ', '-')

    source = kind.template_directory
    destination = root / directory_name
    copytree(source, destination)

    save_project_config(path=destination / PROJECT_CONFIG_FILENAME, kind_key=kind.key, title=title)

    project = Project.from_path(destination)
    project.start()


def save_project_config(path: Path, kind_key: str = None, title: str = None, shortcut: str = None):
    data = {}
    if kind_key:
        data['kind'] = kind_key
    if title:
        data['title'] = title
    if shortcut:
        data['shortcut'] = shortcut
    with path.open('w') as f:
        toml.dump(data, f)


def print_error(string, color='red'):
    secho('==> Problem: ', fg=color, nl=False)
    echo(string)


def print_summary(object, additional_keys: List[str]=None, primary_color='yellow'):
    secho('------------------------------------------------------------------------', fg=primary_color)
    if object.title:
        secho('title: ', nl=False, fg=primary_color)
        secho(object.title.upper(), bold=True)

    if additional_keys:
        keys = additional_keys + BaseConfig.get('keys')
    else:
        keys = BaseConfig.get('keys')

    for key in keys:
        if key in ['title']: continue
        key = key.replace('-', '_')
        if hasattr(object, key) and getattr(object, key):
            secho(f'{key.replace("_", "-")}: ', nl=False, fg=primary_color)
            echo(f'{getattr(object, key)}')
    secho('------------------------------------------------------------------------', fg=primary_color)


for cls in (Category, Kind, Project):
    if not cls.ready:
        cls.init()
