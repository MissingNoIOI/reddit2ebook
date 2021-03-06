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

        version='2.0.0',

        description='convert reddit stories and comments into ebooks',
        long_description=long_description,

        url='https://github.com/MissingNoIOI/reddit2ebook',

        author='Gerrit Helling',
        author_email='gerrit@akuma.pictures',

        license='GPLv3',

        include_package_data=True,

        classifiers=[

            'Development Status :: 4 - Beta',

            'Environment :: Console',

            'Intended Audience :: End Users/Desktop',
            'Topic :: Multimedia',

            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

            'Operating System :: OS Independent',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],

        keywords='reddit ebook epub offline',

        packages=find_packages(),

        install_requires=[
            'praw',
            'PyYaml',
            'pypub',
            'mistune',
            'pyprind',
            'Pillow',
            'lxml',
            'ebooklib',
        ],

        entry_points={
            'console_scripts': [
                'reddit2ebook=reddit2ebook.main:main',
            ],
        },

    )
