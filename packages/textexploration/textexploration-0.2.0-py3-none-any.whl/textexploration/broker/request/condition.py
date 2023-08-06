
class Condition:
    
    def __init__(self):
        self.type = None
        self.allowNot = None
        self.allowFacetquery = None
        self.allowExpansion = None
        self.condition = {
        }  
        
    def type(self):
        return(self.type) 
    
    def raw(self): 
        """Get the condition object"""
        if self.type is None:
            raise Exception("no (valid) condition")
        self.condition["type"] = self.type
        return(self.condition)
    
    def param_not(self, value):
        """Negation of the condition"""
        if self.allowNot:
            try:
                currentNot = self.condition["not"]
            except Exception:
                currentNot = None
            if type(value) is bool:
                self.condition["not"] = value
            elif not (value is None):
                raise Exception("value must be a boolean")
            return(currentNot)
        else:
            raise Exception("negation not implemented for this condition")
        
    def param_expansion(self, expansion):
        """Applied expansion for the condition"""
        if self.allowExpansion:
            try:
                currentExpansion = self.condition["expansion"]
            except Exception:
                currentExpansion = None
            if type(expansion) is Expansion:
                self.condition["expansion"] = expansion.raw()
            elif not (expansion is None):
                raise Exception("value must be an expansion")
            return(currentExpansion)
        else:
            raise Exception("expansion not implemented for this condition")    
        
    def param_facetquery(self, value):
        """Create facetquery from condition"""
        if self.allowFacetquery:
            #get current
            try:
                currentFacetquery = self.condition["facetquery"]
            except Exception:
                currentFacetquery = None
            try:
                currentKey = self.condition["key"]
            except Exception:
                currentKey = None   
            #update
            if type(value) is bool:
                self.condition["facetquery"] = value
                #remove previous key    
                try:
                    del self.condition["key"]
                except:
                    pass
            elif type(value) is str:
                self.condition["facetquery"] = True
                self.condition["key"] = value
            elif not(value is None):
                raise Exception("value must be a boolean or string")
            if not (currentKey is None):
                return currentKey
            else:
                return currentFacetquery
        else:
            raise Exception("negation not implemented for this condition")       
        
class ConditionEquals(Condition):
    
    def __init__(self, field, value):
        super().__init__()
        self.type = "equals"
        self.allowNot = True
        self.allowFacetquery = True
        self.allowExpansion = True
        if not(type(field) is str):
            raise Exception("field must be a string")
        self.condition["field"] = field
        if not ((type(value) is str) | (type(value) is bool) | (type(value) is list)):
            raise Exception("value must be a string, boolean or list of strings or booleans")
        self.condition["value"] = value
        
class ConditionPhrase(Condition):
    
    def __init__(self, field, value):
        super().__init__()
        self.type = "phrase"
        self.allowNot = True
        self.allowFacetquery = True
        self.allowExpansion = True
        if not(type(field) is str):
            raise Exception("field must be a string")
        self.condition["field"] = field
        if not ((type(value) is str) | (type(value) is list)):
            raise Exception("value must be a string or list of strings")
        self.condition["value"] = value        
 
class ConditionWildcard(Condition):
    
    def __init__(self, field, value):
        super().__init__()
        self.type = "wildcard"
        self.allowNot = True
        self.allowFacetquery = True
        if not(type(field) is str):
            raise Exception("field must be a string")
        self.condition["field"] = field
        if not ((type(value) is str) | (type(value) is list)):
            raise Exception("value must be a string or list of strings")
        self.condition["value"] = value        

class ConditionRegexp(Condition):
    
    def __init__(self, field, value):
        super().__init__()
        self.type = "regexp"
        self.allowNot = True
        self.allowFacetquery = True
        if not(type(field) is str):
            raise Exception("field must be a string")
        self.condition["field"] = field
        if not ((type(value) is str) | (type(value) is list)):
            raise Exception("value must be a string or list of strings")
        self.condition["value"] = value        

class ConditionRange(Condition):
    
    def __init__(self, field, start, end):
        super().__init__()
        self.type = "range"
        self.allowNot = True
        self.allowFacetquery = True
        if not(type(field) is str):
            raise Exception("field must be a string")
        self.condition["field"] = field        
        if not(start is None):
            if not ((type(start) is str) ):
                raise Exception("start must be a string")
            else:
                self.condition["start"] = start   
        if not(end is None):
            if not ((type(end) is str) ):
                raise Exception("end must be a string")
            else:
                self.condition["end"] = end            


class ConditionCQL(Condition):
    
    def __init__(self, field, value):
        super().__init__()
        self.type = "cql"
        self.allowNot = True
        self.allowFacetquery = True
        if not(type(field) is str):
            raise Exception("field must be a string")
        self.condition["field"] = field
        if not ((type(value) is str) | (type(value) is list)):
            raise Exception("value must be a string or list of strings")
        self.condition["value"] = value      
        
class Expansion:
    
    def __init__(self, value, parameters):
        if not(type(value) is str):
            raise Exception("value must be a string")
        self.expansion = {
            "type" : value
        }  
        if type(parameters) is dict:
            self.expansion["parameters"] = parameters       
        elif not(parameters is None):
            raise Exception("parameters must be a dict")
        
    def raw(self): 
        """Get the expansion object"""
        return(self.expansion)        
            