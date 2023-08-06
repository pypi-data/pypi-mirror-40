from setuptools import setup, find_packages


setup(
    name="textexploration",
    version="0.2.0",
    author="Matthijs Brouwer",
    packages=find_packages(),
    license="LICENSE.txt",
    long_description=open("README.txt").read(),
    install_requires=[
        "requests >= 2.21.0",
        "pandas",
    ],
)

