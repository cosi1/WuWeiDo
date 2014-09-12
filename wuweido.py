#!/usr/bin/env python
# coding=utf-8
from Tkinter import *
import tkMessageBox, tkSimpleDialog
from wwd import ToDoList, VERSION

"""
Tk-based GUI for WuWeiDo
Author: Paweł Piątkowski
"""


class Application(Frame):
    def __init__(self, master=None):
        self.td = ToDoList()
        Frame.__init__(self, master)
        self.taijitu_img = PhotoImage(file="wwd.png")
        self.master.tk.call("wm", "iconphoto", root._w, self.taijitu_img)
        self.split_img = PhotoImage(file="flow.png")
        self.pack()
        self.createWidgets()

    def showTask(self):
        task = self.td.get_current_task()
        self.task = task
        if task=="": task = "No tasks!"
        self.task_button["text"] = task
        self.master.title(task)

        if self.expanded:
            path = self.td.get_current_path()
            if len(path)<2:
                self.expand["text"] = "<"
            else:
                self.expand["text"] = " > ".join(path[0:-1])

    def createWidgets(self):
        self.taijitu = Button(self, image=self.taijitu_img)
        self.taijitu.image = self.taijitu_img
        self.taijitu["command"] = self.wwdMenu
        self.taijitu.pack({"side": "left"})

        self.expand = Button(self, text=">")
        self.expanded = False
        self.expand["command"] = self.expandView
        self.expand.pack({"side": "left"})

        self.task_button = Button(self)
        self.showTask()
        self.task_button["command"] = self.taskDone
        self.task_button.pack({"side": "left"})
        
        self.add_button = Button(self, text="+")
        self.add_button["command"] = self.addTask
        self.add_button.pack({"side": "left"})

        self.split_button = Button(self, image=self.split_img)
        self.split_button["command"] = self.splitTask
        self.split_button.pack({"side": "left"})

    def taskDone(self):
        if self.task=="":
            tkMessageBox.showinfo("Well done!", "You have no more tasks!")
        else:
            self.td.delete_current_task()
            tkMessageBox.showinfo("Well done!", "'%s' done!" % self.task)
            self.showTask()

    def wwdMenu(self):
        tkMessageBox.showinfo("WuWeiDo",
            "WuWeiDo %s by Paweł Piątkowski\nDo your work like a Sage" % VERSION)

    def expandView(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.showTask()
        else:
            self.expand["text"] = ">"

    def addTask(self):
        path = self.td.get_current_path()
        if len(path)>1:
            path_text = " to '%s'" % " > ".join(path[0:-1])
        else:
            path_text = ""
        task = tkSimpleDialog.askstring("Add a new task",
            "Enter the title of your task to be added%s:" % path_text)
        if task:
            self.td.add_task(task)
            self.showTask()

    def splitTask(self):
        path = self.td.get_current_path()
        if len(path)==0: return
        path_text = " > ".join(path)
        subtask = tkSimpleDialog.askstring("Split task",
            "Enter the title of your first subtask of '%s':" % path_text)
        if subtask:
            self.td.split_task(subtask)
            self.showTask()


root = Tk()
root.geometry("+0-33")
root.resizable(0, 0)
app = Application(master=root)
app.mainloop()

