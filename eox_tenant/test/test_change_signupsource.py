"""This module include a class that checks the command change_signup_source"""

import mock
from django.core.management import call_command
from django.test import TestCase


class ChangeDomainTestCase(TestCase):
    """ Test for change_signup_source command"""

    @mock.patch('eox_tenant.edxapp_wrapper.users.get_user_signup_source')
    def test_change_signupsource(self, signupsource_mock):
        """Test signup source model manager is called with the proper arguments"""
        signupsource_filtered = mock.MagicMock()
        signupsource = mock.MagicMock()
        signupsource.objects.filter.return_value = signupsource_filtered
        signupsource_mock.return_value = signupsource

        call_command('change_signup_sources', "--from", "example1.edunext.co", "--to", "example2.edunext.co")
        signupsource.objects.filter.assert_called_with(site="example1.edunext.co")
        signupsource_filtered.update.assert_called_with(site="example2.edunext.co")
