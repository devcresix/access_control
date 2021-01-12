from gpiozero import DigitalInputDevice
from signal import pause
from smbus2 import SMBus
from mlx90614 import MLX90614
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def i2c(webController):
    try:
        bus = busio.I2C(board.SCL, board.SDA)
        return bus
    except:
        webController.errorDetected('code:I01')
        return - 1


def ads(webController):
    i2c = i2c(webController)
    if (i2c == -1):
        return - 1
    else:
        try:
            dev = ADS.ADS1015(i2c)
            return dev
        except:
            webController.errorDetected('code:A01')
            return - 1


def disSensor(webController):
    ads = ads(webController)
    if (ads == -1):
        return - 1
    else:
        try:
            dev = AnalogIn(ads, ADS.P0)
            return dev
        except:
            webController.errorDetected('code:S01')
            return - 1


def pot1(webController):
    ads = ads(webController)
    if (ads == -1):
        return - 1
    else:
        try:
            dev = AnalogIn(ads, ADS.P1)
            return dev
        except:
            webController.errorDetected('code:P01')
            return - 1


def pot2(webController):
    ads = ads(webController)
    if (ads == -1):
        return - 1
    else:
        try:
            dev = AnalogIn(ads, ADS.P2)
            return dev
        except:
            webController.errorDetected('code:P01')
            return - 1


def measureTemp(limit, webController):
    webController.measuringTemperature()
    sharpIR = disSensor(webController)

    if (sharpIR == -1):
        return (-1, -1)

    else:
        try:
            bus = SMBus(1)  # SMBus for Temperature Sensor
            # Temperature Sensor - I2c
            tempSensor = MLX90614(bus, address=0x5A)
            while True:
                if(sharpIR.value > 18000):
                    temperature = tempSensor.get_object_1()
                    bus.stop()
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
        sanitizerPIR = DigitalInputDevice(27)
        if(sanitizerPIR.wait_for_active(timeout=timeout)):
            return True
        else:
            return False
    except:
        webController.errorDetected('code: P01')
        return -1


def sanitizeTime(webController):
    try:
        sanitizeTimer = pot1(webController)
        value = sanitizeTimer.value
        timeInSeconds = value
        return timeInSeconds
    except:
        return -1


def doorTime(webController):
    try:
        doorTimer = pot2(webController)
        value = doorTimer.value
        timeInSeconds = value
        return timeInSeconds
    except:
        return -1
