class Target:
    # ip = ""
    # port = ""
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


    def toString(self):
        print "Target: {} - {}".format(self.ip,self.port)

    def __str__(self):
        return "Target: {} - {}".format(self.ip,self.port)
