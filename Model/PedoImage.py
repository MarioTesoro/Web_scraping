import math

class PedoImage:
    hostname = None
    local_path = None
    faces_found = None
    age_confidence= None
    porn_confidence = None
    key= None
    id=None
    counter = 1

    def __eq__(self, other):
        r= PedoImage()
        r=other
        #return (self.get_local_path() == r.get_local_path())
        return self.get_id() == r.get_id()
        
    def __hash__(self):
        #return hash(self.local_path)
        return hash(self.id)
    
    def convertToNumber(s):
        return int.from_bytes(s.encode(), 'little')
    
    #setters
    def set_id(self,id):
        self.id= id

    def set_hostname(self,hostname):
        self.hostname = hostname

    def set_local_path(self,local_path):
        self.local_path = local_path
    
    def set_faces_found(self,faces_found):
        self.faces_found = faces_found

    def set_age_confidence(self,age_confidence):
        self.age_confidence = age_confidence

    def set_porn_confidence(self,porn_confidence):
        self.porn_confidence = porn_confidence
    
    def set_key(self,key):
        self.key = key

    def set_counter(self,counter):
        self.counter = counter
   
    #getters
    def get_id(self):
        return self.id

    def get_hostname(self):
        return self.hostname

    def get_local_path(self)->str:
        return self.local_path
    
    def get_faces_found(self):
        return self.faces_found

    def get_age_confidence(self):
        return self.age_confidence

    def get_porn_confidence(self):
        return self.porn_confidence
    
    def get_key(self):
        return self.key

    def get_counter(self):
        return self.counter
