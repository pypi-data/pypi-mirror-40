import json
import pandas as pd

class Response:
    
    def __init__(self, response):
        if type(response) == str:
            try:
                self.response = json.loads(response)
            except json.JSONDecodeError as decodeErr:
                print ("JSON Decode Error:",decodeErr) 
                raise Exception("no (valid) response from broker")
        else:
            raise Exception("response must be of type str")
            
    def __repr__(self):
        description = "Broker Response"
        #find number of results
        try:
            ntot = self.response["response"]["numFound"]            
        except:
            ntot = 0
            pass
        try:
            ndocs = len(self.response["response"]["docs"])            
        except:
            ndocs = 0
            pass
        description += "\n- documents: {0} from {1}".format(ndocs, ntot)
        if ndocs>0:
            try:
                start = self.response["response"]["start"]            
            except:
                start = 0
            description += ", starting at {0}".format(start)
        if "facet_counts" in self.response:    
            description += "\n- facet_counts:"
            if ("facet_queries" in self.response["facet_counts"]) & bool(self.response["facet_counts"]["facet_queries"]): 
                description += "\n  - facet_queries ({0})".format(len(self.response["facet_counts"]["facet_queries"]))
            if ("facet_fields" in self.response["facet_counts"]) & bool(self.response["facet_counts"]["facet_fields"]): 
                description += "\n  - facet_fields ({0})".format(len(self.response["facet_counts"]["facet_fields"]))
            if ("facet_ranges" in self.response["facet_counts"]) & bool(self.response["facet_counts"]["facet_ranges"]): 
                description += "\n  - facet_ranges ({0})".format(len(self.response["facet_counts"]["facet_ranges"]))
            if ("facet_intervals" in self.response["facet_counts"]) & bool(self.response["facet_counts"]["facet_intervals"]): 
                description += "\n  - facet_intervals ({0})".format(len(self.response["facet_counts"]["facet_intervals"]))
            if ("facet_heatmaps" in self.response["facet_counts"]) & bool(self.response["facet_counts"]["facet_heatmaps"]): 
                description += "\n  - facet_heatmaps ({0})".format(len(self.response["facet_counts"]["facet_heatmaps"]))
        return(description)    
    
    def raw(self): 
        return(self.response)
    
    def numFound(self): 
        try:
            return(self.response["response"]["numFound"])
        except:
            return(None)
        
    def start(self): 
        try:
            return(self.response["response"]["start"])
        except:
            return(None)    
    
    def docs(self): 
        try:
            return(pd.DataFrame(self.response["response"]["docs"]))
        except:
            return(None)
        
        
        
