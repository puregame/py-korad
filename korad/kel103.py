import socket
import time
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class koradUdpComm(object):

    def __init__(self, localAddress, deviceAddress, port):
        self.clientAddress = (localAddress, port)
        self.deviceAddress = (deviceAddress, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        self.sock.bind(self.clientAddress)
        self.sock.settimeout(1.0)

    def close(self):
        self.sock.close()

    def udpSendRecv(self, message):

        # build the message
        messageb = bytearray()
        messageb.extend(map(ord, message))
        messageb.append(0x0a)

        startTime = time.time()
        while 1:
            sent = self.sock.sendto(messageb , self.deviceAddress)
            self.sock.settimeout(1.0) 
            data, server = self.sock.recvfrom(1024)
            if len(data) > 0:
                return data.decode('utf-8')
            
            if time.time() - startTime > 3:
                print ("UDP timeout")
                return " "

    def udpSend(self, message):
        # build the message
        messageb = bytearray()
        messageb.extend(map(ord, message))
        messageb.append(0x0a)

        sent = self.sock.sendto(messageb , self.deviceAddress)

class kel103(object):

    def __init__(self, localAddress, deviceAddress, port):
        self.device = koradUdpComm(localAddress, deviceAddress, port)
        self.device.connect()

    def deviceInfo(self):
        return self.device.udpSendRecv('*IDN?')
    
    def checkDevice(self):
        if 'KEL103' in self.deviceInfo():
            return True
        else:
            return False

    def measureSetCurrent(self):
        s = self.device.udpSendRecv(':CURR?')
        return float(s.strip('A\n'))

    def setCurrent(self, current):
        s = self.device.udpSend(':CURR ' + str(current) + 'A')
        if self.measureSetCurrent() != current:
            raise ValueError('Current set incorectly on the device')

    def getGenericBoolean(self, settingName):
        s = self.device.udpSendRecv(':{}?'.format(settingName))
        if 'OFF' in s:
            return False
        if 'ON' in s:
            return True

    def setGenericBoolean(self, settingName, state):
        self.device.udpSend(':{0} {1:d}'.format(settingName, state))
        if self.getGenericBoolean(settingName) != state:
            raise ValueError('Caution: {} not set'.format(settingName))

    def getOutput(self):
        return self.getGenericBoolean('INP')

    def setOutput(self, state):
        self.setGenericBoolean('INP', state)

    def getComp(self):
        return self.getGenericBoolean('SYST:COMP')

    def setComp(self, state):
        self.setGenericBoolean('SYST:COMP', state)

    def shutdown(self):
        ''' Turn off output and end communications '''
        self.setOutput(False)
        self.endComm()
        
    def endComm(self):
        self.device.close()

    def getFunc(self):
        s = self.device.udpSendRecv(':FUNC?')
        return s.strip('\n')

    def setFunc(self, func_type):
        ''' func options: 
        CC = Constant Current
        CV = Constant Voltage
        CR = Constant Resistance
        CW = Constant Wattage
        SHORt = ???'''
        self.device.udpSend(':FUNC {}'.format(func_type))
        if self.getFunc() != func_type:
            raise ValueError('Caution: {} not set properly'.format('FUNC'))

    def setConstantCurrent(self):
        self.setFunc('CC')

    def setConstantPower(self):
        self.setFunc('CW')
        
    def setConstantResistance(self):
        self.setFunc('CR')

#### COMPLETED AND TESTED ABOVE THIS LINE

    def getGenericFloat(self, settingName, units):
        return float(self.device.udpSendRec(':{}?'.format(settingName)).strip('V\n')))

    def measureVoltage(self):
        return self.getGenericFloat('MEAS:VOLT', 'V')

    def measurePower(self):
        return self.getGenericFloat('MEAS:POW', 'W')

    def measureCurrent(self):
        return self.getGenericFloat('MEAS:CUR', 'A')

    def measureAllParams(self):
        return {"voltage": self.measureVoltage(), "current": self.measureCurrent(), "power": self.measurePower()}

    def setGenericFloat(self, settingName, value, units, precsision=3):
        # tod0: test 3 decimal places!
        s = self.device.udpSend(':{0} {1:.{prec}f}{2}'.format(settingName, value, units, prec=precision))
        if self.getGenericFloat(settingName, units) != value:
            raise ValueError('{} set incorectly on the device'.format(settingName))
        

    def setCurrent(self, current):
        self.setGenericFloat("CURR", current, "A")

    def getCurrentSetpoint(self):
        raise NotImplementedError("getting setpoints not yet implemented")

    
    def setPower(self, power):
        self.setGenericFloat("POW", power, "A")

    def getPowerSetpoint(self):
        raise NotImplementedError("getting setpoints not yet implemented")

    def setVoltage(self, voltage):
        self.setGenericFloat("VOLT", voltage, "A")

    def getVoltageSetpoint(self):
        raise NotImplementedError("getting setpoints not yet implemented")

    def setCurrentMax(self, current):
        raise NotImplementedError("Setting max values not yet implemented")

    def setVoltageMax(self, voltage):
        raise NotImplementedError("Setting max values not yet implemented")
        
    def setPowerMax(self, Power):
        raise NotImplementedError("Setting max values not yet implemented")

    def setBatteryData(self, setting_id, max_current, set_current, voltage_cutoff, capacty_cutoff, time_cutoff):
        # todo: check if settings are all proper??
        self.device.udpSend(':BATT {0}, {1}A, {2}A, {3}V, {4}AH, {5}M'.format(setting_id, max_current, 
                                                                        set_current, voltage_cutoff, 
                                                                        capacity_cutoff, time_cutoff))

        self.device.udpSend(':RCL:BATT {}'.format(setting_id))
        print(self.device.udpSendRec(':RCL:BATT?'))
        # todo: confirm settings worked with feedback!

    def getBatteryTime(self):
        return self.getGenericFloat('BAT:TIM?')

    def getBatteryCapacity(self):
        return self.getGenericFloat('BAT:CAP?')

    def setKeyboardLock(self, locked):
        self.setGenericBoolean('SYST:LOCK', locked)

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