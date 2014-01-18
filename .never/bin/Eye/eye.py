#!/usr/bin/env python
from config import *
import state
import platform
import view

CONFIG_FILENAME = 'config.ini'

class Eye():
    def __init__(self):
        print "fuck"
        self.config = Config(CONFIG_FILENAME)
        
        if self.config.role() == state.SERVER_ROLE:
            self.state = state.ServerState(self)
        elif self.config.role() == state.CLIENT_ROLE:
            self.state = state.ClientState(self)
        else:
            print "Impossible here"
        
        if platform.system() == 'Windows':
            self.view = view.WindowsView(self)
        elif platform.system() == 'Linux':
            self.view = view.LinuxView(self)
        else :
            exit
        
        self.view.state = self.state
        self.state.update_state()
        self.view.run()

if __name__ == '__main__':
    eye = Eye()
        
