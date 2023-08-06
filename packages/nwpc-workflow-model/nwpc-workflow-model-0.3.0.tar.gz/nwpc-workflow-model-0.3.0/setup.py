from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nwpc-workflow-model',

    version='0.3.0',

    description='A workflow model using in operation systems at NWPC.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/perillaroc/nwpc-workflow-model',

    author='perillaroc',
    author_email='perillaroc@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],

    keywords='nwpc workflow model',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],

    extras_require={
        'test': ['pytest'],
        'cov': ['pytest-cov', 'codecov']
    },

    entry_points={}
)
