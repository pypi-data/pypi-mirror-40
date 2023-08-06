from setuptools import setup

from dab import __version__


setup(
    name='dab',
    version=__version__,
    description='does not stand for "doin\' a build"',
    url='https://bigdickenergy.club/dab',
    entry_points={
        'console_scripts': [
            'dab=dab.__main__:main',
        ],
    })
