from setuptools import setup
import os

setup(
    name='gtmunit1',
    version=os.environ['VERSION'],

    description='Package 1 for Gigantum Client unit testing.',
    long_description='This package does not contain any real functionality. '
                     'It exists for unit testing the pip integration for the Gigantum Client',

    author='Gigantum',
    author_email='hello@gigantum.com',

    packages=['gtmunit1'],

    url='https://github.com/gigantum/gigantum-client',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
    ],
    keywords=[]
)
