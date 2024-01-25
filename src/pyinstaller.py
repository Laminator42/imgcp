import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / 'main.py')


def install():
    PyInstaller.__main__.run(
        [
            path_to_main,
            '--onefile',
            '--clean',
            '-n',
            'imgcp',
        ]
    )


if __name__ == '__main__':
    install()
