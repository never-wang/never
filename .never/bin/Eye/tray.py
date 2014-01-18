#!/usr/bin/env python
# -�~- coding: utf-8 -�~-
#########################################################################
# Author: Wang Wencan
# Created Time: Wed 25 Sep 2013 09:26:22 AM CST # File Name: tray.py
# Description: 
#########################################################################
import platform
if platform.system() == 'Windows':
    import wx
elif platform.system() == 'Linux':
    import gtk
    import appindicator
import os

CONFIG_ACCEPT_MSG = "设置修改后需要重新启动程序后方能生效"

class Tray():
    config_window_width = 300
    config_window_height = 300
    def __init__(self, view):
        self.view = view
        self.state = view.state
        self.itemlist = [(1, '状态', self.menu_status),
                         (2, '休息', self.menu_rest),
                         (3, "设置", self.menu_config),
                         (4, '退出', self.menu_quit)]
    
    def menu_rest(self, event):
        self.view.start_rest(event)

class WindowsTray(Tray):
    def __init__(self, view):
        Tray.__init__(self, view)

        self.tray = wx.TaskBarIcon()
        self.tray.SetIcon(wx.Icon(os.path.os.path.join(os.path.dirname(__file__), "eye.gif"),  wx.BITMAP_TYPE_GIF)) 
        self.tray.Bind(wx.EVT_TASKBAR_CLICK, self.popup_menu)
    
    def popup_menu(self, event):
        menu = self.make_menu()
        self.tray.PopupMenu(menu)
            
    def make_menu(self):
        menu = wx.Menu()
        for id, text, callback in self.itemlist:
            item = menu.Append(id, text)
            menu.Bind(wx.EVT_MENU, callback, id = id)
        return menu
    
    def menu_status(self, event):
        status = self.state.get_status()
        dialog = wx.MessageDialog(None, status, style=wx.OK|wx.CENTRE)
        dialog.ShowModal()
    
    def menu_config(self, event):
        '''user config the Eye by a window, the config will be stored in config file too'''
        self.config_frame = wx.Frame(None, 
                size = (self.config_window_width, self.config_window_height), title = '设置',
                style = wx.DEFAULT_FRAME_STYLE & (~ wx.RESIZE_BORDER) & (~ wx.MAXIMIZE_BOX))
        self.config_frame.SetBackgroundColour(wx.ColourDatabase().Find("WHITE"))
        self.config_frame.Centre()
        self.config_frame.Show()
        frame_width, frame_height = self.config_frame.GetSize()
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.config_frame.SetSizer(box)

        self.config_text = wx.TextCtrl(self.config_frame, style = wx.TE_MULTILINE)
        text = self.view.config.text()
        if text != None:
            self.config_text.WriteText(text)
        box.Add(self.config_text, 1, wx.EXPAND | wx.ALL, 0)
        
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(button_box, 0)

        accept_button = wx.Button(self.config_frame, label = '确定')
        accept_button_width, accept_button_height = accept_button.GetSize()
        accept_button.Bind(wx.EVT_BUTTON, self.config_accept)
        button_box.Add(accept_button, 0, wx.LEFT, frame_width / 2 - accept_button_width - 5)
        cancel_button = wx.Button(self.config_frame, label = '取消')
        cancel_button_width, cancel_button_height = accept_button.GetSize()
        cancel_button.Bind(wx.EVT_BUTTON, self.config_cancel)
        button_box.Add(cancel_button, 0, wx.RIGHT, frame_width / 2 - cancel_button_width - 5)
        self.config_frame.Layout()       

    def menu_quit(self, event):
        self.view.frame.Close()
        self.tray.Destroy()
        self.state.quit()
    
    def config_accept(self, event):
        text = self.config_text.GetValue()
        self.view.config.set_text(text)
        self.config_frame.Close()
        
        dialog = wx.MessageDialog(None, CONFIG_ACCEPT_MSG, style=wx.OK|wx.CENTRE)
        dialog.ShowModal()
        
        del self.config_frame
        del self.config_text

    def config_cancel(self, event):
        self.config_frame.Close()
        del self.config_frame
        del self.config_text

class LinuxTray(Tray):
    def __init__(self, view):
        Tray.__init__(self, view)

        self.tray = appindicator.Indicator('Eye', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
        self.tray.set_status(appindicator.STATUS_ACTIVE)
        self.tray.set_icon(os.path.join(os.path.abspath(os.path.dirname(__file__)), "eye.gif"))
        self.tray.set_attention_icon('indicator-messages-new')
        self.tray.set_menu(self.make_menu())

    def make_menu(self):
        menu = gtk.Menu()
        for id, text, callback in self.itemlist:
            item = gtk.MenuItem(text)
            item.connect('activate', callback)
            item.show()
            menu.append(item)
        menu.show()
        return menu
    
    def menu_status(self, event):
        status = self.state.get_status()
        dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, 
                buttons = gtk.BUTTONS_OK,
                message_format = status)
        dialog.run()
        dialog.destroy()
    
    def menu_config(self, event):
        '''user config the Eye by a window, the config will be stored in config file too'''
        self.config_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.config_window.set_size_request(
                self.config_window_width,
                self.config_window_height)
        self.config_window.set_resizable(True)
        self.config_window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.config_window.set_resizable(False)

        box = gtk.VBox(False, 0)
        self.config_window.add(box)

        text_buffer=gtk.TextBuffer()
        text_buffer.set_text(self.view.config.text())

        self.text_view = gtk.TextView(text_buffer)
        box.pack_start(self.text_view)

        button_table = gtk.Table(rows = 1, columns = 4, homogeneous = True)
        box.pack_start(button_table, False, False, 0)

        accept_button = gtk.Button(label = '确定')
        button_table.attach(accept_button, 1, 2, 0, 1)
        accept_button.connect('clicked', self.config_accept)
        
        cancel_button = gtk.Button(label = '取消')
        button_table.attach(cancel_button, 2, 3, 0, 1)
        cancel_button.connect('clicked', self.config_cancel)
        
        self.config_window.show_all()

    def config_accept(self, event):
        text_buffer = self.text_view.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(),
                text_buffer.get_end_iter())
        self.view.config.set_text(text)
        self.config_window.hide_all()
        dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, 
                buttons = gtk.BUTTONS_OK,
                message_format = CONFIG_ACCEPT_MSG)
        dialog.run()
        dialog.destroy()
        del self.config_window
        del self.text_view

    def config_cancel(self, event):
        self.config_window.hide_all()
        del self.config_window
        del self.text_view


    def menu_quit(self, event):
        gtk.main_quit()
        self.state.quit()
        
