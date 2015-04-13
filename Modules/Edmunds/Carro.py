__author__ = 'mariohernandez'

class Carro(object):


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
    automatico = False

    def __init__(self):
        self.min = float("inf")
        self.manual = False
        self.automatico = False
        pass

    def __str__(self):
        return self.__dict__