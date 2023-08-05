# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

NAME = "groupdocs-signature-cloud"
VERSION = "18.8.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
TEST_REQUIRES = ["asposestoragecloud >= 1.0.5"]

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
TEST_REQUIRES = ['asposestoragecloud >= 1.0.5']

setup(
    name=NAME,
    version=VERSION,
    description="GroupDocs.Signature Cloud SDK for Python allows you to use GroupDocs.Signature APIs in your Python applications",
	author="GroupDocs Signature",
    author_email="groupdocs.cloud@asposeptyltd.com",
    url="https://github.com/groupdocs_signature_cloud/groupdocs_signature_cloud-python",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Libraries",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
	],
    keywords=["groupdocs", "signature", "cloud", "python", "sdk"],
    install_requires=[
        'six',
        'certifi',
        'asposestoragecloud'
    ],
	tests_require=TEST_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""
    This repository contains GroupDocs Signature Cloud SDK for Python source code. This SDK allows you to work with GroupDocs Signature Cloud REST APIs in your Python applications quickly and easily, with zero initial cost.
    """,
    long_description_content_type="text/markdown"
)



