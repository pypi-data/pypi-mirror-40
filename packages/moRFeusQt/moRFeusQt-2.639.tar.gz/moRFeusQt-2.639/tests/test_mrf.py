import hid
import unittest
import os, sys
from moRFeusQt import mrf
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMRFs(unittest.TestCase):

    @classmethod
    def mockdevice(cls):
        # hard code the opening of the morfeus device and return
        td = hid.device()
        td.open(mrf.MoRFeus.vendorID, mrf.MoRFeus.productID)
        td.set_nonblocking(0)
        return td

    def test_find(self):
        # If the device isn't found, test do not continue
        cond = mrf.MoRFeus.find()
        print(cond, "Devices found")
        self.assertTrue((cond >= 1))

    def test_initdevice(self):
        # init two test devices, one from morfeus class and another from mockdevice
        devicecount = mrf.MoRFeus.find()
        devices = []
        testdevices = []
        for i in range(0, devicecount):
            devices.append(mrf.MoRFeus.initdevice(index=i))
            testdevices.append(devices[i])
            # testdevices.append(self.mockdevice())
            # Check types
            self.assertEqual(type(devices[i]), type(testdevices[i]))
            # Check if 'td1' is and instance of type 'td2'(hard opened hid.device)
            self.assertIsInstance(devices[i], type(testdevices[i]))
            # Close the devices
            devices[i].close()


if __name__ == "__main__":
    unittest.main()
