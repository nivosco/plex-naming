'''
September 2014
@author: Niv Voskoboynik
'''

import base64
import tkinter
import os
from tkinter.filedialog import askopenfilename
from fnmatch import translate

class GUI(tkinter.Frame):

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.printTextToScreen = tkinter.StringVar()  
        self.printTextToScreen.set("")
        tkinter.Label(self.master, textvariable=self.printTextToScreen).pack()      
        self.currentFile = None
        self.outputText = None
        self.inputText = None
        self.conformationButton = None
        self.pathToCurrentFile = None
        self.create_widgets() 

    def exitProg(self):
        self.quit()

    def newFile(self):  
        self.printTextToScreen.set("") 
        self.currentFile = None
        self.outputText = None
        self.inputText = None
        self.conformationButton = None
        self.pathToCurrentFile = None

    def openFile(self):
        if self.currentFile is not None:
            self.currentFile = None;        
        try:
            self.currentFile = askopenfilename()
        except:
            self.printTextToScreen.set("Error: open file")
        else:
            self.printTextToScreen.set("File Opened Successfully")            

    def saveFile(self):     
        if self.pathToCurrentFile is not None:
            if self.currentFile is not None:
                try:
                    f = open(self.currentFile,"r")
                except:
                    self.printTextToScreen.set("Failed to open the file")         
                else:
                    text2save = str(f.read())
                    self.pathToCurrentFile.open()
                    self.pathToCurrentFile.write(text2save)
                    self.pathToCurrentFile.close()
                    f.close()
                    self.printTextToScreen.set("File was saved")
                    self.isSavedBoolean = True
            else:
                self.printTextToScreen.set("No File Found")            
        else:
            self.saveAsFile()  

    def saveAsFile(self):
        self.pathToCurrentFile = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if self.pathToCurrentFile is None:
            self.printTextToScreen.set("Error: save failed")
        else:         
            if self.currentFile is not None:
                try:
                    f = open(self.currentFile,"r")
                except:
                    self.printTextToScreen.set("Failed to open the file")         
                else:
                    text2save = str(f.read())
                    self.pathToCurrentFile.write(text2save)
                    self.pathToCurrentFile.close()
                    f.close()
                    self.printTextToScreen.set("File was saved")
                    self.isSavedBoolean = True
            else:
                self.printTextToScreen.set("No File Found")          

    def about(self):
        self.printTextToScreen.set("This program was made by Niv Voskoboynik (nivosco@gmail.com)\nAll rights reserved, September 2014")

    def printFile(self):
        if self.currentFile is not None:
            try:
                f = open(self.currentFile,"r")
            except:
                self.printTextToScreen.set("Failed to open the file")         
            else:
                self.printTextToScreen.set(f.read())
                f.close()
        else:
            self.printTextToScreen.set("No File Found")

    def editName(self):
        if self.currentFile is not None:
            self.printTextToScreen.set("What is the new Name:")
            self.inputText = tkinter.Entry(self.master)
            self.inputText.pack(padx=5)
            self.conformationButton = tkinter.Button(self.master, text="OK", command=self.changeName)
            self.conformationButton.pack(pady=5)
        else:
            self.printTextToScreen.set("No open files")    

    def changeName(self):
        name = self.inputText.get()       
        head,tail  = os.path.split(self.currentFile)
        os.rename(self.currentFile,(head+"/"+name+'.'+tail.split(".")[-1]))
        self.currentFile = head+"/"+name+'.'+tail.split(".")[-1]
        self.conformationButton.destroy()
        self.inputText.destroy()
        self.printTextToScreen.set("File name was changed")
        self.isSavedBoolean = False

    def standartDecode64(self):
        if self.currentFile is not None:
            try:
                f = open(self.currentFile,"r")
            except:
                self.printTextToScreen.set("Failed to open the file")         
            else:
                line = f.read()
                temp = line.find('base64',0,len(line))
                line = base64.b64decode(line[temp+8:temp+4*250], "  ", False)
                line = str(line)
                newline = ""
                for i in range(1,len(line)):
                    if line[i] < '0' or line[i] > '9':
                        newline = newline + line[i]
                    else:
                        if len(newline)>1:
                            if newline[len(newline)-1]!='\n':
                                newline = newline + '\n'              
                self.printTextToScreen.set(newline)
                f.close()                       
        else:
            self.printTextToScreen.set("No open files") 

    def plex(self):
        self.printTextToScreen.set("What is the name of the TV show:")
        self.inputText = tkinter.Entry(self.master)
        self.inputText.pack(padx=5)
        self.conformationButton = tkinter.Button(self.master, text="OK", command=self.tvShow)
        self.conformationButton.pack(pady=5)

    def tvShow(self):
        line = ""
        directoryTv = tkinter.filedialog.askdirectory()
        name = self.inputText.get()
        self.conformationButton.destroy()
        self.inputText.destroy()
        list_dir = os.listdir(directoryTv)
        for file in list_dir:           
            head,tail = os.path.split(file)#@UnusedVariable
            season,episode = self.getSeasonEpisode(tail)
            exten = tail.split(".")[-1]
            file = str(file)
            directoryTv = str(directoryTv)
            name = str(name)
            exten = str(exten)
            if exten=="srt" or exten=="sub" or exten=="txt":
                try:
                    os.rename(directoryTv+"/"+file,directoryTv+"/"+name+" - s"+season+"e"+episode+'.'+exten)  
                except:
                    continue
                line = line+file+"   ->   "+name+" - s"+season+"e"+episode+"."+exten+'\n'
            if exten=="mkv" or exten=="avi" or exten=="mp4" or exten=="rmvb":
                try:
                    os.rename(directoryTv+"/"+file,directoryTv+"/"+name+" - s"+season+"e"+episode+'.'+exten)
                except:
                    continue
                line = line+file+"   ->   "+name+" - s"+season+"e"+episode+"."+exten+'\n'
        if line=="":
            self.printTextToScreen.set("No changes")
        else:
            self.printTextToScreen.set(line)

    def getSeasonEpisode(self,name):
        season = 0 
        episode = 0
        for i in range(0,len(name)-2):
            if ((name[i]=='s' or name[i]=='S') and (name[i+1]>='0' and name[i+1]<='9') and (name[i+2]>='0' and name[i+2]<='9')):
                season = name[i+1]+name[i+2]
            if (name[i]=='e' or name[i]=='E') and (name[i+1]>='0' and name[i+1]<='9') and (name[i+2]>='0' and name[i+2]<='9'):
                episode = name[i+1]+name[i+2]
        return(season,episode)

    def translate(self):
        directory = tkinter.filedialog.askdirectory()
        gs = goslate.Goslate()        
        line = self.helper(directory,gs)
        if line=="":
            self.printTextToScreen.set("No changes")
        else:
            self.printTextToScreen.set(line)

    def helper(self,directory,gs):
        line = ""
        self.printTextToScreen.set("ok")
        for root,subFolders, files in os.walk(directory):
            self.printTextToScreen.set(files)
            for folder in subFolders:
                line = line + self.helper(directory+'/'+folder,gs)
            for folder in subFolders:
                translate = gs.translate(str(folder),'en')  
                line = line+folder+"   ->   "+translate+"\n"
                os.rename(directory+"/"+folder, directory+"/"+translate)                
            for file in files:
                head,tail = os.path.split(file)#@UnusedVariable
                exten = tail.split(".")[-1]
                name = tail.split(".")[0]
                file = str(file)
                exten = str(exten)
                try:
                    translate = gs.translate(str(name),'en')  
                    os.rename(directory+"/"+file, directory+"/"+translate+"."+exten)
                    line = line+file+"   ->   "+translate+"."+exten+"\n" 
                except:
                    continue
        return(line)

    def deleteExt(self):
        line = ""
        directoryTv = tkinter.filedialog.askdirectory()
        list_dir = os.listdir(directoryTv)
        directoryTv = str(directoryTv)
        for file in list_dir:           
            head,tail = os.path.split(file)#@UnusedVariable
            exten = tail.split(".")[-1]
            reg = tail.split(".")
            if str(reg[1] == "heb"):
                reg = str(reg[0])
                file = str(file)
                exten = str(exten)
                if exten=="srt" or exten=="sub" or exten=="txt":
                    try:
                        os.rename(directoryTv+"/"+file,directoryTv+"/"+reg+"."+exten)  
                    except:
                        continue
                    line = line+file+"   ->   "+reg+"."+exten+'\n'
        if line=="":
            self.printTextToScreen.set("No changes")
        else:
            self.printTextToScreen.set(line)       

    def create_widgets(self):
        menubar = tkinter.Menu(self)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.newFile)
        filemenu.add_command(label="Open", command=self.openFile)
        filemenu.add_command(label="Save", command=self.saveFile)
        filemenu.add_command(label="Save as...", command=self.saveAsFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exitProg())
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Edit File Name", command=self.editName)
        editmenu.add_command(label="Plex Naming", command=self.plex)
        editmenu.add_command(label="Delete extension", command=self.deleteExt)
        editmenu.add_command(label="Translate Folder", command=self.translate)
        editmenu.add_command(label="b64decode", command=self.standartDecode64)
        menubar.add_cascade(label="Edit",menu=editmenu)
        viewmenu = tkinter.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Print", comman=self.printFile)
        menubar.add_cascade(label="View",menu=viewmenu)
        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.master.config(menu=menubar)

root = tkinter.Tk()
root.title("Plex GUI")
root.geometry("500x1000")
app = GUI(root)
root.mainloop()
