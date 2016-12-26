from setuptools import setup, find_packages

setup(
    name="simnav",
    version="0.0.2",
    packages=find_packages(),
    package_data={
        '':['propiedades.sqlite']
    }
)
