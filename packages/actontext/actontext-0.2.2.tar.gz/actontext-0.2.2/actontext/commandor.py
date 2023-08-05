"""
Some wrapper utils around native 'actontext_internal' module, which allow to
load and use COM DLL without registering it in Windows registry
"""

import comtypes.client as cc
import comtypes
import actontext_internal
import logging
from os import path


def ensure_file_exists(filepath):
    if not path.exists(filepath):
        raise FileNotFoundError(filepath)


def load_side_by_side_dll(dllpath, manifestpath, logger=None):
    """
    Loads COM DLL as inproc server, using side-by-side manifest, 
    returns a generated comtypes module for the DLL or raises Runtime error if 
    fails to activate DLL context properly
    """
    if not logger:
        logger = logging.getLogger(__name__)
    ensure_file_exists(dllpath)
    ensure_file_exists(manifestpath)
    logger.debug('Loading library "{}"'.format(dllpath))
    if not path.exists(dllpath):
        raise RuntimeError('Library "{}" not found.'.format(dllpath))
    generated_module = cc.GetModule(dllpath)
    if not generated_module:
        raise RuntimeError('Failed to load library "{}"'.format(dllpath))
    logger.debug(
        'Library loaded. Initializing activation context with manifest...')
    activation_result = actontext_internal.activate(manifestpath)
    if activation_result < 0:
        raise RuntimeError('Failed to initialize activation context')

    return generated_module


class Commandor(object):
    """
    Loads activation context of the COM dll from DLL file and it's manifest file,
    allowing to use not registered in registry COM object
    """

    LOG = logging.getLogger('COMmandor')

    def __init__(self, dllpath: str, manifestpath: str, trace=False):
        if trace:
            Commandor.LOG.setLevel(logging.DEBUG)
        else:
            Commandor.LOG.setLevel(logging.INFO)

        self.__generated_module = load_side_by_side_dll(
            dllpath, manifestpath, logger=Commandor.LOG)
        Commandor.LOG.debug(
            'Activation context was initialized and activated.')

    def create_instance(self, class_guid, interface_name):
        """
        Create instance of a class with GUID and query interface from it
            @class_guid - GUID of COM class the instance of which should be created
            @interface_name - name of the interface to query on object
        """
        com_interface = getattr(self.__generated_module, interface_name)
        obj = cc.CreateObject(class_guid, interface=com_interface)
        return obj.QueryInterface(com_interface)

    def get_generated_module(self):
        """
        Get a raw instance of comtypes Module created for the given typelibrary
        """
        return self.__generated_module
