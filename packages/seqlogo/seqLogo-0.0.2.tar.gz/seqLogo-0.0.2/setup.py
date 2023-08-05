from setuptools import setup
import os
import sys

__version__ = '0.0.2'

def readme():
    path = os.path.dirname(__file__) if os.path.dirname(__file__) else '.'
    with open(path + '/README.rst') as rst:
        return rst.read()

setup(
    name='seqLogo',
    version=__version__,
    description='Python port of the R Bioconductor `seqLogo` package ',
    long_description=readme(),
    url='https://github.com/betteridiot/seqLogo',
    author='Marcus D. Sherman',
    author_email='mdsherm@umich.edu',
    license='BSD 3-Clause',
    install_requires=[
        'numpy',
        'pandas',
        'weblogo'
    ],
    packages=['seqLogo'],
    package_dir={'seqLogo': './seqLogo'},
    package_data={'seqLogo': ['docs/*', 'LICENSE', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    keywords='sequence logo seqlogo bioinformatics genomics weblogo',
    include_package_data=True,
    zip_safe=False
)

