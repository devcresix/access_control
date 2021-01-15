from gpiozero import DigitalInputDevice
from signal import pause
from smbus2 import SMBus
from mlx90614 import MLX90614
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from numpy import interp


def i2c(webController):
    try:
        bus = busio.I2C(board.SCL, board.SDA)
        return bus
    except:
        webController.errorDetected('code:I01')
        return - 1


def ads(webController):
    i2cV = i2c(webController)
    if (i2cV == -1):
        return - 1
    else:
        try:
            dev = ADS.ADS1015(i2cV)
            return dev
        except:
            webController.errorDetected('code:A01')
            return - 1


def disSensor(webController):
    adsV = ads(webController)
    if (adsV == -1):
        return - 1
    else:
        try:
            dev = AnalogIn(adsV, ADS.P0)
            return dev.value
        except:
            webController.errorDetected('code:S01')
            return - 1


def pot1(webController):
    adsV = ads(webController)
    if (adsV == -1):
        return - 1
    else:
        try:
            dev = AnalogIn(adsV, ADS.P1)
            return dev.value
        except:
            webController.errorDetected('code:P01')
            return - 1


def pot2(webController):
    adsV = ads(webController)
    if (adsV == -1):
        return - 1
    else:
        try:
            dev = AnalogIn(adsV, ADS.P2)
            return dev.value
        except:
            webController.errorDetected('code:P01')
            return - 1


def measureTemp(limit, webController):

    try:
        bus = SMBus(1)  # SMBus for Temperature Sensor
        # Temperature Sensor - I2c
        tempSensor = MLX90614(bus, address=0x5A)
        while True:
            sharpIR = disSensor(webController)
            if (sharpIR == -1):
                return (-1, -1)
                break
            elif (sharpIR > 18000):
                webController.measuringTemperature()
                temperature = tempSensor.get_object_1()
                # bus.stop()
                if(temperature > limit):
                    webController.highTemperature()
                    return (temperature, False)
                    break
                else:
                    return (temperature, True)
                    break
    except:
        webController.errorDetected('code:T01')
        return (-1, -1)


def detectHand(timeout, webController):
    try:
        sanitizerPIR = DigitalInputDevice(8)
        value = sanitizerPIR.value
        if (value == 1):
            return True
        elif(sanitizerPIR.wait_for_active(timeout=timeout)):
            return True
        else:
            return False
    except:
        webController.errorDetected('code: P01')
        return -1


def sanitizeTime(webController):
    try:
        sanitizeTimer = pot1(webController)
        if (sanitizeTimer == -1):
            return -1
        timeInSeconds = interp(sanitizeTimer, [0, 26368], [0, 5])
        return round(timeInSeconds, 1)
    except:
        return -1


def doorTime(webController):
    try:
        doorTimer = pot2(webController)
        if (doorTimer == -1):
            return -1
        timeInSeconds = interp(doorTimer, [0, 26368], [0, 10])
        return round(timeInSeconds, 1)
    except:
        return -1
