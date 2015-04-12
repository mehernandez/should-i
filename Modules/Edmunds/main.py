__author__ = 'mariohernandez'

import json
import base64
import io
from httplib import *
from xml.etree import ElementTree
from Models.Modulo import *
from Carro import Carro

class Edmunds(Modulo) :

    CONSUMER_KEY = None
    PRIVATE_KEY = None
    BEARER_TOKEN = None
    MASHAPE_TOKEN = None
    base_URL = "api.edmunds.com"
    connection = HTTPSConnection(base_URL)
    base_URL2 = "fueleconomy.gov"
    connection2 = HTTPConnection(base_URL2)
    connection3 = HTTPConnection(base_URL2)




    def __init__(self) :
        pass



    def pedido(perfil=None,tiempo=-1,params=None):
        pass


    def init(self, marca, modelo, anio):

        styles = self.consultarStylesEdmunds(marca, modelo, anio)


        # Elementos del Json

        carro = Carro()

        # Asignacion de valores de Edmunds

        for style in styles:

            #print json.dumps(style, indent=4)
            carro.id = style["id"]
            carro.motor = (style["engine"])["type"]
            #
            horse = (style["engine"])["horsepower"]
            if horse > carro.maxHorsePower:
                carro.maxHorsePower = horse
            #
            speeds = style["transmission"]["numberOfSpeeds"]
            if speeds > carro.maxVelocidades:
                carro.maxVelocidades = speeds
            #
            trans = (style["transmission"])["transmissionType"]
            if trans == "AUTOMATIC":
                carro.automatico = True
            else:
                carro.manual = True
            #
            colors = len(style["colors"])
            if colors > carro.maxColores:
                carro.maxColores = colors
            #
            puertas = style["numOfDoors"]
            if puertas > carro.maxPuertas:
                carro.maxPuertas = puertas
            #
            precio = (style["price"])["baseMSRP"]
            #
            carro.promedio += precio
            #
            if precio > carro.max:
                carro.max = precio
            #
            if precio < carro.min:
                carro.min = precio

        carro.promedio = carro.promedio / len(styles)

        # Ahora la consulta al API de Fuel Economy

        idFuel = self.consultarIdFuelEconomy(marca, modelo, anio)

        carro.score = self.consultarEmisiones(idFuel)

        print json.dumps(carro.__dict__, indent=4)

        return json.dumps(carro, default=lambda o: o.__dict__, indent=4)




    def consultarEmisiones(self, id):
        query = "/ws/rest/vehicle/emissions/{0}" \
            .format(id)
        self.connection3.request("GET", url=query)
        response = self.connection3.getresponse()

        if response.status == 200:
            ans = response.read()

            print (ans)

            tree = ElementTree.fromstring(ans)

            prom = 0

            for child in tree :

                prom += float(child.find("score").text)

            prom = prom/len(tree)

           # print(prom)

            return prom



        else:
            print("Failed")
            print(response.read())

    def consultarIdFuelEconomy(self, marca, modelo, anio):
        query = "/ws/rest/vehicle/menu/options?year={2}&make={0}&model={1}" \
            .format(marca, modelo, anio)
        self.connection2.request("GET", url=query)
        response = self.connection2.getresponse()

        if response.status == 200:
            ans = response.read()

            print (ans)

            tree = ElementTree.fromstring(ans)

            for child in tree :

                return child.find("value").text

           # print(tree.iter("menuItems").iter("menuItem").text)
        else:
            print("Failed")
            print(response.read())



    def consultarStylesEdmunds(self, marca, modelo, anio):
        query = "/api/vehicle/v2/{0}/{1}/{2}/styles?view=full&fmt=json&api_key=6zca5s7tcwmd53pjdbn7tqzw" \
            .format(marca, modelo, anio)
        self.connection.request("GET", url=query)
        response = self.connection.getresponse()
        if response.status == 200:
            ans = response.read()
            parsed = json.loads(ans)
            #  print json.dumps(parsed, indent=4)
            #  respuesta = analizar_carros(parsed["styles"])
            return parsed["styles"]
        else:
            print("Failed to search tweets")
            print(response.read())



    def get_token(self):
        bearer_creds = base64.b64encode(CONSUMER_KEY + ":" + PRIVATE_KEY)
        headers = {"Authorization": "Basic " + bearer_creds,
                   "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        body = "grant_type=client_credentials"
        self.connection.request("POST", "/oauth2/token", body, headers)
        response = self.connection.getresponse()
        if response.status == 200:
            ans = response.read()
            parsed = json.loads(ans)
            global BEARER_TOKEN
            BEARER_TOKEN = parsed["access_token"]
        else:
            print("Failed to authenticate")
            print(response.read())


    def serialize_data(self):
        with io.open('../data/data.json', 'w') as f:
            json_file = {'CONSUMER_KEY': CONSUMER_KEY,
                         'PRIVATE_KEY': PRIVATE_KEY,
                         'BEARER_TOKEN': BEARER_TOKEN,
                         'MASHAPE_TOKEN': MASHAPE_TOKEN}
            f.write(unicode(json.dumps(json_file, ensure_ascii=False)))


    def deserialize_data(self):
        with io.open('../data/data.json', 'r') as f:
            parsed = json.loads(f.readline())
            global CONSUMER_KEY
            global PRIVATE_KEY
            global BEARER_TOKEN
            global MASHAPE_TOKEN
            CONSUMER_KEY = parsed["CONSUMER_KEY"]
            PRIVATE_KEY = parsed["PRIVATE_KEY"]
            MASHAPE_TOKEN = parsed["MASHAPE_TOKEN"]
            try:
                BEARER_TOKEN = parsed["BEARER_TOKEN"]
            except Exception:
                self.get_token()

#consultarStylesEdmunds("audi", "a4", "2015")

#consultarIdFuelEconomy("audi" , "a4" , "2015")

edmunds = Edmunds()
edmunds.init("audi","a3","2015")
