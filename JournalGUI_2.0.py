## Program: JournalGUI.py
## Version: 2.0
## Author: Kozmik Moore
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
import pickle
import collections
import os

MONTH_DICT={"Jan":"01","Feb":"02","Mar":"03","Apr":"04",'May':'05','June':'06',
                       'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

class JournalWidget():
    def __init__(self):
        #Variables
        date=""
        registry=self.GetEntries()

        #Main Window Instantiation
        self.mainwidget=Tk()
        self.mainwidget.title("Journal")

##        self.pagecount="Page1"
##
##        self.bodycontainer={}
##        for f in ("Page1", "Page2"):
##            frame=f(self.mainwidget, self)
##            self.bodycontainer[f]=frame
##            frame.pack()
            
        #Options Frame
        optionsframe=Frame(self.mainwidget)
        optionstop=Frame(optionsframe)
        SAVE=Button(optionstop, text="Save", command=self.SaveEntry)
        QUIT=Button(optionstop, text="Quit", command=lambda:self.DestroyMainWindow(self.mainwidget))
        SAVE.pack(side=LEFT)
        QUIT.pack(side=LEFT)
        optionstop.pack(side=TOP)
        optionsbottom=Frame(optionsframe)
        NEW=Button(optionsbottom, text="New Entry", command=self.NewEntry)
        LINK=Button(optionsbottom, text="Create Link", command=lambda:self.NewEntry(self.GetDate()))
        NEW.pack(side=LEFT)
        LINK.pack(side=LEFT)
        optionsbottom.pack(side=TOP)
        optionsframe.pack(side=BOTTOM)        

    def MakeDateFrame(self):
        #Date frame
        dateframe=Frame(self.mainwidget, height=1)
        registry=self.GetEntries()
        datekey=()
        binkey=sorted(registry, reverse=False)
        for i in binkey:
            date=self.ConvertDate("program", i)
            index=(date,)
            datekey+=index
        datelabel=Combobox(dateframe, values=datekey)
        datelabel.bind("<<ComboboxSelected>>", lambda e: self.UpdateDisplay(datelabel.get()))
        MODIFY=Button(dateframe, text="Modify", command=self.ModifyDate)
        datelabel.pack(side=LEFT)
        MODIFY.pack(side=LEFT)
        dateframe.pack(side=TOP)

    def MakeBodyFrame(self, text=None):
        #Body Frame
        bodyframe=Frame(self.mainwidget)
        scrollbar=Scrollbar(bodyframe)
        self.body=Text(bodyframe, yscrollcommand=scrollbar.set, wrap=WORD)
        scrollbar.config(command=self.body.yview)
        self.body.pack(side=LEFT)
        scrollbar.pack(side=LEFT, fill=Y)
        bodyframe.pack(side=TOP, padx=2, pady=2)
##        if text:
##            try:
##                body.insert(CURRENT, text)
##            except KeyError:
##                self.ThrowError("Please choose an entry.")

    def MakeTagsFrame(self):
        #Tags Frame
        tagsframe=Frame(self.mainwidget, height=1)
        tagslabel=Label(tagsframe, text="Tags:", width=5)
        self.tagstext=Text(tagsframe, height=1, width=70)
        tagslabel.pack(side=LEFT)
        self.tagstext.pack(side=LEFT)
        tagsframe.pack(side=TOP)

    def MakeLinksFrame(self):
        #Links Frame
        linksframe=Frame(self.mainwidget, height=1)
        linkslabel=Label(linksframe, text="Links:", width=5)
        self.linkstext=Text(linksframe, height=1, width=70)
        linkslabel.pack(side=LEFT)
        self.linkstext.pack(side=LEFT)
        linksframe.pack(side=TOP)

    def UpdateDisplay(self, value):
##        print("check2")
##        if value!="":
        date=self.ConvertDate("user", value)
        registry=self.GetEntries()
        self.body.delete("1.0", END)
        self.tagstext.delete("1.0", END)
        self.linkstext.delete("1.0", END)
        self.body.insert(CURRENT, registry[date][0])
        self.tagstext.insert(CURRENT, registry[date][1])
        self.linkstext.insert(CURRENT, registry[date][2])
    
                       
    def ModifyDate(self):
        print("Yes!")

    def SaveEntry(self):
        print("Excellent!")

    def NewEntry(self, date=None):
        if date==None:
            print("Watch Out!")
        else:
            print("Here it comes!")

    def DestroyMainWindow(self, window):
        window.destroy()

    def CreateWindow(self, window=None):
        if window==None:
            self.mainwidget.mainloop()
        else:
            window.mainloop()

    def GetEntries(self):
        filelocation="C:/Users/Kozmik Moore/Dropbox/Journal/Registry.bin"
        errstring=""
        try:
            binfilein=open(filelocation, "rb")
            try:
                fildict={}
                filedict=pickle.load(binfilein)
                return filedict
            except EOFError:
                errstring="Error. File is Empty"
            self.ThrowError(errstring)
        except IOError:
            errstring="Error. File not found."
            self.ThrowError(errstring)

    def GetDate(self):
        date=datetime.today()
        datestr=(datetime.strftime(date, "%d %b %Y, %H%M:%S"))
        return datestr        

    def ConvertDate(self, form, value):
        #This method will convert dates for user- and program-friendly formats
        date=""
        if form=="program":               ##value given is in program-friendly format
            try:
                date+=value[2:4]+" "
                date+=list(MONTH_DICT.keys())[list(MONTH_DICT.values()).index(value[0:2])]+" "
                date+=value[4:8]+", "
                date+=value[8:12]+":"
                date+=value[12:]
            except ValueError:              ##value is in user-friendly format
                date+=MONTH_DICT[value[3:6]]
                date+=value[0:2]
                date+=value[7:11]
                date+=value[13:17]
                date+=value[18:]
        else:
            date+=MONTH_DICT[value[3:6]]
            date+=value[0:2]
            date+=value[7:11]
            date+=value[13:17]
            date+=value[18:]
        return date
            

    def ThrowError(self, errormsg):
        errorwindow=Toplevel()
        errorwindow.title("Error")
        errormessage=Label(errorwindow, text=errormsg)
        button=Button(errorwindow, text="OK", command=errorwindow.destroy)
        errormessage.pack(side=TOP)
        button.pack(side=TOP)
        errorwindow.lift()
        
app=JournalWidget()
app.MakeDateFrame()
app.MakeBodyFrame()
app.MakeTagsFrame()
app.MakeLinksFrame()
app.CreateWindow()
