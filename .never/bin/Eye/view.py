# -�~- coding: utf-8 -�~-
'''
Created on 2013年9月30日

@author: never
'''
import platform
if platform.system() == 'Windows':
    import wx
elif platform.system() == 'Linux':
    import gtk
    import gobject

import ctypes
import config
import eye
import tray
import state

class View():
    work_text = 'Start Work !'
    time_font_size = 25
    work_font_size = 30
    standard_width = 1024

    def __init__(self, eye, monitor_width): 
        self.config = eye.config
        self.state = eye.state
        self.state.view = self
        
        self.work_font_size = self.work_font_size * monitor_width / self.standard_width
        self.time_font_size = self.time_font_size * monitor_width / self.standard_width

    def start_work(self, event):
        self.state.set_state(state.WORK_STATE)
        self.set_view()
    
    def start_rest(self, event):
        self.state.set_state(state.REST_STATE)
        self.set_view()
        
    def run(self):
        self.set_view()
        self.set_time()

class WindowsView(View):
    '''the WindwsView is implemented by wxpython'''
    
    def __init__(self, eye):
        monitor_width = ctypes.windll.user32.GetSystemMetrics(0)
        monitor_height = ctypes.windll.user32.GetSystemMetrics(1)
        
        View.__init__(self, eye, monitor_width)

        self.app = wx.App(False)
        
        self.frame = wx.Frame(None, 
                size = (monitor_width, monitor_height))
        self.frame.Bind(wx.EVT_ERASE_BACKGROUND, 
                self.erase_background)
        self.frame.ShowFullScreen(True)
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.frame.SetSizer(box)
        
        self.time = wx.StaticText(self.frame)
        font = wx.Font(self.time_font_size, wx.FONTFAMILY_DEFAULT, 
                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.time.SetFont(font)
        self.time.SetBackgroundColour(
                wx.ColourDatabase().Find("WHITE"))
        time_width, time_height = self.time.GetSize()
        time_border = 20
        box.Add(self.time, 0, wx.TOP | wx.CENTER, 20)
        
        self.work = wx.Button(self.frame, label = self.work_text)
        font = wx.Font(self.work_font_size, wx.FONTFAMILY_DEFAULT, 
                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.work.SetFont(font)
        button_width, button_height = self.work.GetSize() 
        box.Add(self.work, 0, wx. wx.TOP | wx.CENTRE , 
                monitor_height / 2 - button_height / 2 - time_height - time_border)
        self.work.Bind(wx.EVT_BUTTON, self.start_work)
        
        self.tray = tray.WindowsTray(self)     

    def run(self):
        View.run(self)
        self.app.MainLoop()
        
    def erase_background(self, event):
        dc = event.GetDC()
        dc.Clear()
        
        width, height = self.frame.GetSize()
        image = wx.Image(self.config.image_file(), type = wx.BITMAP_TYPE_ANY)
        image_width, image_height = image.GetSize()
        '''resize image'''
        ratio = max(1.0 * width / image_width, 1.0 * height / image_height)
        image.Rescale(int(image_width * ratio), int(image_height * ratio))
        image_width, image_height = image.GetSize()
        bitmap = wx.BitmapFromImage(image)
        dc.DrawBitmap(bitmap, 0, 0)
    
    def set_time(self):
        self.time.SetLabel(self.state.get_time())
        self.frame.Layout()
        
    def set_view(self):
        cur_state = self.state.get_state()
        
        if cur_state == state.WAIT_WORK_STATE:
            self.work.Show(True)
            self.frame.Show(True)
        elif cur_state == state.WORK_STATE:
            self.work.Show(False)
            self.frame.Show(False)
        elif cur_state == state.REST_STATE:
            self.work.Show(False)
            self.frame.Show(True) 
        else:
            print 'Unkown Eye State'
        self.set_time()
        self.frame.Layout()

class LinuxView(View):
    '''the WindwsView is implemented by wxpython'''
    
    def __init__(self, eye):
        monitor_width = gtk.gdk.screen_width()
        monitor_height = gtk.gdk.screen_height()

        View.__init__(self, eye, monitor_width)
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)
        self.window.set_resizable(True)
        self.window.fullscreen()
        self.window.connect("destroy", gtk.main_quit)
        self.window.show()

        self.fixed = gtk.Fixed()
        self.window.add(self.fixed)
        self.fixed.show()

        self.image = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.config.image_file())
        image_width = pixbuf.get_width()
        image_height = pixbuf.get_height()
        ratio = max(1.0 * monitor_width / image_width, 
                1.0 * monitor_height / image_height)
        pixbuf = pixbuf.scale_simple(int(image_width * ratio), 
                int(image_height * ratio), gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pixbuf)
        self.fixed.put(self.image, 0, 0)
        self.image.show()

        self.time = gtk.Label()
        self.set_time()
        #set time here so that the size_request can get perfect size
        width, height = self.time.size_request()
        self.fixed.put(self.time, monitor_width / 2 - width / 2, 10)
        self.time.show()
        
        self.work = gtk.Button("")
        label = self.work.get_child()
        label.set_markup('<span size="48000">' + self.work_text + '</span>')
        self.work.connect('clicked', self.start_work)
        width, height = self.work.size_request()
        self.fixed.put(self.work, monitor_width / 2 - 
                width / 2, monitor_height / 2 - height / 2)
        self.work.show()
       
        self.tray = tray.LinuxTray(self)     

    def run(self):
        View.run(self)
        gobject.threads_init()
        gtk.main()
    
    def set_time(self):
        self.time.set_markup(
                '<span background="white" size="' + 
                str(self.time_font_size * 1000) + '">' + 
                self.state.get_time() + '</span>')
   
    def set_view(self):
        cur_state = self.state.get_state()
        if cur_state == state.WAIT_WORK_STATE:
            self.work.show()
            self.window.show_all()
        elif cur_state == state.WORK_STATE:
            self.work.hide()
            self.window.hide_all()
        elif cur_state == state.REST_STATE:
            self.window.show_all()
            self.work.hide()
        else:
            print 'Unkown Eye State :', cur_state
        self.set_time()
