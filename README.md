# Do your work like a Sage

> A journey of a thousand miles begins with the first step.

> -- Laozi, *Tao Te Ching*

Ever felt overwhelmed by the pile of tasks to be done? Tried to organize your work with some productivity software? Didn't work?

Why don't you do it the Taoist way?

# WuWeiDo

The idea behind the program can be summarized in these three points:

* Split your work into tasks so small that you can accomplish them without feeling overwhelmed.
* Do *one* task at a time, don't think about the other ones.
* As you have finished your task, forget it, make a pleasant break and proceed to the next one.

# Now about the program

### Files

    wwd.py - the main module; also a command-line client
    wuweido.py - Tk-based GUI
    flow.png, wwd.png - icons
    wwd.conf - config file (not included in the repository, created automatically)
    tasks.wwd - default tasks file (may be changed in the config file); JSON format, may be edited

### Installation

Simply put all the files into one directory; you might want to add that directory to your system path. WuWeiDo requires Python 2.x (tested on 2.7.6, should run with 2.6). It should work on every OS capable of running Python and Tk bindings.

Make sure that wwd.py and wuweido.py can be executed from the command line ("chmod +x *.py" in Linux 
console), so that you can run them directly without invoking Python.

### Usage

#### Command-line client

    wwd.py

Shows the current task.

    wwd.py d

Sets the current task as done (deletes it) and proceeds to the next task.

    wwd.py f

Shows the full path of the current task (i.e. all the parent tasks).

    wwd.py a "Task title"

Adds a new task to the current path.

    wwd.py s "First subtask's title"

Splits the current task into subtasks. You need to specify the title of the first subtask.

    wwd.py h

Shows help.

#### GUI

The current task is shown in the middle of the window. Clicking it will set the task as done (and delete it).

To show/collapse the full path, click the button marked "**>**".

To add a new task to the current path, click "**+**" and enter the title of your task.

To split the current task into subtasks, click the rightmost button and enter the title of the first subtask.

