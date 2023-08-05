"""
This module provides functions to load COM DLL on Windows machine, to avoid registering it in Windows registry.
You can find more about how it can be done in articles on web:
- \"Registration-Free Activation of COM Components: A Walkthrough\" (https://docs.microsoft.com/en-us/previous-versions/dotnet/articles/ms973913(v=msdn.10));
- \"Create side-by-side registrationless COM manifest with VS\" (https://weblog.west-wind.com/posts/2011/Oct/09/An-easy-way-to-create-Side-by-Side-registrationless-COM-Manifests-with-Visual-Studio);
- etc. just Google it

The main use case for module could be lightweight testing of COM objects, created from built in-proc COM servers
"""

from actontext.commandor import Commandor, comtypes, load_side_by_side_dll
from actontext_internal import activate
