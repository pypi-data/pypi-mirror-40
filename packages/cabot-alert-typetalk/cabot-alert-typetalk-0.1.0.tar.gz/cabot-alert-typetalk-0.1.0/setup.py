from setuptools import setup, find_packages
from os import path
from io import open

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='cabot-alert-typetalk',
    version='0.1.0',
    description='',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Issei Horie',
    author_email='is2ei.horie@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='cabot alert typetalk',
    url='https://github.com/is2ei/cabot-alert-typetalk',
    packages=find_packages(),
    project_urls={
        'Bug Reports': 'https://github.com/is2ei/cabot-alert-typetalk/issues',
        'Source': 'https://github.com/is2ei/cabot-alert-typetalk',
    },
)
