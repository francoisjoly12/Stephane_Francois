import laser
import board
import digitalio
# import gaz_sensor.py
# import motor.py
# import servo.py
# import obstacle_sensor.py
import buzzer
# import sd_card

test = laser.laser_detector.detect()
if test == False:
    print(False)
else:
    print(True)

buz = buzzer.Buzzer.alert(1)
if buz == 1:
    print(1)
else:
    print(0)

