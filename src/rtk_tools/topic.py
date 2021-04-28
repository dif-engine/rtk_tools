from .widget import rtkWidget

import tkinter as tk
from tkinter import ttk
import subprocess
import roslib
import rospy
import traceback

class rtkTopic(rtkWidget):
  def on_connect(self,topic_type):
    return
  def connect(self):
    print("cmdの内容を以下に表示↓↓↓")
    cmd="rostopic type "+self.prop["name"]
    print(cmd)

    try:
      print("resの内容を以下に表示↓↓↓")
      res=subprocess.check_output(cmd.split(" "))
      print(res)
      typ=res.decode().strip().split("/")
      print("execの内容を以下に表示↓↓↓")
      ldict = {}
      print("from "+typ[0].strip()+".msg import "+typ[1].strip()+" as topic_type")
      exec("from "+typ[0].strip()+".msg import "+typ[1].strip()+" as topic_type",globals(),ldict)
      print("topic_typeの内容を以下に表示↓↓↓")
      print(ldict['topic_type'])
      self.on_connect(ldict['topic_type'])
      self.discon=False
    except:
      print("rtkTopic::["+self.prop["name"]+"] not registered")
      traceback.print_exc()
  def __init__(self,page,prop):
    super(rtkTopic,self).__init__(page,prop)
    self.discon=True
    self.set_timeout(1)
  def on_timeout(self):
    if self.discon: self.connect()
    if self.discon: self.set_timeout(1)
