from pathlib import Path
import subprocess

SELF_PATH = Path(__file__).parent.absolute()
# DOIT_CONFIG = {'default_tasks': ['devinstall', 'autopep']}


def syscmd(string):
    subprocess.check_call(string, shell=True)
    return True


def task_devinstall():
    """install development packages"""
    yield {
        'name': 'install editable package',
        'actions': [lambda: syscmd('pip install -e "' + str(SELF_PATH) + '"')],
        'verbosity': 2,
        'file_dep': [SELF_PATH / 'setup.py']
    }
    yield {
        'name':
        'install development requeirments',
        'actions': [
            lambda: syscmd('pip install -r "' + str(
                SELF_PATH / 'requirements/dev.txt') + '"')
        ],
        'verbosity':
        2,
        'file_dep': [SELF_PATH / 'requirements/dev.txt']
    }


def task_autopep():
    """lint codebase using yapf acording to PEP8"""
    def autopep(filepath: Path):
        from yapf.yapflib.yapf_api import FormatFile
        FormatFile(str(filepath), in_place=True)

    nparts = len(SELF_PATH.parts)
    for filepath in SELF_PATH.glob('**/*.py'):
        yield {
            'name': '/'.join(filepath.parts[nparts:]),
            'actions': [(autopep, [], {
                'filepath': filepath
            })],
            'file_dep': [filepath]
        }


def task_pytests():
    """run pytests under tests folder"""

    path = SELF_PATH / 'tests'
    nparts = len(path.parts)
    for filepath in (x for x in SELF_PATH.glob('**/*.py') if 'test' in x.name):
        if not filepath.is_file():
            continue
        yield {
            'name': '/'.join(filepath.parts[nparts:]),
            'actions': [lambda: syscmd(f'pytest --testmon "{filepath}"')],
            'verbosity': 2
        }
