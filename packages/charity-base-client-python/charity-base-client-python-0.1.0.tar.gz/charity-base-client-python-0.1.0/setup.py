from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='charity-base-client-python',
    version='0.1.0',
    description='A Python client library for interacting with the CharityBase REST API.',
    long_description=readme,
    author='David Kane',
    author_email='david@drkane.co.uk',
    url='https://github.com/drkane/charity-base-client-python',
    license=license,
    install_requires=requirements,
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    python_requires='>=3',
)
