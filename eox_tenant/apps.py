"""
File configuration for eox-tenant.
"""
from django.apps import AppConfig


class EdunextOpenedxExtensionsTenantConfig(AppConfig):
    """
    App configuration
    """
    name = 'eox_tenant'
    verbose_name = "Edunext Openedx Multitenancy."

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'aws': {'relative_path': 'settings.aws'},
            },
            'cms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'aws': {'relative_path': 'settings.aws'},
            },
        },
        'signals_config': {
            'lms.djangoapp': {
                'relative_path': 'signals',
                'receivers': [
                    {
                        'receiver_func_name': 'start_tenant',
                        'signal_path': 'django.core.signals.request_started',
                    },
                    {
                        'receiver_func_name': 'finish_tenant',
                        'signal_path': 'django.core.signals.request_finished',
                    },
                    {
                        'receiver_func_name': 'clear_tenant',
                        'signal_path': 'django.core.signals.got_request_exception',
                    },
                ],
            }
        },
    }
