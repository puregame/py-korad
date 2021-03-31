from korad.kel103 import Kel103
import time
import unittest

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        # NOTE: change the 
        self.kel = Kel103("10.11.6.3", "10.11.0.200", 18190)
        # self.kel = Kel103("10.11.1.16", "10.11.0.200", 18190)

    def test_device_info(self):
        s = self.kel.device_info()
        self.assertIn("KORAD-KEL103", s)
        # check device info

    def test_func_mode(self):
        # set and check each func mode
        self.kel.set_func("CC")
        self.assertEqual("CC", self.kel.get_func())
        self.kel.set_func("CV")
        self.assertEqual("CV", self.kel.get_func())
        self.kel.set_func("CR")
        self.assertEqual("CR", self.kel.get_func())
        self.kel.set_func("CW")
        self.assertEqual("CW", self.kel.get_func())

        # set current, voltage, power and check that func changes
        self.kel.set_current(1)
        self.assertEqual("CC", self.kel.get_func())
        self.kel.set_voltage(1)
        self.assertEqual("CV", self.kel.get_func())
        self.kel.set_power(3)
        self.assertEqual("CW", self.kel.get_func())

    def test_setting_current(self):
        values_to_test = [0.1, 0.5, 1, 2,5,10,10.5,20,30,29.999]
        for v in values_to_test:
            self.kel.set_current(v)
            self.assertEqual(self.kel.get_current_setpoint(), v)
            
    def test_setting_voltage(self):
        values_to_test = [0.1, 0.5, 1, 2,5,10,10.5,20,30,99.999]
        for v in values_to_test:
            self.kel.set_voltage(v)
            self.assertEqual(self.kel.get_voltage_setpoint(), v)
            
    def test_setting_power(self):
        values_to_test = [0.1, 0.5, 1, 2,5,10,10.5,20,30,129,200,299.99,300]
        for v in values_to_test:
            self.kel.set_power(v)
            self.assertEqual(self.kel.get_power_setpoint(), v)

    def test_output_state_setting(self):
        # ensure setting is current and low current setting before turning output on
        self.kel.set_current(0.1)
        print("test current setting")
        self.kel.set_output(True)
        self.assertEqual(self.kel.get_output(), True)
        self.kel.set_output(False)
        self.assertEqual(self.kel.get_output(), False)

    def test_comp_setting(self):
        self.kel.set_comp(False)
        self.assertEqual(self.kel.get_comp(), False)
        self.kel.set_comp(True)
        self.assertEqual(self.kel.get_comp(), True)
        self.kel.set_comp(False)
        self.assertEqual(self.kel.get_comp(), False)

    def test_measure(self):
        # NO way to check if the values are correct.
        # For now will just print values and assume user double checks that measurements are correct
        self.kel.set_current(0.1)
        # set a low current and turn output on/off

        v = self.kel.measure_voltage()
        c = self.kel.measure_current()
        p = self.kel.measure_power()
        self.assertIsInstance(v, float)
        self.assertIsInstance(c, float)
        self.assertIsInstance(p, float)
        print("Values with output off: {}V, {}A, {}W".format(v,c,p))
        self.kel.set_output(True)
        time.sleep(0.5)
        v = self.kel.measure_voltage()
        c = self.kel.measure_current()
        p = self.kel.measure_power()
        print("Values with output on: {}V, {}A, {}W".format(v,c,p))

    def test_keyboard_lock(self):
        self.kel.set_keyboard_lock(True)
        self.assertEqual(self.kel.get_keyboard_lock(), True)
        self.kel.set_keyboard_lock(False)
        self.assertEqual(self.kel.get_keyboard_lock(), False)

    def tearDown(self):
        self.kel.shutdown()

# check setting and getting battery data, time, capacity

if __name__ == '__main__':
    print("WARNING: this script will turn on the input of the KEL device at CC mode 0.1 amps!\
        Ensure this will not damage any attached equipment!")
    input("Press Enter to continue...")
    unittest.main()