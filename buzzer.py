import board
import digitalio
import analogio
import pwmio
import time


buzzer = pwmio.PWMOut(board.IO10, variable_frequency=True, duty_cycle=2**15)

#timer pour fréqence des beeps
time3 = time.monotonic()

#fréquence pour une note F4
buzzer.frequency = 349

#pour alterner d'état et faire un beep au 0.5s
etat = 0

#le trigger pour démrrer le buzzer  *******DOIT ETRE A 1 POUR BUZZER******
alarme = 1




while True:
    if alarme == 1:
        if(time.monotonic() - time3 > 0.5):
            time3 = time.monotonic()
            if etat == 0:
                buzzer.duty_cycle = not buzzer.duty_cycle
                etat = 1
            else:
                buzzer.duty_cycle = duty_cycle=2**15
                etat = 0
    else:
        buzzer.duty_cycle = not buzzer.duty_cycle
        
    