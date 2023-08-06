from setuptools import find_packages, setup

readme = open('./README.md').read()

setup(
    name='filee',
    version='0.0.5',
    description='A command to save / load files with JSON input / output.',
    long_description=readme,
    long_description_content_type='text/markdown',
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
