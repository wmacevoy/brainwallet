from rng import RNG
from millerrabin import MillerRabin

class Check:
    _RNG=RNG()
    _MILLER_RABIN=MillerRabin(10,_RNG)
    _PRIMES=set()

    @classmethod
    def isPrime(cls,prime,name="prime"):
        prime=cls.toInt(prime,name)
        if prime in cls._PRIMES: return prime
        if cls._MILLER_RABIN.isProbablyPrime(prime):
            cls._PRIMES.add(prime)
            return prime
        return False
        
    @classmethod
    def toPrime(cls,prime,name="prime"):
        if not cls.isPrime(prime,name):
            raise ValueError(str(name) + " must be prime")
        return int(prime)

    @classmethod
    def isInt(cls,value,name="value",min=None,max=None):
        ok = False
        try:
            ok = (int(value) == value)
        except:
            pass

        if not ok: return False
        value = int(value)
        if min != None and value < min: return False
        if max != None and value > max: return False
        return True

    @classmethod
    def toInt(cls,n,name="value",min=None,max=None):
        if not cls.isInt(cls,n,name,min,max):
            if min == None: min="-infinity"
            if max == None: max="+infinity"
            raise ValueError(str(name) + " must be an integer in the range [" + str(min) + "," + str(max) + "]")
        return int(n)

    @classmethod
    def isString(cls,value):
        try:
            value = cls.normalizeString(cls, value)
        except:
            return False
        return True

    @classmethod
    def toString(cls,value):
        try:
            return cls.normalizeString(cls, value)
        except:
            return str(value)

    @classmethod
    def isList(cls,value):
        return type(value) == list

    @classmethod
    def normalizeString(cls, txt):
        if isinstance(txt, str if sys.version < "3" else bytes):
            utxt = txt.decode("utf8")
        elif isinstance(txt, unicode if sys.version < "3" else str):  # noqa: F821
            utxt = txt
        else:
            raise TypeError("String value expected")

        return unicodedata.normalize("NFKD", utxt)
    

