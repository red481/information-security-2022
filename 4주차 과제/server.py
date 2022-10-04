# simple ciphercommunicator relay server
# this code shall not be modified, please edit client.py!!!

from random import random
from socket import AddressFamily, AddressInfo, SocketKind, socket
from threading import Thread
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from Crypto.Random import get_random_bytes

ENCRYPTION_KEY:bytes = b""
CLIENT_LIST:dict[AddressInfo, socket] = {}
BLOCK_SIZE = 16

class SocketWorker(Thread):
    def __init__(self, socket: socket, addr:AddressInfo):
        super().__init__()
        self.sock = socket
        self.addr = addr
        CLIENT_LIST[addr] = socket
        
        self.cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    
    def broadcast(self, msg:bytes):
        plaintext = self.cipher.decrypt(msg)
        unpaded_text = unpad(plaintext, BLOCK_SIZE)
        print(str(self.addr) + ": " + str(unpaded_text))
        
        for (addr, sock) in CLIENT_LIST.items():
            if addr == self.addr:
                print('same address')
                msg = input("Message: ")
                msg_encoded = msg.encode("UTF-8")
                print('encoded utf-8')
                padded_text = pad(msg_encoded, BLOCK_SIZE)
                ciphertext = self.cipher.encrypt(padded_text)
                print('text is encrypted.')
                
               
                sock.send(ciphertext)
                continue
            
            
            
            

    def run(self):
        self.sock.send(ENCRYPTION_KEY) 
        print('send by run')

        try:
            while True:
                recv_bytes = self.sock.recv(1024)
                self.broadcast(recv_bytes)
        except:
            CLIENT_LIST.pop(self.addr)


def accept_loop(sock:socket):
    while True:
        client, addr = sock.accept()
        print('socket accepted')
        print("[*] Accepted a connection from " + str(addr))
        #client.send(ENCRYPTION_KEY)
        print('send by accept_loop')
        SocketWorker(client, addr).start()
        
# generate random aes key for clients
ENCRYPTION_KEY = get_random_bytes(16)
print("[*] Key generated: " + str(ENCRYPTION_KEY))

master_socket = socket(AddressFamily.AF_INET, SocketKind.SOCK_STREAM)
master_socket.bind(('', 24000))
master_socket.listen(1024)

print("[*] Server started on 0.0.0.0:24000")
accept_loop(master_socket)
