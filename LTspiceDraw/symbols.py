import json
from file_interface import *

class SymbolNotFound(Exception):
    """Requested Symbol Not Found. The source for one or more of the components in the circuit was not found."""

class SymbolStash:
    
    def __init__(self, directory_invariant=True):
        
        # Dictionary storing (str) symbol_name -> (str) symbol_loc
        self.symbols_loc = {}
        
        # Dictionary storing (str) symbol_name -> (list of Geometry objects) geometries
        self.compiled_symbols = {}
        
        self.directory_invariant = directory_invariant
        
    def save(self):
        raise NotImplementedError
    
    def get_dicts(self):
        raise NotImplementedError
        
    # disabled locs storage because we need json
    # def get_locs(self):
    #     raise NotImplementedError
        
    def get_symbols(self):
        raise NotImplementedError
        
    def missing_symbol(self, name):
        raise SymbolNotFound
    
    def get_symbol(self, symbol_name):
        try:
            print(self.get_symbols())
            self.get_symbols()[symbol_name]
        except KeyError:
            self.missing_symbol(symbol_name)
    
    def add_symbol(self, name, code):
        
        if self.directory_invariant:
            name = Path(name).name
        
        self.compiled_symbols[name] = parser(code)
        
class WebSymbolStash(SymbolStash):
    
    def __init__(self, localStorage, key, alert_method, directory_invariant=True):
        super().__init__(directory_invariant)
        
        self.localStorage = localStorage
        self.key = key
        self.alert_method = alert_method
        
        if self.localStorage.getItem(self.key) == None:
            self.localStorage.setItem(self.key, json.dumps({}))
        
    def save(self):
        self.localStorage.setItem(self.key, json.dumps(self.compiled_symbols))
    
    def get_dicts(self):
        return json.loads(self.localStorage.getItem(self.key))
        
    # disabled locs storage because we need json
    # def get_locs(self):
    #     return self.get_dicts()[0]
        
    def get_symbols(self):
        return self.get_dicts()#[1] 
    
    def missing_symbol(self, name):
        # Symbol Not Found, prompt user to upload
        if self.alert_method==None:
            super().missing_symbol(name)
        return self.alert_method("Missing symbol " + name, "Upload this symbol to use this circuit")
    
class LocalSymbolStash(SymbolStash):
    pass # TODO: Implement a way to read directories and get the symbol files...