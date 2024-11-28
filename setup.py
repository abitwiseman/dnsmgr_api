from setuptools import setup, find_packages

setup(
    name="dnsmgr_api",
    version="1.0.0",
    description="A Python library to configure named (BIND) and dnsmasq on remote servers via SSH.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="abwm",
    author_email="abitwiseman@gmail.com",
    url="https://github.com/abitwiseman/dnsmgr_api",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "paramiko>=2.11.0",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
