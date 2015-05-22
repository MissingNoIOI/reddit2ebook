"""Convert reddit stories and comments into ebooks
See:
https://github.com/MissingNoIOI/reddit2ebook
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

    setup(
        name='reddit2ebook',

        version='1.0.7',

        description = 'convert reddit stories and comments into ebooks',
        long_description = long_description,

        url = 'https://github.com/MissingNoIOI/reddit2ebook',

        author = 'Gerrit Helling',
        author_email = 'gerrit@akuma.pictures',

        license = 'GPLv3',

        classifiers = [

            'Development Status :: 4 - Beta',

            'Intended Audience :: End Users/Desktop',
            'Topic :: Multimedia',

            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],

        keywords = 'reddit ebook epub pandoc offline',

        packages = find_packages(),

        install_requires = [
            'pypandoc',
            'praw',
            'PyYaml'],

        entry_points = {
            'console_scripts': [
                'reddit2ebook=reddit2ebook.main:main',
            ],
        },
    )
