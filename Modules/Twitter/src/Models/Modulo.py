from abc import ABCMeta, abstractmethod


class Modulo(object):
    nombre = ""

    version = ""

    url = ""

    __metaclass__ = ABCMeta

    @abstractmethod
    def pedido(self, perfil=None, tiempo=-1, params=None):
        return []