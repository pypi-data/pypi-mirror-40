from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

with open('VERSION', 'r') as f:
    version = f.read().strip()

setup(
    name='doppel-cli',
    packages=['doppel'],
    description='An integration testing framework for testing API similarity of software libraries.',
    long_description=readme,
    version=version,
    url='http://github.com/jameslamb/doppel',
    license='BSD 3-clause',
    maintainer='James Lamb',
    maintainer_email='jaylamb20@gmail.com',
    install_requires=[
        'click',
        'tabulate'
    ],
    package_data={
        'doppel': ['bin/analyze.R', 'bin/analyze.py']
    },
    entry_points={
        'console_scripts': [
            'doppel-describe = doppel.describe:main',
            'doppel-test = doppel.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing'
    ]
)
