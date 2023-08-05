from setuptools import setup
from os import path

setup(
    name='radio_t',
    version='1.0',
    description='Radio-T API Wrapper for Python.',
    url='https://github.com/ketsu8/radio-t-wrapper',
    author='ketsu8',
    author_email='ilya.breytburg@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='radio-t python',
    packages=['radio_t'],
    install_requires=['requests'],
    project_urls={
        'Bug Reports': 'https://github.com/ketsu8/radio-t-wrapper/issues',
        'Source': 'https://github.com/ketsu8/radio-t-wrapper',
    },
)
