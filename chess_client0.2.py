import time
import socket
import rsa
from random import choice
from threading import Thread
import os
import json

def err_handler(function):
    def wrapper(*args,**kwargs):
        try:
            result = function(*args,**kwargs)
            return result
        except Exception as err:
            add_str('An error occured in ', function.__name__)
            with open('error_log.txt','a') as err_file:
                err_file.write('[' + ctime() + '] ' +' in ' + function.__name__ + ' ' + str(err.args) + '\n')
    return wrapper


class ServerListener(Thread):

    @err_handler
    def __init__(self):
        Thread.__init__(self)
        self.disconnected = False
        
    @err_handler
    def get_data(self):
        try:
            server_data = client_sock.recv(1024)
            if not server_data:
                print('system: disconnected by server')
                return False
        except ConnectionResetError:
            add_str('system: disconnected by server (connection reset)')
            return False
        add_str(xor_crypt(server_data, xor_key).decode('utf-8'))
        return True

    @err_handler
    def send_data(self, message):
        try:
            client_sock.send(xor_crypt(message.encode('utf-8'), xor_key))
            return True
        except ConnectionResetError:
            add_str('system: disconnected by server')
            return False

    @err_handler
    def run(self):
        while True:
            server_data = self.get_data()
            if not server_data:
                self.disconnected = True
                break
            
@err_handler
def xor_crypt(string:bytes, key:bytes) -> bytes:
    key_len = len(key)
    fitted_key = bytes(key[index % key_len] for index in range(len(string)))
    crypto_str = bytes([string[index] ^ fitted_key[index] for index in range(len(string))])
    return crypto_str

@err_handler
def print_screen():
    os.system('cls')
    for msg in messages[-MAX_MESSAGES:]:
        print(msg)
        
@err_handler
def add_str(msg):
    messages.append(msg)
    print_screen()


ADDRESS, PORT = '127.0.0.1', 6666
KEYLEN = 64
MAX_MESSAGES = 20
messages = []
while True:
    serverListener = ServerListener()
    xor_key = bytes([choice(b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTYVWXYZ1234567890+/') for i in range(KEYLEN)])
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((ADDRESS,PORT))
    server_public_key_data = client_sock.recv(1024)
    server_key = rsa.PublicKey.load_pkcs1(server_public_key_data)
    encrypted_key = rsa.encrypt(xor_key, server_key)
    client_sock.send(encrypted_key)
    serverListener.start()
    while True:
        player_input = input('Enter data to send: ')
        add_str(player_input)
        if player_input == 'f': # find game
            serverListener.send_data('f')
        elif player_input == 'a': # accept game
            serverListener.send_data('a')
        elif player_input == 's': # do a step
            serverListener.send_data('s')
        elif player_input == 'r': # reject ready game
            serverListener.send_data('r')
        elif player_input == 'e': # exit from current game
            serverListener.send_data('e')
        elif player_input == 'c':
            serverListener.send_data('c')
        elif player_input == '!help':
            add_str('f - find game')
            add_str('a - accept game')
            add_str('s - do a step in game (20% of lose)')
            add_str('r - reject ready game')
            add_str('c - cancel game finding')
            add_str('e - exit from current game(automaticaly lose)')
        elif player_input == '!hello':
            serverListener.send_data('hello')
        else:
            add_str('Wrong input. Try again or !help to see the list of commands')
        if serverListener.disconnected:
            add_str('Disconnected')
            break  
    client_sock.close()

