from piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

def batteryCallback(battery):
    print("Battery value: %d" % battery)

def qualityCallback(quality):
    print("Quality value: %d" % quality)

def attentionCallback(attention):
    print("Attention value: %d" % attention)

def meditationCallback(meditation):
    print("Meditation value: %d" % meditation)

def rawSignalCallback(rawSignal):
    print("Raw signal value: %d" % rawSignal)

def eegSignalCallback(eegSignal):
    print("Delta value: %d" % eegSignal.delta)
    print("Theta value: %d" % eegSignal.theta)
    print("Low alpha value: %d" % eegSignal.lAlpha)
    print("High alpha value: %d" % eegSignal.hAlpha)
    print("Low beta value: %d" % eegSignal.lBeta)
    print("High beta value: %d" % eegSignal.hBeta)
    print("Low Gamma value: %d" % eegSignal.lGamma)
    print("Medium gamma value: %d" % eegSignal.mGamma)

def rawSignalCallback(rawSignal):
    print("Raw value: %d" % rawSignal)

controller = PiNapsController(PiNapsController.I2C_ADDRESSES.A0x9A)
controller.setControl(controller.Control.I2C)
controller.setupInterface(controller.Interface.UART)
#controller.activateTGAT()

#controller.setupI2C()
#controller.setupUART()
#controller.activateTGAT()
#controller.setMode(controller.OutputMode.RAW_OUTPUT_57_6K)
controller.setMode(controller.OutputMode.NORMAL_OUTPUT_9_6K)
#controller.setMode(controller.OutputMode.NORMAL_OUTPUT_9_6K)

parser = BlinoParser()
parser.batteryCallback = batteryCallback
parser.qualityCallback = qualityCallback
parser.attentionCallback = attentionCallback
parser.meditationCallback = meditationCallback
parser.rawSignalCallback = rawSignalCallback
parser.eegSignalCallback = eegSignalCallback
parser.rawSignalCallback = rawSignalCallback


while(1):
    while(controller.dataWaiting() > 0):
        data = controller.readTGAT()
        parser.parseByte(data)


