from os import path

from setuptools import setup, find_packages  # noqa: H301

NAME = "smklog"
VERSION = "0.1.2"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = []

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="Samarkand logger",
    author="David Chen",
    author_email="david.chen@samarkand.global",
    url="https://gitlab.com/samarkand-util/smklog",
    keywords=["logger"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
)
