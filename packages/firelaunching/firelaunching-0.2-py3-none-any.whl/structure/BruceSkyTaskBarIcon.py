#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'yuhaiyang'
__mtime__ = '2018/10/8'
"""
import wx
import wx.adv
from firelaunching import settings
import os


class BruceSkyTaskBarIcon(wx.adv.TaskBarIcon):
    ID_About = wx.NewId()  # 菜单选项“关于”的ID
    ID_Minshow = wx.NewId()  # 菜单选项“最小化”的ID
    ID_Maxshow = wx.NewId()  # 菜单选项“最大化”的ID
    ID_Closeshow = wx.NewId()  # 菜单选项“退出”的ID

    ICON = os.path.join(os.path.dirname(os.path.dirname(__file__)), settings.icon)  # 图标地址
    TITLE = settings.project_name  # 鼠标移动到图标上显示的文字

    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        frame.SetIcon(wx.Icon(self.ICON, wx.BITMAP_TYPE_ICO))  # 设置窗口左上角图标
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置系统托盘图标和标题

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)  # 定义左键双击
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnMinshow, id=self.ID_Minshow)
        self.Bind(wx.EVT_MENU, self.OnMaxshow, id=self.ID_Maxshow)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    # 鼠标左键单击托盘图标打开应用程序
    def OnTaskBarLeftClick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    # 关于
    def OnAbout(self, event):
        wx.MessageBox('程序作者：于海洋\n当前版本：1.0\n发布日期：2018-10-08', "关于")

    # 最小化应用程序
    def OnMinshow(self, event):
        self.frame.Iconize(True)

    # 最大化应用程序
    def OnMaxshow(self, event):
        # 最大化显示
        self.frame.Maximize(True)
        self.OnTaskBarLeftClick(event)

    # 关闭应用程序
    def OnCloseshow(self, event):
        self.frame.Close(True)

    # 右键菜单
    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_Minshow, '最小化')
        menu.Append(self.ID_Maxshow, '最大化')
        menu.Append(self.ID_About, '关于')
        menu.Append(self.ID_Closeshow, '退出')
        return menu
