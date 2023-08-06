import numpy as np
from setuptools import setup, Extension, find_packages

with open('README.md') as f:
    readme = f.read()

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
    version='0.1.1',
    author='Matej Usaj',
    author_email='usaj.m@utoronto.ca',
    description='SAFE implementation for Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/usajusaj/safe',
    packages=find_packages(),
    install_requires=required,
    license="MIT",
    ext_modules=ext_modules,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
