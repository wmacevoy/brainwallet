import copy

class Memoable:
    def __init__(self,types,memo={}):
        self.__dict__['_types'] = types
        self.__dict__['_memo'] = self.defaults
        self.update(memo)

    @property
    def defaults(self):
        values = {}
        types=self.__dict__['_types']
        for name in types:
            values[name]=copy.deepcopy(types[name]['default'])
        return values

    @property
    def memo(self):
        return self.__dict__['_memo'].copy()

    def update(self,memo):
        types=self.__dict__['_types']
        for name in types:
            if name in memo:
                self._memo[name]=types[name]['py'](memo[name])
                
    def __repr__(self):
        return repr(self._memo)

    def __getattr__(self, name):
        memo=self.__dict__['_memo']
        return memo[name]

    def __setattr__(self,name,value):
        memo=self.__dict__['_memo']        
        types=self.__dict__['_types']        
        memo[name]=types[name]['py'](value)
