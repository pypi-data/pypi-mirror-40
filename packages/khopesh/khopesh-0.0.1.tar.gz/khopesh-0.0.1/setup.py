import json
from setuptools import setup

VERSION = '0.0.1'

try:
    with open('README.MD') as readme_file:
        README = readme_file.read()
except FileNotFoundError:
    README = ""

try:
    with open("Pipfile.lock") as pipfile:
        JSON_PIPFILE = json.load(pipfile)
        INSTALL_REQUIRES = []
        for key, value in dict(JSON_PIPFILE["default"]).items():
            INSTALL_REQUIRES.append("{}{}".format(key, value["version"]))
except FileNotFoundError:
    INSTALL_REQUIRES = []

setup(
    name='khopesh',
    packages=['khopesh'],
    version=VERSION,
    description='',
    long_description=README,
    license='MIT',
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['khopesh=khopesh:cli'],
    },
    data_files=[('', ['Pipfile.lock'])],
    author_name='Romain Moreau',
    author_email='moreau.romain83@gmail.com',
    url='https://github.com/Varkal/khopesh',
    download_url='https://github.com/Varkal/khopesh/archive/{}.tar.gz'.format(VERSION),
    keywords=['Khopesh'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers"
    ],
)
