#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'yuhaiyang'
__mtime__ = '2018/10/8'
"""
import wx
import os
import chardet
import time
import datetime
import threading
import queue
from firelaunching import settings
# from structure.BruceSkyMainPanel import MonitorPanelBase
from structure.BruceSkyTaskBarIcon import BruceSkyTaskBarIcon
from utils import Utils
from utils import Launcher


class BruceSkyMainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, None, -1, title=u'BruceSky', size=(900, 580), style=wx.DEFAULT_FRAME_STYLE)
        self.taskBarIcon = BruceSkyTaskBarIcon(self)
        self.StatusBar()
        # 绑定关闭事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        # 窗口最小化时，调用OnIconfiy,注意Wx窗体上的最小化按钮，触发的事件是 wx.EVT_ICONIZE,
        # 而根本就没有定义什么wx.EVT_MINIMIZE,但是最大化，有个wx.EVT_MAXIMIZE。

        # 框架初始化完成，以下内容为各组件的布置

        panel = wx.Panel(self)
        self.InitUI(panel)

    def InitUI(self, panel):
        self.MainPanelBoxSizer = wx.BoxSizer(wx.HORIZONTAL)  # 主面板的横向布局管理器
        self.LeftPanel = wx.Panel(self, -1)
        # self.MiddlePanel = MonitorPanelBase(self)
        self.MiddlePanel = wx.Panel(self)
        self.RightPanel = wx.Panel(self, -1)

        self.BuildLeftPanel()
        self.TextBInput = wx.TextCtrl(self.MiddlePanel, -1, "日志输出监控", size=(600, 500),
                                      style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.HSCROLL)  # 创建丰富文本控件
        vboxnet_b = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        vboxnet_b.Add(self.TextBInput, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        self.MiddlePanel.SetSizer(vboxnet_b)
        self.BuildRightPanel()

        # 在主面板布局管理器中放置panel组件
        self.MainPanelBoxSizer.Add(self.LeftPanel, proportion=0, border=1, flag=wx.ALL | wx.EXPAND)
        self.MainPanelBoxSizer.Add(self.MiddlePanel, proportion=1, border=1, flag=wx.ALL | wx.EXPAND)
        self.MainPanelBoxSizer.Add(self.RightPanel, proportion=0, border=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.MainPanelBoxSizer)
        self.MainPanelBoxSizer.Fit(self)
        self.MainPanelBoxSizer.SetSizeHints(self)
        # iRet = wx.PostEvent(self, wx.CommandEvent(wx.EVT_BUTTON.typeId, self.Button3.GetId()))
        self.status = 0
        self.protocol = 'UDP'
        self.run_type = '循环执行'

    def BuildLeftPanel(self):

        paraInput_Box = wx.StaticBox(self.LeftPanel, -1, u'配置参数')
        paraInput_Sizer = wx.StaticBoxSizer(paraInput_Box, wx.VERTICAL)

        stockCode_Text = wx.StaticText(self.LeftPanel, -1, u'传输协议')
        self.IndicatInput_Box1 = wx.Choice(self.LeftPanel, -1, choices=settings.protocol)
        self.IndicatInput_Box1.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.OnChoiceChange, self.IndicatInput_Box1)
        paraInput_Sizer.Add(stockCode_Text, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        paraInput_Sizer.Add(self.IndicatInput_Box1, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,
                            border=5)

        ip_port = wx.StaticText(self.LeftPanel, -1, u'IP与端口')
        # 创建一个水平BoxSizer放置多个标签，作为infoSizer的第二列的值
        ip_portSizer = wx.BoxSizer(wx.HORIZONTAL)
        # 创建路径框，Browser按钮 和 编辑按钮
        self.ip_value = wx.TextCtrl(self.LeftPanel, -1, Utils.get_host_ip(), size=(50, 27))
        self.ip_value.SetBackgroundColour('#E1E1E1')
        port_label = wx.StaticText(self.LeftPanel, -1, u":", size=(10, 27))
        # port_label.SetBackgroundColour('#E1E1E1')
        self.port_value = wx.TextCtrl(self.LeftPanel, -1, u'515', size=(50, 27))
        self.port_value.SetBackgroundColour('#E1E1E1')
        # 将组件放置到fileSizer中
        ip_portSizer.Add(self.ip_value, 1)
        ip_portSizer.Add(port_label, 0, wx.LEFT | wx.RIGHT, 5)
        ip_portSizer.Add(self.port_value)
        paraInput_Sizer.Add(ip_port, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        paraInput_Sizer.Add(ip_portSizer, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

        stockData_Text = wx.StaticText(self.LeftPanel, -1, u'时间间隔(毫秒)')
        self.IndicatInput_Box2 = wx.TextCtrl(self.LeftPanel, -1, u'1000', pos=(80, 25), size=(80, -1))
        self.IndicatInput_Box2.SetBackgroundColour('#E1E1E1')
        paraInput_Sizer.Add(stockData_Text, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        paraInput_Sizer.Add(self.IndicatInput_Box2, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,
                            border=5)

        stock_Text = wx.StaticText(self.LeftPanel, -1, u'日志文件')
        # 创建一个水平BoxSizer放置多个标签，作为infoSizer的第二列的值
        fileSizer = wx.BoxSizer(wx.HORIZONTAL)
        # 创建路径框，Browser按钮 和 编辑按钮
        self.file_value = wx.TextCtrl(self.LeftPanel, -1, "请选择文件...", size=(70, 27))
        self.file_value.SetBackgroundColour('#E1E1E1')
        select_file = wx.Button(self.LeftPanel, -1, "浏览", size=(50, 27))
        edit_file = wx.Button(self.LeftPanel, -1, "编辑", size=(50, 27))
        # 将组件放置到fileSizer中
        fileSizer.Add(self.file_value, 1)
        fileSizer.Add(select_file, 0, wx.LEFT | wx.RIGHT, 5)
        fileSizer.Add(edit_file)

        paraInput_Sizer.Add(stock_Text, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        paraInput_Sizer.Add(fileSizer, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

        self.Bind(wx.EVT_BUTTON, self.OnSelectFile, select_file)
        self.Bind(wx.EVT_BUTTON, self.OnEdit, edit_file)

        paraInput_Box1 = wx.StaticBox(self.LeftPanel, -1, u'执行方式')
        paraInput_Sizer1 = wx.StaticBoxSizer(paraInput_Box1, wx.VERTICAL)
        self.check1 = wx.RadioButton(self.LeftPanel, -1, "循环执行", pos=(50, 20), size=(50, 20), style=wx.RB_GROUP)
        self.check2 = wx.RadioButton(self.LeftPanel, -1, "自定义(次)", pos=(100, 20), size=(75, 20))
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRunTypeChange, self.check1)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRunTypeChange, self.check2)
        check_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.custom_value = wx.TextCtrl(self.LeftPanel, -1, u"1", size=(30, 20))
        check_box_sizer.Add(self.check2, 0, wx.EXPAND | wx.ALL, 0)
        check_box_sizer.Add(self.custom_value, 1, wx.EXPAND | wx.ALL, 10)
        paraInput_Sizer1.Add(self.check1, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        paraInput_Sizer1.Add(check_box_sizer, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        self.TextAInput = wx.TextCtrl(self.LeftPanel, -1, "当前实时效率为：0条/秒", size=(150, 150),
                                      style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.HSCROLL)  # 创建丰富文本控件
        vboxnetA = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        vboxnetA.Add(paraInput_Sizer, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        vboxnetA.Add(paraInput_Sizer1, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        vboxnetA.Add(self.TextAInput, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        self.LeftPanel.SetSizer(vboxnetA)

    def BuildRightPanel(self):
        # 右侧Panel组件添加
        self.FlexGridSizer = wx.FlexGridSizer(rows=4, cols=1, vgap=3, hgap=3)
        self.Button1 = wx.Button(self.RightPanel, -1, "开始")
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.Button1)
        self.Button2 = wx.Button(self.RightPanel, -1, "停止")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Button2)
        self.Button3 = wx.Button(self.RightPanel, -1, "重置")
        self.Bind(wx.EVT_BUTTON, self.Button2Event, self.Button3)
        self.Button4 = wx.Button(self.RightPanel, -1, "关于")
        self.Bind(wx.EVT_BUTTON, self.OnAbout, self.Button4)

        self.FlexGridSizer.Add(self.Button1, proportion=0, border=5, flag=wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button2, proportion=0, border=5, flag=wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button3, proportion=0, border=5, flag=wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button4, proportion=0, border=5, flag=wx.ALL | wx.EXPAND)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)
        self.RightPanel.SetSizer(self.FlexGridSizer)

    def OnSelectFile(self, event):
        file_wildcard = "All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "选择数据文件", os.getcwd(), style=wx.ID_OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_value.SetValue(dlg.GetPath())
        dlg.Destroy()

    def OnEdit(self, event):
        path = self.file_value.GetValue()
        if not os.path.exists(path):
            wx.MessageBox("请选择正确的文件路径")
            return
        os.startfile(path)

    def OnStart(self, event):

        if self.status == 0:
            self.status = 1  # 标识为启动状态
            # 开启一个线程
            t = threading.Thread(target=self.sendMessage)
            t.start()
        else:
            wx.MessageBox("已经启动任务，暂不支持开启多线程", "操作提示")

    def OnCancel(self, event):
        self.status = 0

    def OnChoiceChange(self, event):
        index = event.GetEventObject().GetSelection()
        self.protocol = settings.protocol[index]

    # 刷新面板，暂时未使用
    def Button1Event(self, event):
        # 创建选项栏目面板
        self.OptionPanel = wx.Panel(self)
        self.MainPanelBoxSizer.Hide(self.MiddlePanel)
        self.MainPanelBoxSizer.Replace(self.MiddlePanel, self.OptionPanel)
        self.SetSizer(self.MainPanelBoxSizer)
        self.MainPanelBoxSizer.Layout()
        # self.ProcessPanelB()

    # 重绘折线图
    def Button2Event(self, event):
        # self.MiddlePanel.cla()  # 必须清理图形,才能显示下一幅图
        # x = [x for x in range(30)]
        # import random
        # y = [random.random() * 100 for x in range(30)]
        # self.MiddlePanel.plot(x, y, '--*g')
        # self.MiddlePanel.xticker(1.0, 1.0)
        # self.MiddlePanel.yticker(10, 10)
        # self.MiddlePanel.title_MPL("RealTime Monitoring Of Transmission Efficiency")
        # # self.MiddlePanel.ShowHelpString("You Can Show MPL1 Helpful String Here !")
        # self.MiddlePanel.grid()
        # self.MiddlePanel.UpdatePlot()  # 必须刷新才能显示
        self.TextAInput.Clear()
        self.TextBInput.Clear()

    def OnRunTypeChange(self, event):
        self.run_type = event.GetEventObject().GetLabel()

    # 自动创建状态栏
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -2, -1])

    # 关于
    def OnAbout(self, event):
        wx.MessageBox('程序作者：于海洋\n当前版本：1.0\n最后更新日期：2018-10-08', "关于")

    # 右上角关闭事件
    def OnClose(self, event):
        dlg = wx.MessageDialog(None, '您确定要退出应用程序吗 ?', '退出应用程序', wx.YES_NO | wx.ICON_QUESTION)
        retCode = dlg.ShowModal()
        if retCode == wx.ID_YES:
            self.taskBarIcon.Destroy()
            self.Destroy()

    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()

    def sendMessage(self):
        try:
            if not os.path.exists(self.file_value.GetValue()):
                wx.MessageBox("文件不存在", "异常提示")
                self.status = 0
                return
            f = open(self.file_value.GetValue(), 'rb')
            # 判断具体的协议，进行选择发送方式
            if self.protocol == 'UDP':
                self.udp_send(f)
            elif self.protocol == 'TCP':
                self.tcp_send(f)
            elif self.protocol == 'Trap V1':
                self.status = 0
                wx.MessageBox("暂不支持该功能，敬请期待！", "温馨提示")
            elif self.protocol == 'Trap V2':
                self.status = 0
                wx.MessageBox("暂不支持该功能，敬请期待！", "温馨提示")
            else:
                self.status = 0
                wx.MessageBox("暂不支持该功能，敬请期待！", "温馨提示")
        except Exception as e:
            self.status = 0
            wx.MessageBox(str(e), "异常提示")

    def tcp_send(self, f):
        tcp = Launcher.tcp_socket()
        tcp.connect((self.ip_value.GetValue(), int(self.port_value.GetValue())))
        self.send(tcp, f)

    def udp_send(self, f):
        udp = Launcher.udp_socket()
        udp.connect((self.ip_value.GetValue(), int(self.port_value.GetValue())))
        self.send(udp, f)

    def monitor(self, q):
        while True:
            if self.status == 0:
                break
            else:
                string = q.get()
                self.TextBInput.SetValue(
                    "\n".join(self.TextBInput.GetValue().strip().split('\n')[
                              -21::]) + "\n" + datetime.datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S') + "\t" + string)

                now_time = int(time.time())
                t = now_time - self.start_time
                if t != 0:
                    self.TextAInput.SetValue('当前实时效率为：' + str(int(self.send_count / t)) + '条/秒')

    def send(self, sk, f):
        self.start_time = int(time.time())
        self.send_count = 0
        q = queue.Queue()
        threading.Thread(target=self.monitor, args=(q,)).start()

        if self.run_type == '循环执行':
            while True:
                # 发送消息
                for line in f:
                    if self.status == 1:
                        string = line.decode(chardet.detect(line).get("encoding"))
                        sk.send(string.encode("UTF-8"))
                        self.send_count = self.send_count + 1
                        q.put(string)
                    else:
                        break
                    time.sleep(int(self.IndicatInput_Box2.GetValue()) / 1000)
                if self.status == 0:
                    break
                f.seek(0)
        else:
            res = int(self.custom_value.GetValue())  # 记录发送次数
            while True:
                for line in f:
                    if res != 0 and self.status != 0:
                        string = line.decode(chardet.detect(line).get("encoding"))
                        sk.send(string.encode("UTF-8"))
                        res = res - 1
                        self.send_count = self.send_count + 1
                        q.put(string)
                        time.sleep(int(self.IndicatInput_Box2.GetValue()) / 1000)
                    else:
                        self.status = 0
                        break
                if self.status == 0:
                    res = 0
                    break
                f.seek(0)
