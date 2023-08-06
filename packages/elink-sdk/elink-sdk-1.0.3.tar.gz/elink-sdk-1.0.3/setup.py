from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='elink-sdk',
    version='1.0.3',
    author="ELinkGate",
    author_email="kevin.truong@elinkgate.com",
    description="ELink SDK for python",
    long_description=long_description,
    url="http://www.elinkgate.com",
    packages=['elink_sdk'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
