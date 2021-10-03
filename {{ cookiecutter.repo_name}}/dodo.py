import platform
import subprocess
from pathlib import Path

from {{cookiecutter.repo_name}}.utils import MLFLOW_DIR

CMD_SEP = '&' if platform.system() == 'Windows' else ';'
SELF_PATH = Path(__file__).parent.absolute()
DOIT_CONFIG = {'default_tasks': ['format', 'pytest']}


def syscmd(string):
    subprocess.call(string, shell=True)
    return True


def task_format():
    """makes code organized and pretty"""
    nparts = len(SELF_PATH.parts)
    for filepath in SELF_PATH.glob('**/*.py'):
        if str(filepath).startswith(str(SELF_PATH / 'output')):
            continue
        yield {
            'name':
            '/'.join(filepath.parts[nparts:]),
            'actions':
            [('autoflake -i -r --expand-star-imports' +
              ' --remove-all-unused-imports' +
              ' --remove-duplicate-keys --remove-unused-variables %s' +
              ' %s isort %s %s yapf -i -r %s') %
             (filepath, CMD_SEP, filepath, CMD_SEP, filepath)],
            'file_dep': [filepath],
            'verbosity':
            2
        }


def task_pytest():
    """run pytests under tests folder"""
    return {'actions': [lambda: syscmd('pytest tests/')], 'verbosity': 2}


def task_ui():
    """start mlflow ui"""
    return {
        'actions':
        ['mlflow ui --backend-store-uri file:%s' % MLFLOW_DIR.as_posix()],
        'verbosity':
        2
    }
