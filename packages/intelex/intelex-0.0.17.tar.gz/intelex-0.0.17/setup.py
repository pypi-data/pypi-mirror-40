from setuptools import setup

with open('README.md', 'r') as fh:
    long_desc = fh.read()

setup(
    name='intelex',
    version='0.0.17',
    description='Intelex SDK',
    url='https://github.com/thomassampson/intelex_sdk',
    author='Thomas Sampson',
    author_email='sampsont91@gmail.com',
    py_modules=["intelex"],
    package_dir={'':'src'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    long_description=long_desc,
    long_description_content_type='text/markdown',
)