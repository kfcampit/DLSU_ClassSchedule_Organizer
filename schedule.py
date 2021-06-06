from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import pandas as pd
import os
import sys


class schedulePage:
    def __init__(self, root):
        self.root = root
        root.title("DLSU Class Schedule Organizer")
        root.protocol("WM_DELETE_WINDOW", lambda : sys.exit(0))

        if os.stat("schedule\\sched.txt").st_size == 0:
            self.gotoEnlist()

        mainframe = Frame(root)
        mainframe.grid(column = 0, row = 0, padx = 8, pady = 8)

        calendar = Frame(mainframe, background = "green3")
        calendar.grid(columnspan = 2, column = 1, row = 2, padx = 8, pady = 8)

        Label(mainframe, text = "Schedule", font = Font(family = "Corbel", size = 20, weight = "bold")).grid(columnspan = 2, column = 1, row = 1, pady = 4)

        self.initializeSchedule()

        days = ["TIME", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
        
        for d, day in enumerate(days):
            Label(calendar, text = day, width = 16, borderwidth = 1, relief = "groove", background = "green4").grid(column = d, row = 0, sticky = (W, E))

        for time, t in enumerate(range(1, ((self.lateTime - self.earlyTime) * 2) + 3, 2), self.earlyTime):
            Label(calendar, text = str(time) + ":00", width = 16, height = 2, borderwidth = 1, relief = "groove", background = "green3").grid(rowspan = 2, column = 0, row = t, sticky = (W, E))

        self.labelColors = [["PaleGreen1" for x in range(1, 7)] for y in range(1, ((self.lateTime - self.earlyTime) * 2) + 3)]
        self.labelText = [["" for x in range(1, 7)] for y in range(1, ((self.lateTime - self.earlyTime) * 2) + 3)]

        try:
            self.loadColors()
        except:
            pass

        for i in range(1, ((self.lateTime - self.earlyTime) * 2) + 3):
            for j in range(1, 7):
               Label(calendar, width = 16, text = self.labelText[i - 1][j - 1], height = 1, borderwidth = 1, relief = "groove", background = self.labelColors[i - 1][j - 1]).grid(column = j, row = i, sticky = (W, E))

        self.titleText = StringVar(root)
        self.titleText.set("Select a Course")
        self.optionList = [n[0] for n in self.classTimes]

        OptionMenu(mainframe, self.titleText, *self.optionList).grid(column = 1, row = 3, ipadx = 90, sticky = E)
        ttk.Button(mainframe, text = "View", width = 16, command = self.view).grid(column = 2, row = 3, sticky = W, padx = 4, pady = 4)
        ttk.Button(mainframe, text = "Delete", width = 16, command = self.delete).grid(column = 2, row = 4, sticky = W, padx = 4, pady = 4)
        ttk.Button(mainframe, text = "Enlist", width = 16, command = self.gotoEnlist).grid(column = 1, row = 5, sticky = W, padx = 4, pady = 4)
        ttk.Button(mainframe, text = "Exit", width = 16, command = self.back).grid(column = 2, row = 5, sticky = E, padx = 4, pady = 4)

        
    def loadColors(self):
        colors = ["red", "blue", "yellow", "orange", "snow", "purple1", "VioletRed1", "goldenrod1", "snow4", "dark olive green", "light cyan", "colar"]
        c = 0

        for classInfo in self.classTimes:
            
            for day in classInfo[-3]:
                if day == "M": d = 0
                elif day == "T": d = 1
                elif day == "W": d = 2
                elif day == "H": d = 3
                elif day == "F": d = 4
                elif day == "S": d = 5

                n = (int(classInfo[-2]) // 100) - self.earlyTime
                n *= 2
                if int(classInfo[-2]) % 100 >= 30:
                    n += 1
        
                m = (int(classInfo[-1]) // 100) - self.earlyTime
                m *= 2
                if int(classInfo[-1]) % 100 >= 30:
                    m += 1

                
                
                for i in range(n, m):
                    self.labelColors[i][d] = colors[c]

                self.labelText[n][d] = classInfo[0]
            c += 1

    def initializeSchedule(self):
        with open("schedule\\sched.txt", mode = "r", encoding = "utf8") as readSched:
            holder = readSched.readlines()
        self.classSched = [classData.strip().split(";") for classData in holder]

        times = []

        for item in self.classSched:
            times.append(int(float(item[-2])))
            times.append(int(float(item[-1])))
        
        self.earlyTime = min(times) // 100
        self.lateTime = max(times) // 100
        
        self.classTimes = [[i[0], i[-3], int(float(i[-2])), int(float(i[-1])) ] for i in self.classSched]
        pass

    def view(self, *args):
        root = Toplevel()
        root.title("View " + self.titleText.get())
        mainframe = (root)

        loadClass = list(filter(lambda i: (i[0] == self.titleText.get()), self.classSched))
        viewClass = loadClass[0]

        Label(mainframe, text = "View Course", font = Font(family = "Corbel", size = 16, weight = "bold")).grid(columnspan = 2, column = 1, row = 1, pady = 4, sticky = (W, E))

        Label(mainframe, text = viewClass[0], width = 32, font = Font(size = 12, family =  "Helvetica"), borderwidth = 1, relief = "groove").grid(columnspan = 2, column = 1, row = 2, sticky = (W, E))

        Label(mainframe, text = viewClass[1], width = 32, font = Font(size = 12, family =  "Helvetica"), borderwidth = 1, relief = "groove").grid(columnspan = 2, column = 1, row = 3, sticky = (W, E))
        
        Label(mainframe, text = viewClass[4], width = 32, font = Font(size = 12, family =  "Helvetica"), borderwidth = 1, relief = "groove").grid(columnspan = 2, column = 1, row = 4, sticky = (W, E))

        Label(mainframe, text = viewClass[2], width = 16, font = Font(size = 12, family =  "Helvetica"), borderwidth = 1, relief = "groove").grid(column = 1, row = 5, sticky = (W, E))

        Label(mainframe, text = viewClass[3], width = 16, font = Font(size = 12, family =  "Helvetica"), borderwidth = 1, relief = "groove").grid(column = 2, row = 5, sticky = (W, E))
        
        Label(mainframe, text = viewClass[5], width = 16, font = Font(size = 12, family =  "Helvetica"), borderwidth = 1, relief = "groove").grid(column = 1, row = 6, sticky = (W, E))

        Label(mainframe, text = str(int(float(viewClass[6]))) + " - " + str(int(float(viewClass[7]))), width = 16, font = Font(size = 12, family =  "Helvetica"), borderwidth = 1, relief = "groove").grid(column = 2, row = 6, sticky = (W, E))

    def delete(self, *args):
        with open("schedule\\sched.txt", mode = "r", encoding = "utf8") as removeLine:
            lines = removeLine.readlines()
        with open("schedule\\sched.txt", mode = "w", encoding = "utf8") as rewrite:
            for line in lines:
                if not self.titleText.get() in line:
                    rewrite.write(line[:-1] + "\n")

        self.root.destroy()
        self.new_window = Tk()
        schedulePage(self.new_window)

    def gotoEnlist(self):
        self.root.destroy()
        self.new_window = Tk()
        enlistMain(self.new_window)
    
    def back(self, *args):
        self.root.destroy()
        pass


class enlistMain:
    def __init__(self, root):

        if not os.path.exists("schedule\\sched.txt"):
            if os.path.isdir("schedule"):
                try:
                    open("schedule\\sched.txt","x")
                except:
                    pass
            else:
                os.mkdir("schedule")
                open("schedule\\sched.txt","x")

        self.root = root
        root.title("DLSU Class Schedule Organizer")

        root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
        mainframe = Frame(root)
        mainframe.grid(column = 0, row = 0, padx = 8, pady = 8)

        Label(mainframe, text = "Enlistment", font = Font(family = "Corbel", size = 16, weight = "bold")).grid(columnspan = 2, column = 1, row = 1, pady = 4, sticky = (W, E))
        ttk.Separator(mainframe, orient = HORIZONTAL).grid(columnspan = 2, column = 1, row = 2, ipadx = 160, pady = 4)

        self.courseCde = StringVar()
        ttk.Label(mainframe, text = "Course Code: ", font = Font(family = "Corbel")).grid(column = 1, row = 3, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.courseCde, width = 32).grid(column = 2, row = 3, padx = 4, pady = 5, sticky = W)

        self.courseNo = StringVar()
        ttk.Label(mainframe, text = "Course Number: ", font = Font(family = "Corbel")).grid(column = 1, row = 4, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.courseNo, width = 32).grid(column = 2, row = 4, padx = 4, pady = 5, sticky = W)

        self.courseName = StringVar()
        ttk.Label(mainframe, text = "Course Name: ", font = Font(family = "Corbel")).grid(column = 1, row = 5, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.courseName, width = 32).grid(column = 2, row = 5, padx = 4, pady = 5, sticky = W)

        self.facultyName = StringVar()
        ttk.Label(mainframe, text = "Faculty Name: ", font = Font(family = "Corbel")).grid(column = 1, row = 6, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.facultyName, width = 32).grid(column = 2, row = 6, padx = 4, pady = 5, sticky = W)
        
        self.section = StringVar()
        ttk.Label(mainframe, text = "Section: ", font = Font(family = "Corbel")).grid(column = 1, row = 7, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.section, width = 32).grid(column = 2, row = 7, padx = 4, pady = 5, sticky = W)

        self.day = StringVar()
        ttk.Label(mainframe, text = "Day: ", font = Font(family = "Corbel")).grid(column = 1, row = 8, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.day, width = 32).grid(column = 2, row = 8, padx = 4, pady = 5, sticky = W)

        self.startTime = StringVar()
        ttk.Label(mainframe, text = "Start Time: ", font = Font(family = "Corbel")).grid(column = 1, row = 9, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.startTime, width = 32).grid(column = 2, row = 9, padx = 4, pady = 5, sticky = W)

        self.endTime = StringVar()
        ttk.Label(mainframe, text = "End Time: ", font = Font(family = "Corbel")).grid(column = 1, row = 10, padx = 4, pady = 5, sticky = W)
        ttk.Entry(mainframe, textvariable = self.endTime, width = 32).grid(column = 2, row = 10, padx = 4, pady = 5, sticky = W)

        ttk.Button(mainframe, text = "Schedule", width = 20, command = self.gotoSchedule).grid(column = 1, row = 11, sticky = W, pady = 16)
        ttk.Button(mainframe, text = "Save", width = 16, command = self.save).grid(column = 2, row = 11, padx = 4, sticky = E, pady = 16)
        

    def save(self, *args):
        checkList = [self.courseCde.get(), self.courseName.get(), self.courseNo.get(), self.section.get(), self.facultyName.get(), self.day.get(), self.startTime.get(), self.endTime.get()]

        with open("schedule\\sched.txt", mode = "a", encoding = "utf8") as writeText:
            writeText.write(";".join(list(map(str, checkList))) + "\n")
        
        self.gotoSchedule()
        
    def gotoSchedule(self):
        self.root.destroy()
        self.new_window = Tk()
        schedulePage(self.new_window)

root = Tk()
enlistMain(root)
root.mainloop()