import requests
from lxml import html
from lxml import etree

#local
from connector import Connector
from credential import Credential    


class Connector_PfSense(Connector):

    def __init__(self, credential):
        super().__init__(credential)
        self.s = requests.session()
        self.magic_csrf_token = None
        self.verify = False

        if self.credential.ssl:
            self.credential.host = "https://%s/" % self.credential.host
        else:
            self.credential.host = "http://%s/" % self.credential.host
        
    def connect(self):
        # Get the Magic CSRF Token
        r = self.s.get("%sindex.php" % self.credential.host, verify=self.verify)
        try:
            self.magic_csrf_token = html.fromstring(r.text).xpath('//input[@name=\'__csrf_magic\']/@value')[0]
        except:
            self.magic_csrf_token = ""

        # Login into Firewall Webinterface
        r = self.s.post("%sindex.php" % self.credential.host,
                data={
                    "__csrf_magic": self.magic_csrf_token,
                    "usernamefld": self.credential.username,
                    "passwordfld": self.credential.password,
                        "login": "Login"
                },
                verify=self.verify)
                
        #get new csrf token
        self.magic_csrf_token = html.fromstring(r.text).xpath('//input[@name=\'__csrf_magic\']/@value')[0]
        if html.fromstring(r.text).xpath('//title/text()')[0].startswith("Login"):
            exit("Login was not Successful!")

        # download configuration
        self.login_success = True

    def retrieve(self):
        r = self.s.post("%sdiag_backup.php" % self.credential.host,
                data={
                    "__csrf_magic": self.magic_csrf_token,
                    "download": "Download configuration as XML",
                    "encrypt_password": "",
                    "backuparea": "",
                    "donotbackuprrd": "yes"}, verify=self.verify)

        if html.fromstring(r.text).xpath('count(//pfsense)') != 1.0:
            exit("Something went wrong! the returned Content was not a PfSense Configuration File!")
        # safe or output the Configuration
        return r.text

    def __str__(self):
        return f"HOST : {self.credential.host} ; SSL : {self.credential.ssl} ; Username : {self.credential.username} ; Password : {self.credential.password}"

cred = Credential("pfsense", "192.168.140.250", False, "admin", "pfsense")
pfsense = Connector_PfSense(cred)
print(pfsense)
pfsense.connect()
print(pfsense.retrieve())

"""
EXAMPLE
cred = Credential("pfsense", "192.168.140.250", False, "admin", "pfsense")
pfsense = Connector_PfSense(cred)
print(pfsense)
pfsense.connect()
print(pfsense.retrieve())
"""
