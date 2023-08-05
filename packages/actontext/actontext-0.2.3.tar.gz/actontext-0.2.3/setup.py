import setuptools
from distutils.core import Extension

long_description = """# actontext

This module provides functions to load COM DLL on Windows machine, to avoid registering it in Windows registry.
You can find more about how it can be done in articles on web:
- [Registration-Free Activation of COM Components: A Walkthrough](https://docs.microsoft.com/en-us/previous-versions/dotnet/articles/ms973913(v=msdn.10));
- [Create side-by-side registrationless COM manifest with VS](https://weblog.west-wind.com/posts/2011/Oct/09/An-easy-way-to-create-Side-by-Side-registrationless-COM-Manifests-with-Visual-Studio);
- etc. just Google it

Possibly the main use case for package could be lightweight testing of COM objects, created from built in-proc COM servers
"""

setuptools.setup(
    name = 'actontext',
    packages = ['actontext'],
    version = '0.2.3',
    license='MIT',
    description = "This module provides functions to load COM DLL on Windows machine, to avoid registering it in Windows registry.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Mokych Andrey',
    author_email = 'mokych.apriorit@gmail.com',
    url = 'https://github.com/mettizik/pyactontext',
    download_url = 'https://github.com/mettizik/pyactontext/archive/v0.2.3.tar.gz',
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
