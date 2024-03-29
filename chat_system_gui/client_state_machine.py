"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import game_tic_tac_toe as game

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.my_image = []
        self.peer_image = []
        #self.game_state = False

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def game_connect_to(self,peer):
        msg = json.dumps({"action": "game_connect", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
        #self.peer_image = []
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                
                elif my_msg[0]=="g":
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.game_connect_to(peer) == True:
                        self.state = S_GAMING
                        
                        self.game_role = 'x'
                        self.out_msg += 'Connect to ' + peer + '. Play the game!\n\n'
                        self.out_msg += '-----------------------------------\n'
                        self.out_msg+="Rules of Tic Tac Toe 2.0\n"
                        self.out_msg+="1.The conditions of victory are the same as\n"
                        self.out_msg+="   ordinary tic-tac-toe\n"
                        self.out_msg+="2.Each player has three types of pieces:\n"
                        self.out_msg+="   small, medium and big\n"
                        self.out_msg+="3.Each type has 3 pieces.\n"
                        self.out_msg+="4.Medium type can cover any small type of piece.\n"
                        self.out_msg+="5.Big type can cover any small or medium type.\n"
                        self.out_msg+="   Big type can not be covered.\n\n"
                        #game.main(self.game_role,self.me,socket=self.s)
                        game.main(self,socket=self.s)
                        #return [self.out_msg]
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

                if peer_msg["action"] == "game_connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Game request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Play the game!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.out_msg+="Rules of Tic Tac Toe 2.0\n"
                    self.out_msg+="1.The conditions of victory are the same as\n"
                    self.out_msg+="   ordinary tic-tac-toe\n"
                    self.out_msg+="2.Each player has three types of pieces:\n"
                    self.out_msg+="   small, medium and big\n"
                    self.out_msg+="3.Each type has 3 pieces.\n"
                    self.out_msg+="4.Medium type can cover any small type of piece.\n"
                    self.out_msg+="5.Big type can cover any small or medium type.\n"
                    self.out_msg+="   Big type can not be covered.\n\n"
                    #self.game_state = True
                    self.state = S_GAMING
                    self.game_role = 'o'
                    #game.main(self.game_role,self.me,socket=self.s)
                    game.main(self,socket=self.s)
                    #return [self.out_msg]

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                #self.my_image = ''
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg, "image":self.my_image}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                self.peer_image = []
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                #image, might be redundant
                #elif peer_msg["action"] == "image":
                    #self.out_msg += peer_msg["from"] + peer_msg["message"]
                
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]
                    #image
                    if len(peer_msg["image"]) > 0:
                        self.peer_image = peer_msg["image"]

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        elif self.state==S_GAMING: #not used, don't proc as game running
            pass
            #self.state = S_LOGGEDIN
            #if len(my_msg) > 0:     # my stuff going out
                #self.my_image = ''
                #mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg, "image":self.my_image}))
                #if my_msg == 'bye':
                    #self.disconnect()
                    #self.state = S_LOGGEDIN
                    #self.peer = ''
                    #game.quit()
                    #self.out_msg += 'Game end.\n'
                #else:
                    #game.main(self.game_role,self.me,socket=self.s)
            #if len(peer_msg) > 0:    # peer's stuff, coming in
                #self.peer_image = []
                #peer_msg = json.loads(peer_msg)
                #if peer_msg["action"] == "game_connect":
                    #self.out_msg += "(" + peer_msg["from"] + " joined to play)\n"
                #elif peer_msg["action"] == "disconnect":
                    #self.state = S_LOGGEDIN
                    #game.quit()
                    #self.out_msg += 'Game end.\n'
            
            
            
            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
