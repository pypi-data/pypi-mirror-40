from setuptools import setup, find_packages

setup(
    name='py-structures',
    version='0.1.0',
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    url='https://github.com/bholten/structures',
    license='MIT',
    author='Brennan Holten',
    author_email='bholten@protonmail.ch',
    description='Pseudo C-style structs for Python'
)
