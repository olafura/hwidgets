import ConfigParser

def getUsernamePassword():
    config = ConfigParser.RawConfigParser()
    config.read("hwidgets.conf")
    username = config.get("Server","username")
    password = config.get("Server","password")
    return (username, password)
