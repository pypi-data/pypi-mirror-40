from setuptools import find_packages, setup

readme = open('./README.md').read()

setup(
    name='filee',
    version='0.0.4',
    description='A command to save / load files with JSON input / output.',
    long_description=readme,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'filee = filee.main:cli'
        ]
    }
)
