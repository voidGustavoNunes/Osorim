#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Project#001 V1.0
#
# github.com/hnralmeida/osorim/project01
#

import RPi.GPIO as g
import serial
from time import sleep
import sys

g.setmode(g.BOARD)

# Iniciando Sensor UltraSonico
echo = 15
trig = 16

g.setup(trig, g.OUT)
g.setup(echo, g.IN)

# Iniciando Motores
ena = 12
enb = 32
in1 = 29
in2 = 31
in3 = 35
in4 = 37
serialPort = 'dev/ttyAMA0/'

g.setup(in1, g.OUT)
g.setup(in2, g.OUT)
g.setup(in3, g.OUT)
g.setup(in4, g.OUT)

g.setup(ena, g.OUT)
g.setup(enb, g.OUT)

g.output(in1, g.HIGH)
g.output(in2, g.LOW)
g.output(in3, g.HIGH)
g.output(in4, g.LOW)

m1 = g.PWM(ena, 1000)
m2 = g.PWM(enb, 1000)

m1.start(25)
m2.start(25)

sleep(1)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
g.setup(11,g.OUT)
servo1 = g.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
servo1.ChangeDutyCycle(7)

# funcao para garantir a leitura correta da distancia
def distFix(dist):
    dist.sort()
    return dist[2]

# funcao que retorna a distancia medida pelo sensor ultrassonico
def distControl():
    init_t = 0
    end_t = 0
    
    g.output(trig,g.LOW)
    time.sleep(0.01)
    g.output(trig, g.HIGH)
    time.sleep(0.01)
    g.output(trig,g.LOW)

    while g.input(echo) == 0 :
        init_t = time.time()

    while g.input(echo) == 1 :
        end_t = time.time()

    tempo = end_t - init_t
    dist = (tempo * 17150)    ## velocidade = 34300 cm/s
                                ## ida e volta
    return dist

# funcao que normaliza leituras de distancia do sensor ultrassonico
def retDist():
    vDist = [ ]
    for i in range(1,6) :
        vDist.append( distControl() )
        
    d = distFix(vDist)

    return d

# recebe um parametro que contra o motor
# aceita os comandos:
# r (run), s (stop)
# f (foward), b (backward)
# l (low), m (medium), h (high)
def motor1(x):
    if x=='r':
        if(temp1==1):
            g.output(in1,g.HIGH)
            g.output(in2,g.LOW)
            print("Motor 2 turned forward")
        else:
            g.output(in1,g.LOW)
            g.output(in2,g.HIGH)
            print("Motor 2 turned backward")

    elif x=='s':
        print("Motor 2 has stopped")
        g.output(in1,g.LOW)
        g.output(in2,g.LOW)

    elif x=='f':
        print("Motor 2 turned forward")
        g.output(in1,g.HIGH)
        g.output(in2,g.LOW)
        temp1=1

    elif x=='b':
        print("Motor 2 turned backward")
        g.output(in1,g.LOW)
        g.output(in2,g.HIGH)
        temp1=0

    elif x=='l':
        print("Motor 1 is in low speed now")
        m1.ChangeDutyCycle(25)

    elif x=='m':
        print("Motor 1 is in medium speed now")
        m1.ChangeDutyCycle(50)

    elif x=='h':
        print("Motor 1 is in high speed now")
        m1.ChangeDutyCycle(100)
    
    elif x=='e':
        g.cleanup()
        print("GPIO Clean up")
        exit()
    
    else:
        print("<<<  wrong entry  >>>")
        print("please enter ta valid command to continue.....")

# recebe um parametro que contra o motor
# aceita os comandos:
# r (run), s (stop)
# f (foward), b (backward)
# l (low), m (medium), h (high)
def motor2(x):
    if x=='r':
        if(temp2==1):
            g.output(in3,g.HIGH)
            g.output(in4,g.LOW)
            print("Motor 2 turned forward")
        else:
            g.output(in3,g.LOW)
            g.output(in4,g.HIGH)
            print("Motor 2 turned backward")

    elif x=='s':
        print("Motor 2 has stopped")
        g.output(in3,g.LOW)
        g.output(in4,g.LOW)

    elif x=='f':
        print("Motor 2 turned forward")
        g.output(in1,g.HIGH)
        g.output(in2,g.LOW)
        temp2=1

    elif x=='b':
        print("Motor 2 turned backward")
        g.output(in3,g.LOW)
        g.output(in4,g.HIGH)
        temp2=0

    elif x=='l':
        print("Motor 2 is in low speed now")
        m2.ChangeDutyCycle(25)

    elif x=='m':
        print("Motor 2 is in medium speed now")
        m2.ChangeDutyCycle(50)

    elif x=='h':
        print("Motor 2 is in high speed now")
        m2.ChangeDutyCycle(100)
    
    elif x=='e':
        g.cleanup()
        print("GPIO Clean up")
        exit()
    
    else:
        print("<<<  wrong entry  >>>")
        print("please enter ta valid command to continue.....")
        
# controle do servo
# f deixa a 90 graus
# l deixa a 180 graus
# r deixa a 0 graus
def servoD(x):
    if x == 'r':
        servo1.ChangeDutyCycle(2)
    elif x == 'l':
        servo1.ChangeDutyCycle(13)
    elif x == 'f':
        servo1.ChangeDutyCycle(7)
        
# checa uma rotacao de 90 graus
def rotate90(ser) :
    rot = 0
    while rot < 1.57 and rot > (-1.57):
        try:
            line = float(ser.readline().decode('utf-8').rstrip())
            print("\n")
            print(line, rot)
            line = float(line)*0.1 
            rot = line + rot
        except (KeyboardInterrupt):
            break
        except:
            pass
    
# funcao principal de teste 
def main():
    # for serial reading is used
    #     line = ser.readline().decode('utf-8').rstrip()
    ser = serial.Serial(serialPort, 9600, timeout=1)
    ser.flush()
    
    while(1) :
            
        d = retDist()
        
        if d<16 :
            servoD('r')
            sleep(0.5)
            d = retDist()
            if d<16 :
                servoD('l')
                sleep(0.5)
                d = retDist()
                if d<16 :
                    print("Dead End")
                else:
                    motor1('s')
                    motor2('f')
                    rotate90(ser)
                    motor1('f')
                    motor2('f')
            else:
                motor1('f')
                motor2('s')
                rotate90(ser)
                motor1('f')
                motor2('f')
        else:
            motor1('f')
            motor2('f')
        servoD('f')
        sleep(0.5)
        ###
    
    ser.close()
    
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        ser.close()
        g.cleanup()

