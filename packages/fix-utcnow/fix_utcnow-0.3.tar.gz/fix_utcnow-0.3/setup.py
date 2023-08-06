
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


config = {
    'description': 'fix-utcnow',
    'author': 'Maksim Afanasevsky',
    'url': 'https://github.com/maxtwen/fix-utcnow',
    'download_url': 'https://github.com/maxtwen/fix-utcnow',
    'author_email': 'maxtwen1@gmail.com',
    'version': '0.3',
    'install_requires': [''],
    'packages': ['fix_utcnow'],
    'scripts': [],
    'name': 'fix_utcnow',
    'data_files': [('c', ['fix_utcnow/c/libfixutcnow.so'])]
    # 'long_description': read('README.md'),
    # 'long_description_content_type': 'text/markdown'
}

setup(**config)
