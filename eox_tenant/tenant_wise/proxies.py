"""
Tenant wise proxies that allows to override the platform models.
"""
import logging
import json
from itertools import chain

import six
from django.conf import settings
from django.core.cache import cache

from eox_tenant.edxapp_wrapper.site_configuration_module import get_site_configuration_models
from eox_tenant.models import TenantConfig, Microsite

SiteConfigurationModels = get_site_configuration_models()
TENANT_ALL_ORGS_CACHE_KEY = "tenant.all_orgs_list"
EOX_TENANT_CACHE_KEY_TIMEOUT = getattr(
    settings,
    "EOX_TENANT__CACHE_KEY_TIMEOUT",
    300
)
TENANT_MICROSITES_ITERATOR_KEY = "tenant-microsites-iterator"
logger = logging.getLogger(__name__)


class TenantSiteConfigProxy(SiteConfigurationModels.SiteConfiguration):
    """
    This a is Proxy model for SiteConfiguration from <openedx.core.djangoapps.site_configuration.models>.
    This allows to add or override methods using as base the SiteConfiguration model.
    More information in https://docs.djangoproject.com/en/3.0/topics/db/models/#proxy-models
    """

    class Meta:
        """ Set as a proxy model. """
        proxy = True

    def __unicode__(self):
        key = getattr(settings, "EDNX_TENANT_KEY", "No tenant is active at the moment")
        return u"<Tenant proxy as site_configuration: {}>".format(key)

    @property
    def enabled(self):
        """
        Return True if EDNX_TENANT_KEY is in the current settings.
        """
        if getattr(settings, 'EDNX_TENANT_KEY', None):
            return True
        return False

    @enabled.setter
    def enabled(self, value):
        """
        We ignore the setter since this is a read proxy.
        """
        pass

    def get_value(self, name, default=None):
        """
        Return Configuration value from the Tenant loaded in the settings object
        as if this was a SiteConfiguration class.
        """
        try:
            return getattr(settings, name, default)
        except AttributeError as error:
            logger.exception("Invalid data at the TenantConfigProxy get_value. \n [%s]", error)

        return default

    def save(self, *args, **kwargs):
        """
        Don't allow to save TenantSiteConfigProxy model in database.
        """
        pass

    @classmethod
    def get_all_orgs(cls):
        """
        This returns a set of orgs that are considered within all microsites and TenantConfig.
        This can be used, for example, to do filtering
        """
        # Check the cache first
        org_filter_set = cache.get(TENANT_ALL_ORGS_CACHE_KEY)
        if org_filter_set:
            return org_filter_set

        org_filter_set = set()
        if not cls.has_configuration_set():
            return org_filter_set

        tenant_config = TenantConfig.objects.values_list("lms_configs")
        microsite_config = Microsite.objects.values_list("values")  # pylint: disable=no-member

        for config in chain(tenant_config, microsite_config):
            try:
                current = json.loads(config[0])
                org_filter = current.get("course_org_filter", {})
            except IndexError:
                continue

            if org_filter and isinstance(org_filter, list):
                for org in org_filter:
                    org_filter_set.add(org)
            elif org_filter:
                org_filter_set.add(org_filter)

        cls.set_key_to_cache(TENANT_ALL_ORGS_CACHE_KEY, org_filter_set)

        return org_filter_set

    @classmethod
    def get_value_for_org(cls, org, val_name, default=None):
        """
        Returns a configuration value for a microsite or TenantConfig which has an org_filter that matches
        what is passed in.
        """

        if not cls.has_configuration_set():
            return default

        cache_key = "org-value-{}-{}".format(org, val_name)
        cached_value = cache.get(cache_key)

        if cached_value:
            return cached_value

        tenant_config = TenantConfig.objects.values_list("lms_configs")
        microsite_config = Microsite.objects.values_list("values")  # pylint: disable=no-member

        for config in chain(tenant_config, microsite_config):
            try:
                current = json.loads(config[0])
                org_filter = current.get("course_org_filter", {})
            except IndexError:
                continue

            if org_filter:
                if isinstance(org_filter, six.string_types):
                    org_filter = set([org_filter])
                if org in org_filter:
                    result = current.get(val_name, default)
                    cls.set_key_to_cache(cache_key, result)
                    return result

        return default

    @classmethod
    def has_configuration_set(cls):
        """
        We always require a configuration to function, so we can skip the query
        """
        return getattr(settings, "USE_EOX_TENANT", False)

    @classmethod
    def set_key_to_cache(cls, key, value):
        """
        Stores a key value pair in a cache scoped to the thread
        """
        cache.set(
            key,
            value,
            EOX_TENANT_CACHE_KEY_TIMEOUT
        )