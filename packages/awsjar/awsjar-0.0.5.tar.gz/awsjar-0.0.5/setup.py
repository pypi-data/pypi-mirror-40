from setuptools import setup, find_packages


setup(
    name="awsjar",
    version="0.0.5",
    description="Jar saves the state of your AWS Lambda functions",
    packages=find_packages(include=["awsjar"]),
    url="https://github.com/ysawa0/awsjar",
    license="Apache 2.0",
    author="Yuki Sawa",
    author_email="yukisawa@gmail.com",
    install_requires=["boto3>=1.7.4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
    ],
)
