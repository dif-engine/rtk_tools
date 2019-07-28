#!/usr/bin/python

import numpy as np
import yaml
import threading

import roslib
import rospy

import Tkinter as tk
import ttk
from src.widget import rtkWidget
from src.page import rtkPage
from src.text import rtkText
from src.number import rtkNumber
from src.echo import rtkEcho
from src.pub import rtkPub
from src.title import rtkTitle

def loadwidget(filename):
  page=rtkPage(root)
  f=open(filename,'r')
  for line in f:
    prop=eval("{"+line+"}")
    if "class" not in prop: continue
    if prop["class"]=="Title":
      if "page" in prop:
        if prop["page"]=="break":
          page=rtkPage(root)
    w=eval("rtk"+prop["class"]+"(page,prop)")
  f.close()

def cb_pagefwd():
  if rtkPage.pageNo<len(rtkPage.pages)-1:
    ctrl.pack_forget()
    rtkPage.show(1)
    ctrl.pack(fill='x',anchor='sw',expand=1)

def cb_pagebwd():
  if rtkPage.pageNo>0:
    ctrl.pack_forget()
    rtkPage.show(-1)
    ctrl.pack(fill='x',anchor='sw',expand=1)

def cb_save():
   return

def cb_scan():
  if rtkPage.pageNo<0: return
  rtkPage.reload()
  print yaml.dump(rtkWidget.Param)
  t=threading.Timer(1,cb_scan)
  t.start()

def cb_close():
  rtkPage.pageNo=-1
  return

####ROS Init####
rospy.init_node("rtk_panel",anonymous=True)

####Layout####
root=tk.Tk()
ttk.Style(root).theme_use("clam")
root.title("panel")
root.geometry("300x800+0+0")
root.protocol("WM_DELETE_WINDOW", cb_close)

loadwidget("panel.ui")

ctrl=tk.Frame(root,bd=2,background='#444444')
ctrl.columnconfigure(1,weight=1)
ctrl.columnconfigure(2,weight=1)
ctrl.columnconfigure(3,weight=1)
ttk.Button(ctrl,text="<<<",command=cb_pagebwd).grid(row=1,column=1,padx=1,pady=1,sticky='nsew')
ttk.Button(ctrl,text=">>>",command=cb_pagefwd).grid(row=1,column=2,padx=1,pady=1,sticky='nsew')
ttk.Button(ctrl,text="Save",command=cb_save).grid(row=1,column=3,padx=1,pady=1,sticky='nsew')

rtkPage.show(0)
ctrl.pack(fill='x',anchor='sw',expand=1)

cb_scan()
while rtkPage.pageNo>=0 and not rospy.is_shutdown():
  root.update()
rtkPage.pageNo=-1

