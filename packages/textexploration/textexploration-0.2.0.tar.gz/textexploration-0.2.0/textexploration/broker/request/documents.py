
class Documents:
    
    def __init__(self, start, rows):
        self.documents = {
        } 
        if type(start)==int:
            self.documents["start"] = start
        elif not(start is None):
            raise Exception("start must be an integer")
        if type(rows)==int:
            self.documents["rows"] = rows
        elif not(rows is None):
            raise Exception("rows must be an integer")   
            
        
    def raw(self): 
        """Get the documents object"""
        return(self.documents)
    
    def param_start(self, value):
        """start of documents"""
        try:
            currentStart = self.documents["start"]
        except Exception:
            currentStart = None
        if type(value) is int:
            self.documents["start"] = value
        elif not (value is None):
            raise Exception("value must be an integer")
        return(currentStart)
    
    def param_rows(self, value):
        """rows of documents"""
        try:
            currentRows = self.documents["rows"]
        except Exception:
            currentRows = None
        if type(value) is int:
            self.documents["rows"] = value
        elif not (value is None):
            raise Exception("value must be an integer")
        return(currentRows)
    
    def param_fields(self, value):
        """fields of documents"""
        try:
            currentFields = self.documents["fields"]
        except Exception:
            currentFields = None
        if type(value) is list:
            self.documents["fields"] = value
        elif not (value is None):
            raise Exception("value must be a list")
        return(currentFields)
    
        
