import socket
import rsa
import random
import json
from time import sleep
from threading import Thread
from datetime import datetime
from copy import deepcopy
from check_module import *
class EventLoop(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.events2 = []
        self.delay = 0.1
        self.tickrate = int(1/self.delay)
        self.active_games = []
        self.ready_pairs = []
        
    def disconnect(client, msg):
        print(get_date(), msg, client.address)
        if client.game:
            if game.white_player == self:
                game.black_player.send_msg('END Your opponent disconnected. You automatically win')
                game.black_player.socket.close()
            else:
                game.white_player.send_msg('END Your opponent disconnected. You automatically win')
                game.white_player.socket.close()
            self.active_games.remove(client.game)
        elif client in ready_clients:
            for pair in self.ready_pairs:
                if client in pair:
                    if client == pair[0]:
                        pair[1].send_msg('CANCEL Your opponent disconnected')
                    else:
                        pair[0].send_msg('CANCEL Your opponent disconnected')
                self.ready_pairs.remove(pair)
        elif client in waiting_clients:
            waiting_clients.remove(client)
        connected_clients.remove(client)
        client.socket.close()
        
        
    def find_pair(self):
        try:
            first_player = waiting_clients[0]
            second_player = waiting_clients[1]
            self.ready_pairs.append((first_player, second_player))
            waiting_clients.remove(first_player)
            waiting_clients.remove(second_player)
            first_player.send_msg('READY')
            second_player.send_msg('READY')
        except IndexError:
            pass

    def check_ready_pairs(self):
        to_delete = []
        for first,second in self.ready_pairs:
            if first.accepted and second.accepted:
                if random.randint(0,1):
                    new_game = Game(first,second)
                else:
                    new_game = Game(second, first)
                self.active_games.append(new_game)
                first.game = new_game
                second.game = new_game
                new_game.white_player.send_msg('GAME')
                new_game.white_player.send_msg('MSG You plays first')
                new_game.black_player.send_msg('GAME')
                new_game.black_player.send_msg('MSG Opponent plays first')
                to_delete.append((first, second))
        for pair in to_delete:
            self.ready_pairs.remove(pair)

    def run(self) -> None:
        while True:
            sleep(self.delay)
            self.find_pair()
            self.check_ready_pairs()
            for event2 in self.get_events2():
                if event2['type'] == 'select':
                    if event2['caller'].game:
                        event2['caller'].game.do_step(event2['caller'], event2['x'], event2['y'])
                elif event2['type'] == 'accept':
                    if event2['caller'].game == None:
                        event2['caller'].accepted = True
                    else:
                        event2['caller'].send_msg('MSG game already accepted')
                elif event2['type'] == 'disconnect':
                    self.disconnect(event2['caller'], event2['msg'])
##            print(get_date(), 'connected:', len(connected_clients),'waiting:',
##                  len(waiting_clients), 'playing:', len(playing_clients),'ready:', len(ready_clients))

    def get_events2(self):
        events2 = self.events2[:]
        self.events2 = []
        return events2
        
    def add_event2(self,event):
        self.events2.append(event)
            

def get_date() -> str:
    date = datetime.now()
    date_str = '[{0:0>2}-{1:0>2}-{2:0>4} {3:0>2}:{4:0>2}]'.format(date.day,
                                                                  date.month,
                                                                  date.year,
                                                                  date.hour,
                                                                  date.minute)
    return date_str


class ConnectedClient(Thread):

    def __init__(self, socket, address):
        Thread.__init__(self)
        self.address = address
        self.socket = socket
        self.xor_key = None
        self.name = 'User' + str(users)
        self.accepted = False
        self.blocked = False
        self.exceed_time = 10
        self.game = None


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
        
    def xor_crypt(self, string:bytes, key:bytes) -> bytes:
        key_len = len(key)
        fitted_key = bytes(key[index % key_len] for index in range(len(string)))
        crypto_str = bytes([string[index] ^ fitted_key[index] for index in range(len(string))])
        return crypto_str


    def get_msg(self):
        chunks = []
        bytes_recv = 0
        while bytes_recv < 512:
            chunk = self.socket.recv(min(512 - bytes_recv, 2048))
            if chunk == b'':
                return False
            chunks.append(chunk)
            bytes_recv = bytes_recv + len(chunk)
        return self.xor_crypt(b''.join(chunks), self.xor_key).decode('utf-8').strip()
            
    
    def send_msg(self, msg):
        msg = msg + ' ' * (512 - len(msg))
        msg = self.xor_crypt(msg.encode('utf-8'), self.xor_key)
        bytes_sent = 0
        while bytes_sent < 512:
            sent = self.socket.send(msg[bytes_sent:])
            if sent == 0:
                print('Socket connection broken')
                return False
            bytes_sent += sent 
        return True


    def run(self):
        self.socket.send(public.save_pkcs1())
        raw_xor_key = self.socket.recv(1024)
        self.xor_key = rsa.decrypt(raw_xor_key, private)
        print(get_date(),'secure key received from', self.address)
        waiting_clients.append(self)
        while True:
            client_data = self.get_msg()
            if not client_data:
                break
            data_words = client_data.split(' ')
            print(get_date(), 'get', client_data, 'from', self.address)
            if data_words[0] == 'SELECT':
                loop.add_event2({'type':'select',
                                 'x':int(data_words[1]),
                                 'y':int(data_words[2]),
                                 'caller':self
                                 }
                                )
            elif data_words[0] == 'ACCEPT':
                loop.add_event2({'type':'accept', 'caller':self})
            else:
                print(get_date(), 'can\'t recognize:',client_data, 'from', self.address)
                self.disconnect('Wrong data')
                break

class Game():

    def __init__(self, first_player, second_player):
        self.white_player  = first_player
        self.black_player = second_player
        self.white_step = True
        self.black_step = False
        self.white_check = False
        self.black_check = False
        self.white_checkmate = False
        self.black_checkmate = False
        self.white_selected_figure = [100,100]
        self.black_selected_figure = [100,100]
        self.field = [
                        ['r','h','b','q','k','b','h','r'],
                        ['p','p','p','p','p','p','p','p'],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        ['p','p','p','p','p','p','p','p'],
                        ['r','h','b','q','k','b','h','r'],
                    ]
        self.white_figures = [[j,i] for j in range(8) for i in range(6,8)]
        self.black_figures = [[j,i] for j in range(8) for i in range(2)]
        self.taken_by_white = {'p':0, 'r':0, 'b':0, 'h':0, 'q':0}
        self.taken_by_black = {'p':0, 'r':0, 'b':0, 'h':0, 'q':0}
        self.black_admissible = []
        self.white_admissible = []

    def do_step(self, player, x, y):
        print('step','white',self.white_step,'black',self.black_step)
        if (0 <= x <= 7) and (0 <= y <= 7):
            if player == self.white_player:
                if self.white_step:
                    if [x, y] in self.white_figures:
                        self.white_selected_figure = [x, y]
                        self.white_admissible = check_positions_white(self.white_selected_figure,
                                                                 self.white_figures,
                                                                 self.black_figures,
                                                                 self.field)
                        figure_type = self.field[y][x]
                        #self.white_admisisble = exclude_check_unprotected(figure_type)                                                   
                    elif [x, y] in self.black_figures and self.white_selected_figure:
                        if [x,y] in self.white_admissible:
                            self.take_figure(self.white_figures, self.black_figures, [x,y], self.white_selected_figure)
                            self.white_player.send_msg('TAKE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_player.send_msg('TAKE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.white_admissible = []
                        self.white_selected_figure = [100,100]
                    elif self.field[y][x] == ' ' and self.white_selected_figure:
                        if [x,y] in self.white_admissible:
                            self.move_figure(self.white_figures, [x,y], self.white_selected_figure)
                            self.white_player.send_msg('MOVE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_player.send_msg('MOVE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.white_admissible = []
                        self.white_selected_figure = [100,100]
                    else:
                        self.white_admissible = []
                        self.white_selected_figure = [100,100]
                    self.white_player.send_msg('ADMISSIBLE ' + json.dumps(self.white_admissible))
                    self.white_player.send_msg('LIGHT ' + json.dumps(self.white_selected_figure))
                else:
                    self.white_player.send_msg('ALERT not your step')
            else:
                if self.black_step:
                    if [x, y] in self.black_figures:
                        self.black_selected_figure = [x,y]
                        self.black_admissible = check_positions_black(self.black_selected_figure,
                                                                      self.black_figures,
                                                                      self.white_figures,
                                                                      self.field)
                        figure_type = self.field[y][x]
                    elif [x, y] in self.white_figures and self.black_selected_figure:
                        if [x, y] in self.black_admissible:
                            self.take_figure(self.black_figures, self.white_figures, [x,y], self.black_selected_figure)
                            self.white_player.send_msg('TAKE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_player.send_msg('TAKE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.black_admissible = []
                        self.black_selected_figure = [100,100]
                    elif self.field[y][x] == ' ' and self.black_selected_figure:
                        if [x, y] in self.black_admissible:
                            self.move_figure(self.black_figures, [x,y], self.black_selected_figure)
                            self.white_player.send_msg('MOVE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_player.send_msg('MOVE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.black_admissible = []
                        self.black_selected_figure = [100,100]
                    else:
                        self.black_admissible = []
                        self.black_selected_figure = [100,100]
                    self.black_player.send_msg('ADMISSIBLE ' + json.dumps(self.black_admissible))
                    self.black_player.send_msg('LIGHT ' + json.dumps(self.black_selected_figure))
##                    player.send_msg('MSG Opponent\'s step')
##                    self.white_player.send_msg('MSG Your step')
                else:
                    self.black_player.send_msg('ALERT not your step')

   
    def take_figure(self,player_figures, opponent_figures, new_pos, old_pos):
        opponent_figures.remove(new_pos)
        self.field[new_pos[1]][new_pos[0]] = self.field[old_pos[1]][old_pos[0]]
        self.field[old_pos[1]][old_pos[0]] = ' '
        player_figures[player_figures.index(old_pos)] = new_pos[:]
        print('figure taken')


    def move_figure(self,player_figures, new_pos, old_pos):
        print(self.field)
        self.field[new_pos[1]][new_pos[0]] = self.field[old_pos[1]][old_pos[0]]
        self.field[old_pos[1]][old_pos[0]] = ' '
        player_figures[player_figures.index(old_pos)] = new_pos[:]
        print(self.field)
        print('figure moved')

VERSION = '0.8'
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
active_games = []
users = 0
loop = EventLoop()
loop.start()
while True:
    server_sock.listen(0)
    sock,addr = server_sock.accept()
    new_client = ConnectedClient(sock,addr)
    connected_clients.append(new_client)
    new_client.start()
    users += 1
