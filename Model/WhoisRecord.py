class Whois():
    #attributi
    domain = None
    creation_date = None
    updated_date = None
    expiration_date = None
    name = None
    org = None
    location = None
    registrar = None
    email = None

    #setters

    def set_domain(self,domain):
        self.domain = domain

    def set_creation_date(self,creation_date):
        self.creation_date = creation_date

    def set_updated_date(self,updated_date):
        self.updated_date = updated_date

    def set_expiration_date(self,expiration_date):
        self.expiration_date = expiration_date

    def set_name(self,name):
        self.name = name
    
    def set_org(self,org):
        self.org = org

    def set_location(self,location):
        self.location = location
    
    def set_registrar(self,registrar):
        self.registrar = registrar
    
    def set_email(self,email):
        self.email = email

    #getters

    def get_domain(self) -> list:
        return self.domain

    def get_creation_date(self) -> str:
        return self.creation_date

    def get_updated_date(self) -> str:
        return self.updated_date

    def get_expiration_date(self) -> str:
        return self.expiration_date

    def get_name(self) -> str:
        return self.name

    def get_org(self) -> str:
        return self.org

    def get_location(self) -> str:
        return self.location

    def get_registrar(self) -> str:
        return self.registrar

    def get_email(self) -> str:
        return self.email