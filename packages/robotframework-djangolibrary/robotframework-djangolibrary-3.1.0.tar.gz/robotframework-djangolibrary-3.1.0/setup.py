from setuptools import setup, find_packages

version = '3.1.0'

long_description = (
    open('README.rst').read() +
    '\n' +
    '\n' +
    open('CHANGES.rst').read() +
    '\n')

setup(
    name='robotframework-djangolibrary',
    version=version,
    description="A Robot Framework library for Django.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Web Environment',
        'Framework :: Robot Framework',
        'Framework :: Django',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='robotframework django test',
    author='kitconcept GmbH | Timo Stollenwerk',
    author_email='stollenwerk@kitconcept.com',
    url='https://kitconcept.com',
    license='Apache License 2.0',
    packages=find_packages(
        exclude=['ez_setup', 'examples', 'tests']
    ),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django',
        'factory_boy',
        'requests',
        'robotframework',
        'robotframework-seleniumlibrary',
        'robotframework-debuglibrary',
        'six',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
