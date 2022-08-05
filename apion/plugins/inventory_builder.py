class InventoryBuilder(object):
    def __init__(self, host, username, password, conn):
        self.host = host
        self.username = username
        self.password = password
        self.conn = conn

    def generate(self):
        ivars = {
            "ansible_user": self.username,
            "ansible_pass": self.password,
            "ansible_connection": self.conn,
        }
        inventory = {"all": {"hosts": self.host, "vars": ivars}}
        return inventory