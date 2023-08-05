import setuptools
from distutils.core import Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'actontext',
    packages = ['actontext'],
    version = '0.2.1',
    license='MIT',
    description = "This module provides functions to load COM DLL on Windows machine, to avoid registering it in Windows registry.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Mokych Andrey',
    author_email = 'mokych.apriorit@gmail.com',
    url = 'https://github.com/mettizik/pyactontext',
    download_url = 'https://github.com/mettizik/pyactontext/archive/v0.2.1.tar.gz',
    keywords = ['COM', 'ATL', 'side-by-side', 'activation context'],
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
      "Operating System :: Microsoft :: Windows",
    ],
    ext_modules=[
        Extension('actontext_internal', ['native/actonext.cpp'])],
    install_requires=['comtypes']
)
