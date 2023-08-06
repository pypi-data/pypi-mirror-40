from os import path
from setuptools import setup, find_packages

VERSION = '0.8'


directory = path.dirname(path.abspath(__file__))
with open(path.join(directory, 'requirements.txt')) as f:
    required = f.read().splitlines()


setup(
    name='bgpack',
    version=VERSION,
    description='BBGLab tool',
    packages=find_packages(),
    install_requires=required,
    author="Barcelona Biomedical Genomics Lab",
    author_email="bbglab@irbbarcelona.org",
    license="Apache Software License 2.0",
    entry_points={
            'console_scripts': [
                'bgpack = bgpack.cli:cli'
            ]
        }
)