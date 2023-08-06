from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='gplay',
        version='1.0.6',
        description='A Google Play Api Command Line Interface (CLI)',
        long_description=long_description,
        url='https://github.com/nassendelft/google-play-cli',
        author='Nick Assendelft',
        author_email='n.assendelft@gmail.com',
        license='GPL-3.0',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
        keywords='cli command-line google google-api api play google-play',
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        py_modules=["gplay", "google_play_api"],
        install_requires=['google-api-python-client', 'docopt'],
        entry_points={
            'console_scripts': [
                'gplay = gplay:do_action',
            ],
        },
)
