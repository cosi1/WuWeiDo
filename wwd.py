#!/usr/bin/env python
# coding=utf-8
import os.path as op
import sys
import json

"""
WuWeiDo - a Taoist to-do list
Author: Paweł Piątkowski
"""

VERSION = "0.0.2"


class ToDoList(object):
    """
    The main class. Provides methods for managing to-do lists.
    """
    BASE_DIR = op.dirname(op.realpath(__file__))
    CONFIG_FILE = op.join(BASE_DIR, "wwd.conf")
    DEFAULT_TASK_FILE = op.join(BASE_DIR, "tasks.wwd")

    def __init__(self):
        self.config = self.get_config()
        self.tasks = self.get_tasks()

    def get_config(self):
        config = {}
        if not op.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "wb") as f:
                f.write("TaskFile=%s" % self.DEFAULT_TASK_FILE)
            config["TaskFile"] = self.DEFAULT_TASK_FILE
        else:
            with open(self.CONFIG_FILE, "rb") as f:
                for line in f:
                    config_line = line.strip().split("=")
                    if len(config_line)>1:
                        config[config_line[0]] = config_line[1]
        return config

    def get_tasks(self):
        """
        Returns all the tasks as a list.
        """
        fname = self.config["TaskFile"]
        if not op.exists(fname):
            with open(fname, "wb") as f:
                f.write("[]")
            return []
        with open(fname, "rb") as f:
            json_data = f.read()
        return json.loads(json_data)

    def get_current_path(self):
        """
        Returns the full path (i.e. all the parent tasks) of the current task.
        """
        tree = self.tasks
        task = []
        while len(tree)>0:
            if type(tree) in (unicode, str):
                return task + [tree]
            if type(tree) is dict:
                task.append(tree.keys()[0])
                tree = tree.itervalues().next()[0]
            else:
                tree = tree[0]
        return ""

    def get_current_task(self):
        """
        Returns the title of the current task.
        """
        task = self.get_current_path()
        if len(task)>0:
            return task[-1]
        else:
            return ""

    def delete_current_task(self):
        """
        Deletes the current task.
        """
        def del_first(tree):
            if not (type(tree) in (list, dict)) or len(tree)==0:
                return
            if type(tree) is dict:
                subtree = tree.itervalues().next()[0]
            else:
                subtree = tree[0]
            if type(subtree) is dict and len(subtree)>0:
                del_first(subtree)
            if type(subtree) in (unicode, str) or len(subtree)==0:
                if type(tree) is dict:
                    first_key = tree[tree.keys()[0]]
                    first_key.pop(0)
                    if len(first_key)==0:
                        tree.popitem()
                else:
                    tree.pop(0)
        del_first(self.tasks)
        with open(self.config["TaskFile"], "wb") as f:
            json.dump(self.tasks, f)

    def add_task(self, task):
        """
        Adds a new task to the current path (at the end of the list).
        """
        tree = self.tasks
        if len(tree)==0:
            tree.append(task)
        else:
            while len(tree)>0:
                if type(tree) is dict:
                    t = tree.itervalues().next()[0]
                    tree = tree[tree.keys()[0]]
                else:
                    t = tree[0]
                if type(t) in (unicode, str):
                    tree.append(task)
                    break
                tree = t
        with open(self.config["TaskFile"], "wb") as f:
            json.dump(self.tasks, f)

    def split_task(self, subtask):
        """
        Splits the current task, creating the first subtask.
        """
        tree = self.tasks
        task = ""
        while len(tree)>0:
            if type(tree) is dict:
                t = tree.itervalues().next()[0]
                tree = tree[tree.keys()[0]]
            else:
                t = tree[0]
            if type(t) in (unicode, str):
                task = tree.pop(0)
                tree.insert(0, {task: [subtask]})
                break
            tree = t
        with open(self.config["TaskFile"], "wb") as f:
            json.dump(self.tasks, f)
        return (task, subtask)


if __name__=="__main__":
    td = ToDoList()

    if len(sys.argv)<2:
        task = td.get_current_task()
        if task=="":
            task = "<no tasks>"
        exit(task)

    arg = sys.argv[1]

    if arg=="d":
        task = td.get_current_task()
        if task=="":
            exit("No tasks! :-)")
        td.delete_current_task()
        exit("'%s' done!" % task)

    if arg=="f":
        task = " > ".join(td.get_current_path())
        exit(task)

    if arg=="a":
        try:
            task = sys.argv[2]
            td.add_task(task)
            exit("'%s' added to the parent task. Good luck!" % task)
        except IndexError:
            exit("Please specify the title of your task in the command line.")

    if arg=="s":
        try:
            subtask = sys.argv[2]
            names = td.split_task(subtask)
            exit("'%s' is now a parent task of '%s'." % names)
        except IndexError:
            exit("Please specify the title of the first subtask in the command line.")

    print "WuWeiDo %s by Paweł Piątkowski -- \x1b[32mDo your work like a Sage\x1b[0m" % VERSION
    print "Options:"
    print "  <no option> - show the current task"
    print "  d - set the task as done (delete it from the list)"
    print "  f - show the path of the current task (i.e. all the parent tasks)"
    print "  a \"Task description\" - add a new task to the current path"
    print "  s \"First subtask\" - split the current task into subtasks"

