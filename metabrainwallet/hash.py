class Hash:
    A = 25214903917
    B = 11
    @classmethod
    def advance(cls,state):
        return (cls.A * state + cls.B) & ((1 << 48) - 1)
    @classmethod    
    def hashString(cls,string):
        if string == None:
            return None
        utf8=bytes(str(string),'utf-8')
        hash=cls.hashBytes(utf8)
        return hash

    @classmethod    
    def hashBytes(cls,data):
        if data == None:
            return None
        i=0
        n=len(data)
        state = cls.advance(n)
        while i+6<=n:
            x=(data[i+0]<<0) | (data[i+1]<<8) | (data[i+2]<<16) | (data[i+3]<<24) | (data[i+4]<<32) | (data[i+5]<<40)
            state = cls.advance(state ^ x)
            i = i + 6
        pad=i+6-n
        x=((data[i+0] if i+0<n else pad)<<0) | ((data[i+1] if i+1 < n else pad)<<8) | ((data[i+2] if i+2<n else pad)<<16) | ((data[i+3] if i+3<n else pad)<<24) | ((data[i+4] if i+4<n else pad)<<32) | ((data[i+5] if i+5<n else pad)<<40)
        state = cls.advance(state ^ x)
        return state
