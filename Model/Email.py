class Email:
    #attributi
    urls = None
    sender = []

    #setters

    def set_urls(self,urls):
        self.urls = urls

    def set_sender(self,sender):
        self.sender = sender
    

    #getters

    def get_urls(self) -> list:
        return self.urls

    def get_sender(self) -> str:
        return self.sender
    