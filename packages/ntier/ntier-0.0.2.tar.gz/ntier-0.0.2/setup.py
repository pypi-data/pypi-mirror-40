'''Setup for package.'''
import pathlib
from setuptools import (setup)

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
VERSION = '0.0.2'

setup(
    name='ntier',
    version=VERSION,
    description=(
        'A library containing data structures and classes used in making the domain layer '
        'of n-tier web applications'
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    author='Trey Cucco',
    author_email='fcucco@gmail.com',
    url='https://gitlab.com/tcucco/ntier',
    download_url='https://gitlab.com/tcucco/ntier/-/archive/master/ntier-master.tar.gz',
    packages=['ntier'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    platforms='any',
)
