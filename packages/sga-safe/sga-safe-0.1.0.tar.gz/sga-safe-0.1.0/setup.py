import numpy as np
from setuptools import setup, Extension, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

ext_modules = [
    Extension(
        "safe.safe_calc",
        ["safe/safe_calc.pyx"],
        language="c++",
        include_dirs=[np.get_include()],
        libraries=['gsl', 'gslcblas']
    )
]

setup(
    name="sga-safe",
    version='0.1.0',
    description='SGA Utilities',
    long_description=readme,
    install_requires=required,
    license=lic,
    author='Matej Usaj',
    author_email='usaj.m@utoronto.ca',
    url='https://github.com/usajusaj/safe',
    ext_modules=ext_modules,
    packages=find_packages(),
)
