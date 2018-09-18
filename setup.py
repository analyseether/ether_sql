#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup,
)


setup(
    name='ether_sql',
    version='0.1.3',
    description="""A python library to push ethereum blockchain data into an sql database.""",
    long_description_markdown_filename='README.md',
    author='Ankit Chiplunkar',
    author_email='ankit@analyseether.com',
    url='https://github.com/analyseether/ether_sql',
    include_package_data=True,
    install_requires=[
        "web3==4.4.1",
        "sqlalchemy==1.2.4",
        "alembic==0.9.9",
        "psycopg2-binary==2.7.4",
        "Click==6.7",
	"Celery==4.1.1",
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6, <4',
    extras_require={
        'tester': [
            "pytest==3.0.0",
            "pytest-cov==2.2.1",
        ],
        'linter': [
            "flake8==3.4.1",
            "isort>=4.2.15,<5",
        ],
    },
    entry_points='''
        [console_scripts]
        ether_sql=ether_sql.cli:cli
    ''',
    py_modules=['ether_sql'],
    zip_safe=False,
    keywords='ethereum',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
