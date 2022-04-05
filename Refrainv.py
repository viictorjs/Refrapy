##Refrapy - Seismic Refraction Data Analysis
##Refrainv - Data inversion
##Author: Victor Guedes, MSc
##E-mail: vjs279@hotmail.com

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Toplevel, Frame, Button, Label, filedialog, messagebox, PhotoImage, simpledialog
from os import path, makedirs, getcwd
from obspy import read
from obspy.signal.filter import lowpass, highpass
from scipy.signal import resample
from scipy.interpolate import interp1d
from numpy import array, where, polyfit
import Pmw
import warnings

warnings.filterwarnings('ignore')

class Refrainv(Tk):
    
    def __init__(self):
        
        super().__init__()
        self.geometry("1600x900")
        self.title('Refrapy - Refrainv v2.0.0')
        self.configure(bg = "#F0F0F0")
        self.resizable(0,0)
        self.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

        frame_toolbar = Frame(self)
        frame_toolbar.grid(row=0,column=0,sticky="EW")
        
        photo = PhotoImage(file="%s/images/ico_refrapy.gif"%getcwd())
        labelPhoto = Label(frame_toolbar, image = photo, width = 151)
        labelPhoto.image = photo
        labelPhoto.grid(row=0, column =0, sticky="W")
        self.statusLabel = Label(frame_toolbar, text = "Create or load a project to start", font=("Arial", 11))
        self.statusLabel.grid(row = 0, column = 4, sticky = "W")
        Pmw.initialise(self)

        self.ico_newProject = PhotoImage(file="%s/images/ico_newProject.gif"%getcwd())
        self.ico_loadProject = PhotoImage(file="%s/images/ico_loadProject.gif"%getcwd())
        self.ico_openPick = PhotoImage(file="%s/images/ico_loadPicks.gif"%getcwd())

        bt = Button(frame_toolbar,image = self.ico_newProject,command = self.createProject,width=25)
        bt.grid(row = 0, column = 1, sticky="W")
        bl = Pmw.Balloon(self)
        bl.bind(bt,"Create new project path")
        
        bt = Button(frame_toolbar,image = self.ico_loadProject,command = self.loadProject,width=25)
        bt.grid(row = 0, column = 2, sticky="W")
        b = Pmw.Balloon(self)
        b.bind(bt,"Load project path")
        
        bt = Button(frame_toolbar, image = self.ico_openPick,command = self.loadPick)
        bt.grid(row = 0, column = 3, sticky="W")
        b = Pmw.Balloon(self)
        b.bind(bt,"Load pick file")

        self.protocol("WM_DELETE_WINDOW", self.kill)
        self.initiateVariables()

    def initiateVariables(self):

        self.projReady = False
    
    def kill(self):

        out = messagebox.askyesno("Refrainv", "Do you want to close the software?")

        if out: self.destroy(); self.quit()

    def createPanels(self):

        self.frame_timeterms = Frame(self, bg = "white")
        self.frame_timeterms.grid(row = 1, column = 0, sticky = "EW")

        self.frame1 = Frame(self.frame_timeterms, bg = "white")
        self.frame1.grid(row = 0, column = 0, sticky = "E")
        self.fig1 = plt.figure(figsize = (8.05,3.65))
        canvas1 = FigureCanvasTkAgg(self.fig1, self.frame1)
        canvas1.draw()
        toolbar1 = NavigationToolbar2Tk(canvas1, self.frame1)
        toolbar1.update()
        canvas1._tkcanvas.pack()
        self.ax1 = self.fig1.add_subplot(111)
        self.fig1.patch.set_facecolor('#F0F0F0')

        self.frame2 = Frame(self.frame_timeterms, bg = "white")
        self.frame2.grid(row = 0, column = 1, sticky = "W")
        self.fig2 = plt.figure(figsize = (8.05,3.65))
        canvas2 = FigureCanvasTkAgg(self.fig2, self.frame2)
        canvas2.draw()
        toolbar2 = NavigationToolbar2Tk(canvas2, self.frame2)
        toolbar2.update()
        canvas2._tkcanvas.pack()
        self.ax2 = self.fig2.add_subplot(111)
        self.fig2.patch.set_facecolor('#F0F0F0')

        self.frame3 = Frame(self.frame_timeterms, bg = "white")
        self.frame3.grid(row = 1, column = 0, sticky = "EW", columnspan=2)
        self.fig3 = plt.figure(figsize = (16.1,4.05))
        canvas3 = FigureCanvasTkAgg(self.fig3, self.frame3)
        canvas3.draw()
        toolbar3 = NavigationToolbar2Tk(canvas3, self.frame3)
        toolbar3.update()
        canvas3._tkcanvas.pack()
        self.ax3 = self.fig3.add_subplot(111)
        self.fig3.patch.set_facecolor('#F0F0F0')

        self.frame_timeterms.tkraise()
      
    def createProject(self):

        pass

    def loadProject(self):

        self.createPanels()

    def loadPick(self):

        self.projReady = True

        
        if self.self.porjReady:

            pickFile = filedialog.askopenfilename(title='Open', initialdir = self.projPath+"/picks/", filetypes=[('Pick file', '*.sgt')])

            if pickFile:

                with open(pickFile, "r") as file:

                    lines = file.readlines()
                    npoints = int(lines[0].split()[0])
                    sgx = [float(i.split()[0]) for i in lines[2:2+npoints]]
                    sgtindx = lines.index("#s g t\n")
                    s = [int(i.split()[0]) for i in lines[sgtindx+1:]]
                    g = [int(i.split()[1]) for i in lines[sgtindx+1:]]
                    t = [float(i.split()[2]) for i in lines[sgtindx+1:]]
                    sx = [sgx[i-1] for i in s]
                    gx = [sgx[i-1] for i in g]
                    loaded = False
                        
                    for i in range(len(self.sts)):
                    
                        for j in range(len(sx)):

                            if self.sources[i] == sx[j] and gx[j] in self.receiverPositions[i]:

                                pickline = self.axs[i].hlines(t[j], gx[j]-(self.dx*0.25),gx[j]+(self.dx*0.25),color='r')
                                self.picksArts[i].append(pickline)
                                self.xpicks[i].append(gx[j])
                                self.tpicks[i].append(t[j])
                                loaded = True


















        
app = Refrainv()
app.mainloop()
