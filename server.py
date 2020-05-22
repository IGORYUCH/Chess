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
    


    def run(self):
        while True:
            sleep(2)
            try:
                first_player, second_player = waiting_clients[0], waiting_clients[1]
                first_player.opponent, second_player.opponent = second_player, first_player
                first_player.send_msg('server: game is ready. Send "a" to accept the game')
                second_player.send_msg('server: game is ready. Send "a" to accept the game')
                ready_clients.extend([first_player, second_player])
                waiting_clients.remove(first_player)
                waiting_clients.remove(second_player)
            except IndexError:
                pass
            for client in ready_clients:
                if not client.accepted:
                    print(client.name)
                    client.exceed_time -= 1
                    if client.exceed_time <= 0:
                        ready_clients.remove(client)
                        ready_clients.remove(client.opponent)
                        client.send_msg('server: Time to accept exceed. You are excluded from ready to play queue')
                        client.opponent.send_msg('server: Your opponent\'s time exceeded. You are excluded from ready to play queue')
                        client.opponent.exceed_time, client.exceed_time = 10, 10
                        client.accepted, client.opponent.accepted = False, False
                        client.opponent.opponent, client.opponent = None, None
            print(get_date(), 'connected:', len(connected_clients),'waiting:',
                  len(waiting_clients), 'playing:', len(playing_clients),'ready:', len(ready_clients))

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
        self.connected = True
        self.xor_key = None
        self.opponent = None
        self.name = 'User' + str(users)
        self.accepted = False
        self.exceed_time = 10
        self.step = False


    def disconnect(self, reason):
        print(get_date(), reason, self.address)
        if self in playing_clients:
            self.opponent.step = False
            playing_clients.remove(self)
            playing_clients.remove(self.opponent)
            self.opponent.send_msg('server: Your opponent disconnected. You autimatically win')
            self.opponent.opponent = None
        elif self in ready_clients:
            self.opponent.accepted = False
            self.opponent.exceed_time = 10
            ready_clients.remove(self.opponent)
            ready_clients.remove(self)
            self.opponent.send_msg('server: Your opponent disconnected. Excluded from ready to play queue')
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
        while True:
            client_data = self.get_msg()
            if not client_data:
                break
            print(get_date(), 'get', client_data, 'from', self.address)
            if client_data == 'hello':
                for client in connected_clients:
                    client.send_msg('server: hello from ' + self.name)
                    #client.send_msg('server: hello from '+self.name)
            elif client_data == 'f':
                if self in waiting_clients:
                    self.send_msg('server: you are already in ready to play queue')
                elif self in ready_clients or self in playing_clients:
                    self.send_msg('server: already in game')
                else:
                    waiting_clients.append(self)
                    self.send_msg('server: added  in ready to play queue')
            elif client_data == 'c':
                if self in waiting_clients:
                    waiting_clients.remove(self)
                    self.send_msg('server: excluded from ready to play queue')
                else:
                    self.send_msg('server: you are not in ready to play queue')
            elif client_data == 'r':
                if self in waiting_clients:
                    waiting_clients.remove(self)
                    self.time_to_wait = 10
                    self.wait_for_accept = False
                else:
                    self.send_msg('server: you are not in ready to play queue')
            elif client_data == 'a':
                if self in ready_clients:
                    if self.accepted:
                        self.send_msg('server: game already accepted')
                    else:
                        self.accepted = True
                        self.opponent.send_msg('server: opponent accepted the game')
                        if self.accepted and self.opponent.accepted:
                            if self.step:
                                self.send_msg('server: you plays first')
                                self.opponent.send_msg('server: your opponent plays first')
                            else:
                                self.send_msg('server: your opponent plays first')
                                self.opponent.send_msg('server: you plays first')
                            playing_clients.append(self)
                            playing_clients.append(self.opponent)
                            ready_clients.remove(self)
                            ready_clients.remove(self.opponent)
                            self.accepted = False
                            self.opponent.accepted = False
                        else:
                            self.step = True
            elif client_data == 's':
                if self in playing_clients:
                    if self.step:
                        self.step = not self.step
                        self.opponent.step = not self.opponent.step
                        if random.randint(1,8) == 8:
                            self.send_msg('server: you accidentaly lose. Opponent\'s win')
                            self.opponent.send_msg('server: you accidentaly win. Gratulations!')
                            playing_clients.remove(self.opponent)
                            playing_clients.remove(self)
                            self.step = False
                            self.opponent.step = False
                            self.opponent.opponent = None
                            self.opponent = None
                            
                        else:
                            self.send_msg('server: you did a step. Opponent\'s time to play')
                            self.opponent.send_msg('server: opponent did a step. Your time to play')
                        
                    else:
                        self.send_msg('server: it\'s not your time to play')
                else:
                    self.send_msg('server: you are not playing')
            else:
                print(get_date(), 'can\'t recognize:',client_data, 'from', self.address)
                break


ADDRESS, PORT = '127.0.0.1', 6666
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
    connected_clients.append(new_client)
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
