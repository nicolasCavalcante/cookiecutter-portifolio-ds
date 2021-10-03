"""Script that runs after the project generation phase."""
import subprocess
from pathlib import Path

PROJECT_DIRECTORY = Path.cwd()

if "{{ cookiecutter.open_source_license }}" == "Not open source":
    (PROJECT_DIRECTORY / "LICENSE").unlink()

if "{{ cookiecutter.setup_project }}" == "Yes - select this":
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', '*'])
    subprocess.call(['git', 'commit', '-m', 'Initial commit'])
    subprocess.call(['pipenv', 'install', '--dev', '--skip-lock'])
    subprocess.call(['pipenv', 'shell'])
