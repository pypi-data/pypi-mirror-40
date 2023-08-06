import gevent
from gevent import socket, monkey
import json
import ipaddress
from subprocess import Popen, PIPE
from Target import Target

class BannerGrabber():
    targets = []
    vulnTargets = []
    ipTargets = []
    file = ""
    def __init__(self):
        self.targets = []
        self.vulnTargets = []
        self.ipTargets = []
        self.file = ""
        monkey.patch_all()

    def checkPort(self, ip, port):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            t = Target(ip, port)
            self.targets.append(t)
        else:
            pass


    def getBanner(self, t):
        s = socket.socket()
        s.connect((t.ip, t.port))
        s.send("HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024)
        s.close()
        for x in self.file:
            if x in banner:
                self.vulnTargets.append("{}:{}".format(t.ip, t.port))


    def networkScan(self, ip):
        i = str(ip)
        toping = Popen(['ping', '-c', '1', "-w", "1", "-s", "0", i], stdout=PIPE)
        output = toping.communicate()[0]
        hostalive = toping.returncode
        if hostalive == 0:
            if i not in self.ipTargets:
                self.ipTargets.append(i)

    def help(self):
        print "To use this library create a file db.json and add array of services you want to check"

    def scan(self, tar,path):
        self.vulnTargets = []
        self.ipTargets = []
        self.targets = []
        target = tar
        with open(path, 'r') as f:
            self.file = json.load(f)

        if "/" in target:
            network = ipaddress.ip_network(u"{}".format(target))
            for ip in network.hosts():
                self.networkScan(ip)

            if len(self.ipTargets) > 0:
                for ip in self.ipTargets:
                    jobs = [gevent.spawn(self.checkPort, ip, port) for port in range(1000)]
                    gevent.joinall(jobs)
        else:
            jobs = [gevent.spawn(self.checkPort, target, port) for port in range(1000)]
            gevent.joinall(jobs, timeout=int(1))

        jobs = [gevent.spawn(self.getBanner, t) for t in self.targets]
        gevent.joinall(jobs, timeout=int(1))

        if len(self.vulnTargets) > 0:
            print "Founded a vuln"
            print self.vulnTargets
            return self.vulnTargets
        else:
            print "0 vuln founded"
