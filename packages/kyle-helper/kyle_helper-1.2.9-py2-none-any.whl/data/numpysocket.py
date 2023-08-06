import socket
import numpy as np
from cStringIO import StringIO
import logging

class numpysocket():
    def __init__(self):
        pass

    def receive(self, port=7555):
        server_socket=socket.socket()
        server_socket.bind(('',port))
        server_socket.listen(1)
        client_connection,client_address=server_socket.accept()
        self.client_address = client_address
        ultimate_buffer=''
        while True:
            receiving_buffer = client_connection.recv(1024)
            if not receiving_buffer: break
            ultimate_buffer+= receiving_buffer
        received_array=np.load(StringIO(ultimate_buffer))['frame']
        client_connection.close()
        server_socket.close()
        return received_array

    def reply(self, array, port):
        self.send(array, server_address=self.client_address[0], port=port)

    def send(self, array, server_address='localhost', port=7555):
        
        if not isinstance(array,np.ndarray):
            print 'not a valid numpy image'
            return
        client_socket=socket.socket()
        try:
            client_socket.connect((server_address, port))
        except socket.error,e:
            return
        f = StringIO()
        np.savez_compressed(f,frame=array)
        f.seek(0)
        out = f.read()
        client_socket.sendall(out)
        client_socket.shutdown(1)
        client_socket.close()
        logging.info('array sent')
        pass




