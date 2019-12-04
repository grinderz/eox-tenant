""" Backend abstraction. """

from microsite_configuration.microsite import (  # pylint: disable=import-error
    get_value,
)

from eox_tenant.backends.base import AbstractBaseMicrositeBackend


def get_base_microsite_backend():
    """ Backend to get BaseMicrositeBackend. """
    try:
        from microsite_configuration.backends.base import BaseMicrositeBackend as InterfaceConnectionBackend
    except ImportError:
        InterfaceConnectionBackend = AbstractBaseMicrositeBackend
    return InterfaceConnectionBackend


def get_microsite_get_value(*args, **kwargs):
    """ Backend to get get_value. """
    return get_value(*args, **kwargs)
