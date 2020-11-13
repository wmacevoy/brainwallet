import sys
import unicodedata
from millerrabin import MillerRabin


class Check:
    @classmethod
    def isBoolean(cls,value):
        return type(value) is bool

    @classmethod

    def toBoolean(cls,value):
        if value:
            return True
        else:
            return False
    
    @classmethod
    def isInt(cls, value, min=None, max=None):
        if cls.isString(value) and value.isdigit():
            value = int(value)
        try:
            intValue = int(value)
        except:
            return False

        if intValue != value:
            return False

        if min is not None and intValue < min:
            return False
        if max is not None and intValue > max:
            return False

        return True

    @classmethod
    def toInt(cls, value, name="value", min=None, max=None):
        if not cls.isInt(value, min, max):
            raise ValueError(cls._toIntMessage(value, name, min, max))
        if cls.isString(value) and value.isdigit():
            value = int(value)
        return int(value)

    _MILLER_RABIN = MillerRabin()
    _PRIMES = set()

    @classmethod
    def isPrime(cls, value):
        if not cls.isInt(value):
            return False
        value = int(value)
        if value in cls._PRIMES:
            return True
        if cls._MILLER_RABIN.isProbablyPrime(value):
            cls._PRIMES.add(value)
            return True
        return False

    @classmethod
    def toPrime(cls, prime, name="prime"):
        if not cls.isPrime(prime):
            raise ValueError(cls._toPrimeMessage(prime, name))
        return int(prime)

    @classmethod
    def isList(cls, value):
        return type(value) == list

    PYTHON3 = (sys.version_info.major >= 3)
    UNICODE = str if PYTHON3 else unicode
    STRING = str if PYTHON3 else basestring

    @classmethod
    def isString(cls, value):
        q = isinstance(value, (cls.STRING, bytes))
        return q

    @classmethod
    def toString(cls, value):
        if not cls.isString(value):
            value = str(value)

        if not isinstance(value, cls.UNICODE):
            value = value.decode("utf-8")

        value = unicodedata.normalize("NFKD", value)

        return value

    @classmethod
    def _toMessage(cls, value, name):
        msg = str(name) + " (" + str(value) + ", a " + str(type(value)) + \
            " type)"
        return msg

    @classmethod
    def _toIntMessage(cls, value, name, min, max):
        msg = cls._toMessage(value, name) + " must be an integer"
        if min is not None and max is None:
            msg += " >= " + str(min)
        elif min is None and max is not None:
            msg += " <= " + str(max)
        elif min is not None and max is not None:
            msg += " in [" + str(min) + "," + str(max) + "]"
        return msg

    @classmethod
    def _toPrimeMessage(cls, value, name):
        msg = cls._toMessage(value, name) + " must be a prime"
        return msg
