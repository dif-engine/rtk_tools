from .text import rtkText
import collections

import Tkinter as tk
import ttk

import roslib
import rospy

class rtkNumber(rtkText):
  def __init__(self,page,prop):
    super(rtkNumber,self).__init__(page,prop)

  def set(self,value):
    print "type",type(value)
    if type(value) is str:
      super(rtkNumber,self).set(value)
    else:
      self.io.delete(0,tk.END)
      self.io.insert(0,str(value))
      param=eval(self.lb+str(value)+self.rb)
      self.merge(self.Param,param)
      self.value=value
      print "set as number",value
      rospy.set_param(self.prop["name"],value)
  def on_change(self,event):
    try:
      sval=self.io.get()
      if "." in sval:
        nval=float(sval)
      else:
        nval=int(sval)
      self.set(nval)
      self.io.config(foreground='#000000')
    except:
      super(rtkNumber,self).on_change(event)
  def reflesh(self):
    try:
      value=rospy.get_param(self.prop["name"])
      if type(value) is str:
        if "." in value:
          value=float(value)
        else:
          value=int(value)
      if value!=self.value:
        self.set(value)
    except:
      rospy.logwarn("param "+self.prop["name"]+" not found or wrong number")
    return
