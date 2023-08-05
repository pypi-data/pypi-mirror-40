from setuptools import setup, find_packages

import ci_server


setup(
    name='gugfug-ci',
    version=ci_server.__version__,
    packages=find_packages(),

    author='gugfug',
    author_email='gugfug1@gmail.com',
    url='https://github.com/gugfug/gugfug-ci/'
)
