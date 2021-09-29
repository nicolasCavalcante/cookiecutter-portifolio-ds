import platform
import subprocess
from pathlib import Path

CMD_SEP = '&' if platform.system() == 'Windows' else ';'

SELF_PATH = Path(__file__).parent.absolute()
spathsrt = '"%s/"' % SELF_PATH.as_posix()
# DOIT_CONFIG = {'default_tasks': ['format', 'pytest']}


def syscmd(string):
    subprocess.call(string, shell=True)
    return True


def task_format():
    return {
        'actions': [
            'autoflake -i -r --expand-star-imports --remove-all-unused-imports'
            + ' --remove-duplicate-keys --remove-unused-variables .' +
            ' %s isort . %s yapf -i -r .' % (CMD_SEP, CMD_SEP)
        ],
        'verbosity':
        2
    }


def task_pytest():
    """run pytests under tests folder"""
    return {'actions': [lambda: syscmd('pytest tests/')], 'verbosity': 2}
