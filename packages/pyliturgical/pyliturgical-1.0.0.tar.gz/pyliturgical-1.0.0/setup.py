import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "1.0.0"

with open("README.md", "r") as fh:
    long_description = fh.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            sys.exit(
                "Git tag: %s does not match the version of this app: %s" %
                (tag, VERSION)
            )


setup(
    name="pyliturgical",
    version=VERSION,
    author="Ian Turner",
    author_email="ian@pizen.io",
    description="Package for generating liturgial information for a date",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pizen/pyliturgical",
    packages=['pyliturgical'],
    setup_requires=[
        'pytest-runner'
    ],
    install_requires=[
        'python-dateutil'
    ],
    tests_require=[
        'pytest'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Religion"
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
