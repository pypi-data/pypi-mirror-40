# encoding: utf8
import unittest
from dueros.directive.Permission.AskForPermissionsConsent import AskForPermissionsConsent
from dueros.directive.Permission.PermissionEnum import PermissionEnum


class AskForPermissionsConsentTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_permission(self):
        data = {
            'type': 'Permission.AskForPermissionsConsent',
            'permissions': [
                {
                    'name': 'RECORD::SPEECH'
                }, {
                    'name': 'READ::DEVICE:LOCATION'}
            ],
            'token': 'test_token'
        }

        directive = AskForPermissionsConsent()
        directive.add_permission(PermissionEnum.RECORD_SPEECH)
        directive.add_permission(PermissionEnum.READ_DEVICE_LOCATION)
        directive.set_token('test_token')
        self.assertEqual(directive.get_data(), data)
