from setuptools import setup, find_packages
import sys
import os
import inspect

# sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../..'))
# import mlc_tools.version as version

setup(
    name='mlc-tools',
    version='0.0.1',
    packages=find_packages(include='../../mlc_tools/'),
    long_description="mlc-tools",
    install_requires=[
        'enum'
    ]
    # entry_points={
    #     'console_scripts':
    #         ['mlc-tools = mlc_tools.main:console']
    # },
    # test_suite='tests'
)
