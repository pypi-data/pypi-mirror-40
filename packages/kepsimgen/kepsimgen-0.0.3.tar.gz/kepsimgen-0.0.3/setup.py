"""Setup kep-simgen"""
from codecs import open
from os import path
from setuptools import setup, find_packages

HERE = path.dirname(path.realpath(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='kepsimgen',
    install_requires=['keppy'],
    version='0.0.3',
    description='CLI tool that converts Kepware projects into simulation projects',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/jmbeach/kep-simgen',
    author='jmbeach',
    author_email='jaredbeachdesign@gmail.com',
    keywords='kepware simulation opc',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['kep-simgen=kep_simgen.kepware_real_to_simulation:main']
    }
)
