__author__ = 'mariohernandez'

class Carro(object):

    automatico = False
    manual = False
    promedio = 0
    maxPuertas = 0
    maxColores = 0
    maxVelocidades = 0
    max = 0
    min = 0
    maxHorsePower = 0
    motor = ""
    id = ""
    score = 0

    def __init__(self):
        self.min = float("inf")
        pass

    def __str__(self):
        return self.__dict__