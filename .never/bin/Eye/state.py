# -�~- coding: utf-8 -�~-
'''
Created on 2013年10月1日

@author: never
'''
import thread
import datetime
import SocketServer
import threading
import socket
import config

SERVER_ROLE = 'SERVER'
CLIENT_ROLE = 'CLIENT'

WORK_STATE = 'WORK'
REST_STATE = "REST"
WAIT_WORK_STATE = 'WAIT_WORK'

TIME_IDENT = 'TIME'
STATE_IDENT = 'STATE'

INIT_TIME = "00:00:00:00"

class State():
    def __init__(self, eye):
        self.config = eye.config
        self.cur_state = WAIT_WORK_STATE
        self.start_time = datetime.datetime.now()
        self.timer = None
            
    def update_state(self):
        cur_time = datetime.datetime.now()
        time_delta = cur_time - self.start_time 
        print time_delta, self.cur_state
        
        if self.cur_state == REST_STATE:
            if time_delta > self.config.rest_time() :
                self.set_state(WAIT_WORK_STATE)
                self.view.set_view()
        elif self.cur_state == WORK_STATE:
            if time_delta > self.config.work_time() : 
                self.set_state(REST_STATE)
                self.view.set_view()
        self.view.set_time()
            
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
        
        self.timer = threading.Timer(1, self.update_state)
        self.timer.start()

    def quit(self):
        if self.timer != None:
            self.timer.cancel()

    def get_state(self):
        return self.cur_state
    
    def get_time(self):
        time_delta = datetime.datetime.now() - self.start_time
        day = str(time_delta.days)
        hour = str(time_delta.seconds // 3600)
        min = str((time_delta.seconds // 60) % 60) 
        sec = str(time_delta.seconds % 60)
        return (day.rjust(2, '0') + ":" + hour.rjust(2, '0') + ":"  + min.rjust(2, '0')+ 
                ":" + sec.rjust(2, '0'))
        
    def set_state(self, state):     
        self.cur_state = state
        self.start_time = datetime.datetime.now()
        
    def get_status(self):
        return self.cur_state + " : " + self.get_time()
        
class StateServer(SocketServer.TCPServer):
    def __init__(self, addr, handler, state):
        SocketServer.TCPServer.__init__(self, addr, handler)
        self.state = state
        
class ServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        state = self.server.state
        condition = self.server.state.condition
       
        while True:
            condition.acquire()
            condition.wait()
            condition.release()
            self.request.send(state.get_state())
            self.request.send(state.get_time())
        
class ServerState(State):
    def __init__(self, eye):
        State.__init__(self, eye)
        self.condition = threading.Condition()
        thread.start_new_thread(self.start_server, ())
        self.shadow = False
       # self.start_server()
        
    def start_server(self):
        server = StateServer(("", self.config.port()), ServerHandler, self)
        server.serve_forever()
        
    def update_state(self):
        return State.update_state(self)
        
    def get_time(self):
        return State.get_time(self)

class ClientState(State):
    def __init__(self, eye):
        State.__init__(self, eye)
        try:
            print self.config.server_address()
            self.socket = socket.create_connection(address = self.config.server_address(), 
                                               timeout = self.config.timeout())
            print "Connected with server"
            self.shadow = True
            self.time = INIT_TIME
        except:
            print "Can't connect with server"
            self.socket = None
            self.shadow = False
    
    def set_state(self, state):
        if self.shadow:
            pass
        else:
            State.set_state(self, state)
            
    def update_state_from_server(self):
        while True:
            state = self.socket.recv(1024)
            self.time = self.socket.recv(1024)
            print self.time, state
            if state != self.cur_state:
                self.cur_state = state
                self.view.set_view()
            self.view.set_time()
    
    def update_state(self):
        if self.shadow:       
            thread.start_new_thread(self.update_state_from_server, ())    
        else:
            State.update_state(self)
            
    def get_time(self):
        if self.shadow:
            return self.time
        else:
            return State.get_time(self)
        
