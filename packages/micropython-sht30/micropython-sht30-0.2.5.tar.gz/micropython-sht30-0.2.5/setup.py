import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip


setup(
    name="micropython-sht30",
    version='0.2.5',
    description="SHT30 sensor driver for micropython: IC2 bus",
    author="Roberto Sánchez",
    author_email="matt@schinckel.net",
    packages=['sht30'],
    include_package_data=True,
    exclude_package_data={
        '': ['test*.py', 'tests/*.env', '**/tests.py'],
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Other OS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Home Automation',
    ],
)
