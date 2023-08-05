#!/usr/bin/env python



import unittest
import renv_device

class TestRenvDeviceInfo(unittest.TestCase):
    """test class of tashizan.py
    """
    
    def setUp(self):
        self._devUUID = "uuid-1234-5678-9012"
        self._devTypeId = "WEB.DEVICE.TEST_DEVICE"
        self._devName = "name-renv-device-name-for-test"
        self._version = "1.2.3"
        self._devId = "device_id_001"
        self._devPass = "password001"
        self._rd = renv_device.RenvDevice(self._devTypeId, self._devName, self._version, self._devUUID, self._devId, self._devPass)

    def test_givenNameIsEqualToDeviceInfoName(self):
        """
        """
        deviceInfo = self._rd.getDeviceInfo()
        self.assertEqual(self._devName+':'+self._version, deviceInfo['deviceName'])

    def test_givenIdIsEqualToDeviceInfoName(self):
        """
        """
        deviceInfo = self._rd.getDeviceInfo()
        self.assertEqual(self._devUUID, deviceInfo['deviceId'])



if __name__ == "__main__":
    unittest.main()
