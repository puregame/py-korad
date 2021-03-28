import socket

class KoradComm(object):
    def connect(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def send_receive(self, message):
        raise NotImplementedError()

    def send(self, message):
        raise NotImplementedError()

class KoradUdpComm(KoradComm):
    def __init__(self, localAddress, deviceAddress, port):
        self.clientAddress = (localAddress, port)
        self.deviceAddress = (deviceAddress, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        self.sock.bind(self.clientAddress)
        self.sock.settimeout(1.0)

    def close(self):
        self.sock.close()

    def send_receive(self, message):
        # build the message
        messageb = bytearray()
        messageb.extend(map(ord, message))
        messageb.append(0x0a)

        startTime = time.time()
        while 1:
            sent = self.sock.sendto(messageb , self.deviceAddress)
            self.sock.settimeout(1.0) 
            data, server = self.sock.recvfrom(1024)
            if len(data) > 0:
                return data.decode('utf-8')
            
            if time.time() - startTime > 3:
                print ("UDP timeout")
                return " "

    def send(self, message):
        # build the message
        messageb = bytearray()
        messageb.extend(map(ord, message))
        messageb.append(0x0a)

        sent = self.sock.sendto(messageb , self.deviceAddress)


class KoradSerialComm(KoradComm):
    pass