ARDUINO_PORT_NAME = '/dev/ttyACM0'
LIDAR_PORT_NAME = '/dev/ttyUSB0'
CENTER = 0
RIGHT = 60
LEFT = 300
MIN_DISTANCE = 200
MAX_DISTANCE = 400
QUALITY = 13
MAX_BUF_MEAS = 500
NUMBER_MEASURE = 100

FREQ_COMMANDS = 0.1

#OpenCv configuration

#dimensioni schermo
widthScreen=170
heightScreen=110
sensitivity = 10
central_zone = 0.33

#MPU configuration
tCycle = 0.05 #s - original = 0.2
nCalibrationCycle=200 #numero per calibrazione
nConvertX=775.23
nConvertY=512.79
nConvertZ=14.6

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
Device_Address = 0x68