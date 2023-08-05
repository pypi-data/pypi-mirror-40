
from setuptools import setup, find_packages
from ogli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='ogli',
    version=VERSION,
    description='ogli integrates well!',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Shane Berry',
    author_email='srberry1@gmail.com',
    url='http://spectrumtech.net',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'ogli': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        ogli = ogli.main:main
    """,
)
