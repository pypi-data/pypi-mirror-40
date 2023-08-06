from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="py-ninjarmm-api-client",
    version="0.0.3",
    author="Guy Zuercher",
    author_email="geeosor@gmail.com",
    description="Unoffical NinjaRMM API client in Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/raptus-it-services/py-ninjarmm-api-client",
    packages=["ninjarmm_api"],
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
)
