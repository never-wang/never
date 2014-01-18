# -�~- coding: utf-8 -�~-

import ConfigParser
import datetime
import os
import state

class Config:
    def __init__(self, config_filename):
        self.config_filename = os.path.os.path.join(os.path.dirname(__file__), config_filename)
        defaults = {'rest_time' : '10', 'work_time' : '50', 
                'image_file' : 'rei.jpg', 'time_unit' : 'min',
                'role' : 'server', 'port' : '8888', 
                'server' : 'never.local', 'timeout' : '5'}
        self.config = ConfigParser.ConfigParser(defaults)
        self.config.add_section('General')
        self.config.add_section('Server')
        self.config.add_section('Client') 
        try:
            self.config.read(self.config_filename)
        except:
            pass
        
    def rest_time(self):
        rest_time = self.config.getint('General', 'rest_time')
        if self.time_unit() == 'hour':
            return datetime.timedelta(hours = rest_time)
        elif self.time_unit() == 'min':    
            return datetime.timedelta(minutes = rest_time)
        else: 
            '''sec or other'''
            return datetime.timedelta(seconds = rest_time)

    def work_time(self):
        work_time = self.config.getint('General', 'work_time')
        if self.time_unit() == 'hour':
            return datetime.timedelta(hours = work_time)
        elif self.time_unit() == 'min':    
            return datetime.timedelta(minutes = work_time)
        else: 
            '''sec or other'''
            return datetime.timedelta(seconds = work_time)
    
    def image_file(self):
        image_file = self.config.get('General', 'image_file')
        if os.path.isabs(image_file):
            return image_file
        else:
            prefix = os.path.dirname(__file__)
            return os.path.join(prefix, image_file)
    
    def time_unit(self):
        return self.config.get('General', 'time_unit')

    def text(self):
        try :
            file = open(self.config_filename, 'r')
            text = file.read()
            file.close()
            return text
        except :
            return None
        
    def set_text(self, text):
        file = open(self.config_filename, 'w')
        file.write(text)
        file.close()
        try :
            self.config.read(self.config_filename)
        except :
            pass
        
    def role(self):
        role = self.config.get('General', 'role')
        if role == 'server':
            return state.SERVER_ROLE
        elif role == 'client':
            return state.CLIENT_ROLE
        else:
            print "Unknow role"
            
    def port(self):
        if self.role() == state.SERVER_ROLE:
            return self.config.getint('Server', 'port')
        elif self.role() == state.CLIENT_ROLE:
            return self.config.getint('Client', 'port')
        else:
            print "Impossible here"
            
    def server_address(self):
        if self.role() == state.CLIENT_ROLE:
            return (self.config.get('Client', 'server'), self.port())
        else:
            print "Impossible here"
            
    def timeout(self):
        if self.role() == state.CLIENT_ROLE:
            return self.config.getint('Client', 'timeout')
        else:
            print "Impossible here"

if __name__ == "__main__":
    config = Config("eye.ini")
    print config.get_rest_time()
    #print config.get_work_time()
    print config.get_image_file()
    config.set_from_window()
    gtk.main()
