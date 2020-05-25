import socket
import rsa
#import json
import random
from time import sleep
from threading import Thread
from datetime import datetime

class EventLoop(Thread):

    def __init__(self):
        Thread.__init__(self)

    def connect_players(self):# connect ready to play players
        pass

    def add_task(self):
        pass

    def do_step(self):
        pass

    def accept_ready_game(self):
        pass
    
    def delete_client(self):
        pass
    


    def run(self) -> None:
        while True:
            sleep(1)
            try:
                first_player, second_player = waiting_clients[0], waiting_clients[1]
                first_player.opponent = waiting_clients[1]
                second_player.opponent = waiting_clients[0]
                waiting_clients.remove(first_player)
                waiting_clients.remove(second_player)
                print('pair finded')
                first_player.send_msg('READY')
                second_player.send_msg('READY')
                ready_clients.extend([first_player, second_player])
            except IndexError:
                pass
            for client in ready_clients[:]:
                if not client.accepted:
                    print(client.name)
                    client.exceed_time -= 1
                    if client.exceed_time <= 0:
                        ready_clients.remove(client)
                        ready_clients.remove(client.opponent)
                        client.send_msg('CANCEL Time to accept exceed')
                        client.opponent.send_msg('CANCEL Your opponent\'s time exceeded')
                        client.opponent.exceed_time, client.exceed_time = 10, 10
                        client.accepted, client.opponent.accepted = False, False
                        client.opponent.opponent, client.opponent = None, None
##            print(get_date(), 'connected:', len(connected_clients),'waiting:',
##                  len(waiting_clients), 'playing:', len(playing_clients),'ready:', len(ready_clients))

    def add_event(self):
        pass
            

def xor_crypt(string:bytes, key:bytes) -> bytes:
    key_len = len(key)
    fitted_key = bytes(key[index % key_len] for index in range(len(string)))
    crypto_str = bytes([string[index] ^ fitted_key[index] for index in range(len(string))])
    return crypto_str

def get_date() -> str:
    date = datetime.now()
    date_str = '[{0:0>2}-{1:0>2}-{2:0>4} {3:0>2}:{4:0>2}]'.format(date.day, date.month, date.year, date.hour, date.minute)
    return date_str


class ConnectedClient(Thread):

    def __init__(self, socket, address):
        Thread.__init__(self)
        self.address = address
        self.socket = socket
        self.xor_key = None
        self.opponent = None
        self.name = 'User' + str(users)
        self.accepted = False
        self.exceed_time = 10000
        self.step = False


    def disconnect(self, reason) -> None:
        print(get_date(), reason, self.address)
        if self in playing_clients:
            self.opponent.step = False
            playing_clients.remove(self)
            playing_clients.remove(self.opponent)
            self.opponent.send_msg('ALERT Your opponent disconnected. You autimatically win')
            self.opponent.opponent = None
        elif self in ready_clients:
            self.opponent.accepted = False
            self.opponent.exceed_time = 1000
            ready_clients.remove(self.opponent)
            ready_clients.remove(self)
            self.opponent.send_msg('CANCEL Your opponent disconnected')
        elif self in waiting_clients:
            waiting_clients.remove(self)
        connected_clients.remove(self)
        self.socket.close()
        

    def get_msg(self):
        try:
            encrypted_data = self.socket.recv(1024)
            if not encrypted_data:
                self.disconnect('connection closed by')
        except ConnectionResetError:
            self.disconnect('connection reset by')
        except ConnectionRefusedError:
            self.disconnect('connection refused by')
        except TimeoutError:
            self.disconnect('connection timed out with')
        else:
            return xor_crypt(encrypted_data, self.xor_key).decode('utf-8')
        return False
            
    
    def send_msg(self, msg):
        try:
            self.socket.send(xor_crypt(msg.encode('utf-8'), self.xor_key))
        except ConnectionResetError:
            self.disconnect('connection reset by')
        except ConnectionRefusedError:
            self.disconnect('connection refused by')
        except TimeoutError:
            self.disconnect('connection timed out with')
        else:
            return True
        return False


    def run(self):
        self.socket.send(public.save_pkcs1())
        raw_xor_key = self.socket.recv(1024)
        self.xor_key = rsa.decrypt(raw_xor_key, private)
        print(get_date(),'secure key received from', self.address)
        connected_clients.append(self)
        waiting_clients.append(self)
        while True:
            client_data = self.get_msg()
            if not client_data:
                break
            print(get_date(), 'get', client_data, 'from', self.address)
            if 'MOVE' in client_data:
                self.opponent.send_msg(client_data)
            elif client_data == 'ACCEPT':
                print('player accepted')
                if self in ready_clients:
                    if self.accepted:
                        self.send_msg('MSG game already accepted')
                    else:
                        self.accepted = True
                        self.opponent.send_msg('ACCEPT Opponent accepted the game')
                        if self.accepted and self.opponent.accepted:
                            self.send_msg('GAME')
                            self.opponent.send_msg('GAME')
##                            if self.step:
##                                self.send_msg('ALERT you plays first')
##                                print(xor_crypt('ALERT you plays first'.encode('utf-8'), self.xor_key))
##                                print(xor_crypt('ALERT you plays first'.encode('utf-8'), self.opponent.xor_key))
##                                self.opponent.send_msg('ALERT your opponent plays first')
##                            else:
##                                self.send_msg('ALERT your opponent plays first')
##                                self.opponent.send_msg('ALERT you plays first')
                            ready_clients.remove(self.opponent)
                            ready_clients.remove(self)
                            playing_clients.append(self.opponent)
                            playing_clients.append(self)
                            self.accepted = False
                            self.opponent.accepted = False
                else:
                    self.send_msg('server: you are not playing')
            else:
                print(get_date(), 'can\'t recognize:',client_data, 'from', self.address)
                self.disconnect('Wrong data')
                break

class Game():

    def __init__(first_player, second_player):
        self.white_player  = first_player
        self.black_player = second_player
        self.white_step = True
        self.black_step = False
        self.white_check = False
        self.black_check = False
            

VERSION = '0.3'
ADDRESS, PORT = '127.0.0.1', 6666
print(get_date(), 'chess game server ' + VERSION + ' running on ' + ADDRESS + ' ' + str(PORT))
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
server_sock.bind((ADDRESS, PORT))
public, private = rsa.newkeys(1024)
print(get_date(), 'key pair generated')
connected_clients = []
waiting_clients = []
ready_clients = []
playing_clients = []
users = 0
loop = EventLoop()
loop.start()
while True:
    server_sock.listen(0)
    sock,addr = server_sock.accept()
    new_client = ConnectedClient(sock,addr)
    new_client.start()
    users += 1

## f - искать игру
## e - вычти зи игры(поражение)
## a - принять игру
## r - отклонить игру
## s - сделать ход(12.5 шанс луза)

## k - король
## f - королева (ферзь)
## b - епископ (слон)
## r - крепость (ладья)
## k - рыцарь (конь)
## p - пешка
