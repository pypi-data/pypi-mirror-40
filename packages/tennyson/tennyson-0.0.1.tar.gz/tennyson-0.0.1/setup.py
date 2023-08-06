from setuptools import setup

setup(
    name='tennyson',
    version='0.0.1',
    packages=['tennyson',],
    license='None',
    long_description=open('README.md').read(),
    test_suite='nose.collector',
    tests_require=['nose']
)
