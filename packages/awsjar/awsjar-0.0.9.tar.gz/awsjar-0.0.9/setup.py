from setuptools import setup, find_packages
import versioneer

with open('requirements.txt', 'r') as reqfile:
    requirements = [x.strip() for x in reqfile if x.strip()]

setup(
    name="awsjar",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Jar saves the state of your AWS Lambda functions",
    packages=['awsjar'],
    url="https://github.com/ysawa0/awsjar",
    license="Apache 2.0",
    author="Yuki Sawa",
    author_email="yukisawa@gmail.com",
    install_requires=requirements,
    classifiersa=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
    ],
)
