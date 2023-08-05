#!/usr/bin/env python3
from os import environ, listdir
from os.path import join, expanduser
from pathlib import Path
from subprocess import run

from click import argument, command
from pick import pick

POTENTIAL_FILENAMES = ('config.toml', 'config.yaml', 'config.yml', 'config.fish')
CONFIG_HOME = Path(environ.get('XDG_CONFIG_HOME', '~/.config')).expanduser()
SETUP = Path.home() / '.setup'


def get_nonstandard_configpath(app: str) -> Path:
    paths = {
        'brew': SETUP / 'bin' / 'install-brew-stuff'
    }
    return paths.get(app, None)


@command()
@argument('app')
def conf(app):

    nonstandard_path = get_nonstandard_configpath(app)

    if nonstandard_path:
        config_file = nonstandard_path
    else:
        if CONFIG_HOME / app in CONFIG_HOME.iterdir():
            app_config_dir = CONFIG_HOME / app
            files = list(app_config_dir.iterdir())
            if len(files) == 0:
                print(f'Empty config directory {app_config_dir}')
                return
            elif len(files) == 1:
                config_file = files[0]
            else:
                config_file, _ = pick(files, 'Which file do you want to edit?')
            # for filename in POTENTIAL_FILENAMES:
            #     if app_config_dir / filename in app_config_dir.iterdir():
            #         config_file = app_config_dir / filename

    run([environ['EDITOR'], str(config_file)])