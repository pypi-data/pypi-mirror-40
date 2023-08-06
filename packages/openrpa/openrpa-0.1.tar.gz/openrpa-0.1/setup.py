from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='openrpa',
    version='0.1',
    license='Apache License 2.0',
    keywords=['python', 'robotframework', 'rpa'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    author='Orlof',
    author_email='orlof@users.noreply.github.com',

    url='http://github.com/robocorp/openrpa',

    packages=['openrpa'],
    entry_points = {'console_scripts': ['openrpa = openrpa.run:run_cli']},

    description='OpenRPA',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
