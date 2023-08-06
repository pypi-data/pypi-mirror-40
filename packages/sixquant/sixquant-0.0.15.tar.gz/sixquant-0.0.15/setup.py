from setuptools import setup, find_packages

import sixquant

setup(
    name='sixquant',
    version=sixquant.__version__,
    packages=find_packages(),
    description='A quick and stable data source for finance data.',
    author='caviler',
    author_email='caviler@gmail.com',
    license='MIT',
    url='https://github.com/sixquant/sixquant',
    keywords='finance data',
    install_requires=['numpy', 'pandas', 'talib', 'matplotlib'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License'],
)
