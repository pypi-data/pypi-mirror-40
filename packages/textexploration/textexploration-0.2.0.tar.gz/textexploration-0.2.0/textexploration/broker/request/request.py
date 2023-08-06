import json
from .condition import Condition
from .documents import Documents

class Request:
    
    def __init__(self):
        self.request = {
            "response" : {
                "documents": {}
            }
        }
        
    def __repr__(self):
        return(json.dumps(self.request))
        
    def raw(self): 
        """Get the request object"""
        return(self.request)
    
    def cache(self, cache = None): 
        """Get and optionally change current setting cache"""
        try:
            currentCache = self.request["cache"]
        except Exception:
            currentCache = None
        if type(cache) is bool:
            self.request["cache"] = cache
        elif not (cache is None):
            raise Exception("cache must be of type bool") 
        return(currentCache)
    
    def condition(self, condition = None):
        """Get and optionally change current condition"""
        try:
            currentCondition = self.request["condition"]
        except Exception:
            currentCondition = None
        if isinstance(condition, Condition):
            self.request["condition"] = condition.raw()
        elif not (condition is None):
            raise Exception("invalid condition") 
        return(currentCondition)
    
    def documents(self, documents = None):
        """Get and optionally change current documents"""
        try:
            currentDocuments = self.request["response"]["documents"]
        except Exception:
            currentDocuments = None
        if isinstance(documents, Documents):
            self.request["response"]["documents"] = documents.raw()
        elif not (documents is None):
            raise Exception("invalid condition") 
        return(currentDocuments)
