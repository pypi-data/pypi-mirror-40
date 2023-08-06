from distutils.command.install import INSTALL_SCHEMES

from setuptools import setup, find_packages

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='elink-sdk',
    version='1.0.2',
    author="ELinkGate",
    author_email="kevin.truong@elinkgate.com",
    description="ELink SDK for python",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="http://www.elinkgate.com",
    packages=['elink'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
