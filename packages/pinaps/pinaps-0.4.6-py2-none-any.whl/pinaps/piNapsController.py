import RPi.GPIO as GPIO
from enum import IntEnum

import sys
import serial
from SC16IS750 import SC16IS750 #Will be moving this to only be imported when needed. After testing pip instal SC16IS750

class PiNapsController:
    ##Direct control from PI or through I2C chip##
    class Control(IntEnum):
        NONE = 0
        PI = 1
        I2C = 2

    ##Pi to TGAT interface##
    class Interface(IntEnum):
        NONE = 0
        UART = 1
        I2C = 2
        
    ##Pi pins##
    class PI_PINS(IntEnum):
        POWER = 23
        TX = 14
        RX = 15
        SWITCH_1 = 4
        SWITCH_2 = 17

    ##I2C pins##
    class I2C_PINS(IntEnum):
        POWER = 4
        SWITCH_1 = 6
        SWITCH_2 = 7
        LED_RED = 1
        LED_GREEN = 2
        LED_BLUE = 3

    ##Baudrate values##
    class Baudrate(IntEnum):
        BAUD_1_2K = 1200
        BAUD_9_6K = 9600
        BAUD_57_6K = 57600

    ##TGAT operating modes##
    class OutputMode(IntEnum):
        NORMAL_OUTPUT_1_2K = 0
        NORMAL_OUTPUT_9_6K = 1
        RAW_OUTPUT_57_6K = 3
        FFT_OUTPUT_57_6K = 4

    ##Init interfaces and GPIO pins##
    def __init__(self):
        self._control = self.Control.PI
        self._interface = self.Interface.NONE
        self._UART = None
        self._I2C = None
        GPIO.setmode(GPIO.BCM)

    ##Set control from PI directly or through I2C##
    def setControl(self, selectedControl):
        if(selectedControl == self.Control.PI):
            GPIO.setup(self.PI_PINS.POWER, GPIO.OUT)
            GPIO.setup(self.PI_PINS.SWITCH_1, GPIO.OUT)
            GPIO.setup(self.PI_PINS.SWITCH_2, GPIO.OUT)
        if(selectedControl == self.Control.I2C):
            self._I2C = SC16IS750.SC16IS750()
            self._I2C.init(14745600)
            self._I2C.writeRegister(self._I2C.registers.IODIR, 0xFF)
        self._control = selectedControl

    ##Activate a chosen LED##
    def activateLED(self, selectedLED):
        if(self._control == self.Control.I2C):
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, selectedLED)
        else:
            print("Error: LED could not be activated. Make sure I2C configured properly.")

    ##Deactivate a chosen LED##
    def deactivateLED(self, selectedLED):
        if(self._control == self.Control.I2C):
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, selectedLED)
        else:
            print("Error: LED could not be activated. Make sure I2C configured properly.")

    ##Deactivate all LEDs##
    def deactivateAllLED(self):
        if(self._control == self.Control.I2C):
            self._I2C.writeRegister(self._I2C.registers.IOSTATE, 0xFF)
        else:
            print("Error: LED could not be activated. Make sure I2C configured properly.")

    ##Button Functions##
    ##def 

    ##Power to TGAT##
    def activateTGAT(self):
        ##Activate direct from PI##
        if(self._control == self.Control.PI):
            GPIO.output(self.PI_PINS.POWER, GPIO.HIGH)
        ##Activate through I2C##
        if(self._control == self.Control.I2C):
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.POWER)
        if(self._control == self.Control.NONE):
            print("Error: Can not activate EEG Sensor. Make sure Pinaps control configure first.")

    ##Power down TGAT## 
    def deactivateTGAT(self):
        ##Deactivate direct from PI##
        if(self._control == self.Control.PI):
            GPIO.output(self.PI_PINS.POWER, GPIO.LOW)
        ##Deactivate through I2C##
        if(self._control == self.Control.I2C):
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.POWER)
        if(self._control == self.Control.NONE):
            print("Error: Can not deactivate EEG Sensor. Make sure Pinaps control configure first.")

    ##Setup UART interface between Pi and TGAT##
    def setupUART(self):
        ##Define PI UART interface##
        self._interface = self.Interface.UART
        
        ##Switch to UART through I2C##
        if(self._control == self.Control.I2C):
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_1)
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_2)
            
        #Initalize Pi UART interface#
        self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)
        self.setMode(self.OutputMode.RAW_OUTPUT_57_6K)

    ##Deactivate UART interface between Pi and TGAT##
    def deactivateUART(self):
        ##Define no interface##
        self._interface = self.Interface.NONE
        
        ##Switch off direct from PI##
        if(self._control == self.Control.UART):
            GPIO.output(self.TGAT_UART_PIN, GPIO.LOW)
            
        ##Switch off through I2C##
        if(self._control == self.Control.I2C):
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_2)
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_1)
            
        #Close Pi UART interface if open#
        if(self._UART != None):
            self._UART.close()

    ##Setup I2C interface between Pi and TGAT##
    def setupI2C(self):
        if(self._control == self.Control.I2C):
            ##Define I2C as interface##
            self._interface = self.Interface.I2C
        
            ##Set I2C pin configuration to use I2C serial##
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_1)
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_2)
        
            #Do this here or elsewhere?
            #self._I2C.setBaudrate(9600)
        else:
            print("Error: Pinaps control not configured to I2C. Cannot use I2C interface if control is not configured for I2C.")

    def deactivateI2C(self):
        if(self._control == self.Control.I2C):
            ##Define no interface##
            self._interface = self.Interface.NONE
        
            ##Set I2C pin configuration to Off##
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_1)
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.SWITCH_2)
        else:
            print("Error: Pinaps control not configured to I2C. Cannot use I2C interface if control is not configured for I2C.")

    ##Check if data waiting from TGAT##
    def isWaiting(self):
        if(self._interface == self.Interface.UART):
            if(self._UART.inWaiting()):
                return True
        if(self._interface == self.Interface.I2C):
            if(self._I2C.dataWaiting()):
                return True
        if(self._interface == self.Interface.NONE):
            print("Error: No interface setup. Make sure a chosen interface has been setup.")
        return False

    ##Check how much data is waiting from TGAT##
    def dataWaiting(self):
        if(self._interface == self.Interface.UART):
            return self._UART.inWaiting()
        if(self._interface == self.Interface.I2C):
            return self._I2C.dataWaiting()
        if(self._interface == self.Interface.NONE):
            print("Error: No interface setup. Make sure a chosen interface has been setup.")
        return 0

    ##Read byte of data waiting from TGAT##
    def readTGAT(self):
        if(self._interface == self.Interface.UART):
            return self._decodeByte(self._UART.read())
        if(self._interface == self.Interface.I2C):
            return self._I2C.readRegister(self._I2C.registers.RHR)
        if(self._interface == self.Interface.NONE):
            print("Error: No interface setup. Make sure a chosen interface has been setup.")

    ##Set the TGAT operating mode##
    def setMode(self, output_mode):
        #Set TGAT mode using UART interface#
        if(self._interface == self.Interface.UART):
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_1_2K):
                self._UART.write([0x01])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_1_2K)
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_9_6K):
                self._UART.write([0x00])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_9_6K)
            if(output_mode == self.OutputMode.RAW_OUTPUT_57_6K):
                self._UART.write([0x02])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)
            if(output_mode == self.OutputMode.FFT_OUTPUT_57_6K):
                self._UART.write([0x03])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)

        #Set TGAT mode using I2C interface#
        if(self._interface == self.Interface.I2C):
            self._I2C.writeRegister(self._I2C.registers.LCR, 0x03) #UART Attributes - no parity, 8 databits, 1 stop bit
            self._I2C.writeRegister(self._I2C.registers.FCR, 0x07) #Fifo control - Enable + Reset RX + TX
            #sc.writeRegister(sc.registers.THR, 0x02) #
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_1_2K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x01)
                self._I2C.setBaudrate(self.Baudrate.BAUD_1_2K)
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_9_6K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x00)
                self._I2C.setBaudrate(self.Baudrate.BAUD_9_6K)
            if(output_mode == self.OutputMode.RAW_OUTPUT_57_6K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x2)
                self._I2C.setBaudrate(self.Baudrate.BAUD_57_6K)
            if(output_mode == self.OutputMode.FFT_OUTPUT_57_6K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x3)
                self._I2C.setBaudrate(self.Baudrate.BAUD_57_6K)

        if(self._interface == self.Interface.NONE):
            print("Error: No interface setup. Make sure a chosen interface has been setup.")
            
    ##Decode data recieved over UART##
    def _decodeByte(self, byte):
        #return byte.decode('utf-8')
        return int((str(byte)).encode('hex'), 16)
