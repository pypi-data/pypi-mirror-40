import os
from setuptools import setup, find_packages
from io import open


with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), 'requirements_dev.txt')) as f:
    test_required = f.read().splitlines()
    if test_required[0] == "-r requirements.txt":
        test_required.pop(0)

setup(
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tokenex = tokenex.cli:handle'
        ]
    },
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
    install_requires=required,
    tests_require=test_required,
    include_package_data=True
)
