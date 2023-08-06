import os
import codecs
from setuptools import setup

import versioneer

# with open('requirements.txt', 'r') as reqfile:
#     requirements = [x.strip() for x in reqfile if x.strip()]
try:
    # Python 3
    from os import dirname
except ImportError:
    # Python 2
    from os.path import dirname

here = os.path.abspath(dirname(__file__))

with codecs.open(os.path.join(here, "docs/README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="awsjar",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Jar make it easy to store the state of your AWS Lambda functions.",
    long_description=long_description,
    packages=["awsjar"],
    url="https://github.com/ysawa0/awsjar",
    license="Apache 2.0",
    author="Yuki Sawa",
    author_email="yukisawa@gmail.com",
    install_requires=["boto3"],
    classifiersa=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Beta",
        "Natural Language :: English",
    ],
)
