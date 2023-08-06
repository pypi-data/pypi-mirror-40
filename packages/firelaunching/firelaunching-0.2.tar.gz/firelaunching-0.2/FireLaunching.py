#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'yuhaiyang'
__mtime__ = '2018/10/8'
"""
import wx
from structure.BruceSkyMainFrame import BruceSkyMainFrame


class BruceSkyApp(wx.App):

    def __init__(self):
        wx.App.__init__(self, redirect=False, filename='output')

    def OnInit(self):
        self.frame = BruceSkyMainFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


def main():
    app = BruceSkyApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
