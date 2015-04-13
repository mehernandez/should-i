__author__ = 'mariohernandez'

class Review(object) :

    autor = ""
    titulo = ""
    texto = ""
    sugerencias = ""
    performanceRating = 0
    comfortRating = 0
    fuelEconomyRating = 0
    funToDriveRating = 0
    interiorRating = 0
    exteriorRating = 0
    buildQualityRating = 0
    reliabilityRating = 0

    def __init__(self):

        pass

    def __str__(self):
        return self.__dict__