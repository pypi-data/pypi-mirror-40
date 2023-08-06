import configparser

class Prime:
    def __init__(self):
        self.secrets_path = r'C:\Users\Datasoft\prime_secrets'
        self.config = configparser.ConfigParser()
        self.config.read(self.secrets_path)
        self.user_name = self.config.get("prime", "user_name")
        self.password = self.config.get("prime", "password")
