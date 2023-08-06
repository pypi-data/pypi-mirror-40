"""Packaging settings."""


from setuptools import Command, find_packages, setup
from fsyncer import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fsyncer',
    version=__version__,
    description='Keep your repositories up-to-date all the time.',
    long_description=long_description,
    url='https://github.com/Skarlso/fsyncer',
    author='Gergely Brautigam',
    author_email='gergely.brautigam@gmail.com',
    license='LICENSE',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cli,git',
    packages=find_packages(exclude=['docs', 'test*']),
    install_requires=['PyGithub'],
    entry_points={
        'console_scripts': [
            'fsyncer=fsyncer.fsyncer:main',
        ],
    }
)