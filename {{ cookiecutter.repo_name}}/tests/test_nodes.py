from {{cookiecutter.repo_name}}.nodes import download
from {{cookiecutter.repo_name}}.utils import DATA_DIR


def test_make_dataset():
    path = DATA_DIR / '0_external/raw.csv'
    assert download()
    assert path.exists()
    assert path.is_file()
