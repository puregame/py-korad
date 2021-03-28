
import time
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from .communication import KoradUdpComm

class kel103(object):

    def __init__(self, local_address, device_address, port):
        self.device = KoradUdpComm(local_address, device_address, port)
        self.device.connect()

    def __init__(self, device):
        self.device = device
        self.device.connect()

    def device_info(self):
        return self.device.send_receive('*IDN?')
    
    def check_device(self):
        if 'KEL103' in self.device_info():
            return True
        else:
            return False

    def get_generic_boolean(self, setting_name):
        s = self.device.send_receive(':{}?'.format(setting_name))
        if 'OFF' in s:
            return False
        if 'ON' in s:
            return True

    def set_generic_boolean(self, setting_name, state):
        self.device.send(':{0} {1:d}'.format(setting_name, state))
        if self.get_generic_boolean(setting_name) != state:
            raise ValueError('Caution: {} not set'.format(setting_name))

    def get_output(self):
        return self.get_generic_boolean('INP')

    def set_output(self, state):
        self.set_generic_boolean('INP', state)

    def get_comp(self):
        return self.get_generic_boolean('SYST:COMP')

    def set_comp(self, state):
        self.set_generic_boolean('SYST:COMP', state)

    def shutdown(self):
        ''' Turn off output and end communications '''
        self.setOutput(False)
        self.end_comm()
        
    def end_comm(self):
        self.device.close()

    def get_func(self):
        s = self.device.send_receive(':FUNC?')
        return s.strip('\n')

    def set_func(self, func_type):
        ''' func options: 
        CC = Constant Current
        CV = Constant Voltage
        CR = Constant Resistance
        CW = Constant Wattage
        SHORt = ???'''
        self.device.send(':FUNC {}'.format(func_type))
        if self.getFunc() != func_type:
            raise ValueError('Caution: {} not set properly'.format('FUNC'))

    def set_constant_current(self):
        self.set_func('CC')

    def set_constant_power(self):
        self.set_func('CW')
        
    def set_constant_resistance(self):
        self.set_func('CR')

#### COMPLETED AND TESTED ABOVE THIS LINE

    def get_generic_float(self, setting_name, units=''):
        return float(self.device.udpSendRec(':{}?'.format(setting_name)).strip('{}\n'.format(units)))

    def measure_voltage(self):
        return self.get_generic_float('MEAS:VOLT', 'V')

    def measure_power(self):
        return self.get_generic_float('MEAS:POW', 'W')

    def measure_current(self):
        return self.get_generic_float('MEAS:CUR', 'A')

    def measure_all_params(self):
        return {"voltage": self.measure_voltage(), "current": self.measure_current(), "power": self.measure_power()}

    def set_generic_gloat(self, setting_name, value, units, precsision=3):
        # tod0: test 3 decimal places!
        s = self.device.send(':{0} {1:.{prec}f}{2}'.format(setting_name, value, units, prec=precision))
        if self.get_generic_float(setting_name, units) != value:
            raise ValueError('{} set incorectly on the device'.format(setting_name))
        

    def set_current(self, current):
        self.set_generic_gloat("CURR", current, "A")

    def get_currentSetpoint(self):
        return self.get_generic_float('CURR')
    
    def set_power(self, power):
        self.set_generic_gloat("POW", power, "A")

    def get_power_setpoint(self):
        return self.get_generic_float('POW')

    def set_voltage(self, voltage):
        self.set_generic_gloat("VOLT", voltage, "A")

    def get_voltage_setpoint(self):
        return self.get_generic_float('VOLT')

    def set_current_max(self, current):
        raise NotImplementedError("Setting max values not yet implemented")

    def set_voltage_max(self, voltage):
        raise NotImplementedError("Setting max values not yet implemented")
        
    def set_power_max(self, Power):
        raise NotImplementedError("Setting max values not yet implemented")

    def set_battery_data(self, setting_id, max_current, set_current, voltage_cutoff, capacty_cutoff, time_cutoff):
        # todo: check if settings are all proper??
        self.device.send(':BATT {0}, {1}A, {2}A, {3}V, {4}AH, {5}M'.format(setting_id, max_current, 
                                                                        set_current, voltage_cutoff, 
                                                                        capacity_cutoff, time_cutoff))

        self.device.send(':RCL:BATT {}'.format(setting_id))
        print(self.device.udpSendRec(':RCL:BATT?'))
        # todo: confirm settings worked with feedback!

    def get_battery_time(self):
        return self.get_generic_float('BAT:TIM?', "M")

    def get_battery_capacity(self):
        return self.get_generic_float('BAT:CAP?', "AH")

    def set_keyboard_lock(self, locked):
        self.set_generic_boolean('SYST:LOCK', locked)

# to do:
"""

- BATT command
:BATT 1,30A,25A,2.6V,72AH,500M
    ID,MAX CURRENT, SET CURRENT, CUTOFF VOLTS, CUTOFF CAPACITY, CUTOFF TIMEl
:RCL:BATT 1
:RCL:BATT?

Goal: Use battery function on KEL to do battery testing, less sketchy because it will automatically shut down at proper voltage

- Write tests that can be run on the machine to check if the library works!
"""