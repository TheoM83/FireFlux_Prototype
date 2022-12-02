class Credential:  

    def __init__(self, firewall, host, ssl, username, password):
        self.firewall = firewall
        self.host = host 
        self.ssl = ssl
        self.username = username
        self.password = password
    
    #Connect to the interface
    def get_host(self):
        return self.host

    def get_ssl(self):
        return self.ssl

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def __str__(self):
        return f"FIREWALL : {self.firewall} ; HOST : {self.host} ; SSL : {self.ssl} ; USERNAME : {self.username} ; PASSWORD : {self.password}"