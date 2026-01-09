import time
import board
from pwmio import PWMOut
import servo
from adafruit_debouncer import Debouncer
from digitalio import DigitalInOut, Direction, Pull
import adafruit_tcs34725


pwm1 = PWMOut(board.D6 ,frequency =50)
Servo1 = servo.Servo(pwm1, min_pulse =320, max_pulse =2720)
pwm2 = PWMOut(board.D5 ,frequency =50)
Servo2 = servo.Servo(pwm2, min_pulse =325, max_pulse =2725)

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

sensor.integration_time = 350
sensor.gain = 16

switch = DigitalInOut(board.D10)

switch.direction = Direction.INPUT
switch.pull = Pull.UP
Switch = Debouncer(switch)

a = 0
#States
MMOPHALEN = 1
MMNAARSENSOR = 2

KLEURMETEN = 3
DRAAIGEEL = 4
DRAAIORANJE = 5
DRAAIROOD = 6
DRAAIGROEN = 7
DRAAIBRUIN = 8
DRAAIBLAUW = 9

MMNAARDROPPER = 10
MMDROPPEN = 11
MMTERUGNAAROPHALEN = 12
STOP = 13






#Color States
Geel = 1
Oranje = 2
Rood = 3
Groen = 4
Bruin = 5
Blauw = 6

#Snelheid van de servo's
i1 = 6
i2 = 6

#KleurHoeken
HoekGeel = 64
HoekOranje = 42
HoekRood = 20
HoekGroen = 87
HoekBruin = 108
HoekBlauw = 135

#Servo 1 Hoeken
MMOphalenHoek = 160
MMMetenHoek = 80
MMDroppenHoek = 33



#State Functions

red = (40,9,6)
orange = (39,11,4)
yellow = (30,18,3)
green = (11,27,8)
blue = (3,15,30)
brown = (25,12,8)
none = (17,14,11)



Angle1 = 20
Angle2 = 20
State = MMTERUGNAAROPHALEN

while True:
    Switch.update()
    if Switch.fell:
        Start = time.monotonic()
        while True:
            Switch.update()
            if Switch.fell:
                if (time.monotonic()-Start) > 2:
                    State = STOP

            if State == MMOPHALEN:
                Angle1 = MMOphalenHoek
                Servo1.angle = Angle1
                print('MMOphalen')
                State = MMNAARSENSOR

            elif State == MMNAARSENSOR:
                Angle1 -= i1
                Servo1.angle = Angle1
                if Angle1 <= MMMetenHoek:
                    print('MMnaarSensor')
                    State = KLEURMETEN

            elif State == KLEURMETEN:
                color_rgb = sensor.color_rgb_bytes
                DtoRED = (((color_rgb[0]-red[0])**2) +
                ((color_rgb[1]-red[1])**2) +
                ((color_rgb[2]-red[2])**2))**0.5
                DtoORANGE = (((color_rgb[0]-orange[0])**2) +
                ((color_rgb[1]-orange[1])**2) +
                ((color_rgb[2]-orange[2])**2))**0.5
                DtoYELLOW = (((color_rgb[0]-yellow[0])**2) +
                ((color_rgb[1]-yellow[1])**2) +
                ((color_rgb[2]-yellow[2])**2))**0.5
                DtoGREEN = (((color_rgb[0]-green[0])**2) +
                ((color_rgb[1]-green[1])**2) +
                ((color_rgb[2]-green[2])**2))**0.5
                DtoBLUE = (((color_rgb[0]-blue[0])**2) +
                ((color_rgb[1]-blue[1])**2) +
                ((color_rgb[2]-blue[2])**2))**0.5
                DtoBROWN = (((color_rgb[0]-brown[0])**2) +
                ((color_rgb[1]-brown[1])**2) +
                ((color_rgb[2]-brown[2])**2))**0.5
                DtoNONE = (((color_rgb[0]-none[0])**2) +
                ((color_rgb[1]-none[1])**2) +
                ((color_rgb[2]-none[2])**2))**0.5

                closest = min(DtoRED, DtoORANGE, DtoYELLOW, DtoGREEN, DtoBLUE, DtoBROWN,DtoNONE)
                if closest == DtoRED:
                    colour = "rood"
                    State = DRAAIROOD
                    print(color_rgb)
                elif closest == DtoORANGE:
                    colour = "oranje"
                    State = DRAAIORANJE
                    print(color_rgb)
                elif closest == DtoYELLOW:
                    colour = "geel"
                    State = DRAAIGEEL
                    print(color_rgb)
                elif closest == DtoGREEN:
                    colour = "groen"
                    State = DRAAIGROEN
                    print(color_rgb)
                elif closest == DtoBLUE:
                    colour = "blauw"
                    State = DRAAIBLAUW
                    print(color_rgb)
                elif closest == DtoBROWN:
                    colour = "bruin"
                    State = DRAAIBRUIN
                    print(color_rgb)
                elif closest == DtoNONE:
                    colour = "GeenKleur"
                    if a >= 20:
                        State = STOP
                    else:
                        State = MMTERUGNAAROPHALEN

            elif State == DRAAIBLAUW:
                if Angle2 < (HoekBlauw+3) and Angle2 > (HoekBlauw - 3):
                    print('DraaiBlauw')
                    State = MMNAARDROPPER
                elif Angle2 < HoekBlauw:
                    Angle2 += i2
                    Servo2.angle = Angle2
                elif Angle2 > HoekBlauw:
                    Angle2 -= i2
                    Servo2.angle = Angle2


            elif State == DRAAIGEEL:
                if Angle2 < (HoekGeel+3) and Angle2 > (HoekGeel - 3):
                    print('DraaiGeel')
                    State = MMNAARDROPPER
                elif Angle2 < HoekGeel:
                    Angle2 += i2
                    Servo2.angle = Angle2
                elif Angle2 > HoekGeel:
                    Angle2 -= i2
                    Servo2.angle = Angle2


            elif State == DRAAIROOD:
                if Angle2 < (HoekRood+3) and Angle2 > (HoekRood - 3):
                    print('DraaiRood')
                    State = MMNAARDROPPER
                elif Angle2 < HoekRood:
                    Angle2 += i2
                    Servo2.angle = Angle2
                elif Angle2 > HoekRood:
                    Angle2 -= i2
                    Servo2.angle = Angle2


            elif State == DRAAIBRUIN:
                if Angle2 < (HoekBruin+3) and Angle2 > (HoekBruin - 3):
                    print('DraaiBruin')
                    State = MMNAARDROPPER
                elif Angle2 < HoekBruin:
                    Angle2 += i2
                    Servo2.angle = Angle2
                elif Angle2 > HoekBruin:
                    Angle2 -= i2
                    Servo2.angle = Angle2


            elif State == DRAAIORANJE:
                if Angle2 < (HoekOranje+3) and Angle2 > (HoekOranje - 3):
                    print('DraaiOranje')
                    State = MMNAARDROPPER
                elif Angle2 < HoekOranje:
                    Angle2 += i2
                    Servo2.angle = Angle2
                elif Angle2 > HoekOranje:
                    Angle2 -= i2
                    Servo2.angle = Angle2


            elif State == DRAAIGROEN:
                if Angle2 < (HoekGroen+3) and Angle2 > (HoekGroen - 3):
                    print('DraaiGroen')
                    State = MMNAARDROPPER
                elif Angle2 < HoekGroen:
                    Angle2 += i2
                    Servo2.angle = Angle2
                elif Angle2 > HoekGroen:
                    Angle2 -= i2
                    Servo2.angle = Angle2


            elif State == MMNAARDROPPER:
                Angle1 -= i1
                Servo1.angle = Angle1
                time.sleep(0.01)
                if Angle1 < MMDroppenHoek:
                    State = MMDROPPEN

            elif State == MMDROPPEN:
                Angle1 = MMDroppenHoek
                Servo1.angle = Angle1
                time.sleep(0.1)
                print('MMDroppen')
                State = MMTERUGNAAROPHALEN
                a += 1

            elif State == MMTERUGNAAROPHALEN:
                Angle1 += i1
                Servo1.angle = Angle1
                if Angle1 >= MMOphalenHoek:
                    State = MMOPHALEN
                    print('MMterugnaarOphalen')

            elif State == STOP:
                Eind = time.monotonic() - Start
                print(Eind)
                break

