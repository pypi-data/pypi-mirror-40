from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='elink-sdk',
    version='1.0.0',
    author="ELinkGate",
    author_email="kevin.truong@elinkgate.com",
    description="ELink SDK for python",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="http://www.elinkgate.com",
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
