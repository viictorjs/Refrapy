##Refrapy - Seismic Refraction Data Analysis
##Refrainv - Data inversion
##Author: Victor Guedes, MSc
##E-mail: vjs279@hotmail.com

from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Toplevel, Frame, Button, Label, filedialog, messagebox, PhotoImage, simpledialog, Entry
from os import path, makedirs, getcwd
from obspy import read
from obspy.signal.filter import lowpass, highpass
from scipy.signal import resample
from scipy.interpolate import interp1d,griddata
from numpy import array, where, polyfit, linspace, meshgrid, column_stack
from Pmw import initialise, Balloon
import pygimli as pg
from pygimli.physics import TravelTimeManager

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
        self.statusLabel.grid(row = 0, column = 16, sticky = "W")

        initialise(self)

        self.ico_newProject = PhotoImage(file="%s/images/ico_newProject.gif"%getcwd())
        self.ico_loadProject = PhotoImage(file="%s/images/ico_loadProject.gif"%getcwd())
        self.ico_openPick = PhotoImage(file="%s/images/ico_loadPicks.gif"%getcwd())
        self.ico_invTimeterms = PhotoImage(file="%s/images/vm.gif"%getcwd())
        self.ico_invTomo = PhotoImage(file="%s/images/tomogram.gif"%getcwd())
        self.ico_layerMode = PhotoImage(file="%s/images/camadas.gif"%getcwd())
        self.ico_clearLayers = PhotoImage(file="%s/images/limpar.gif"%getcwd())
        self.ico_layer1 = PhotoImage(file="%s/images/layer1.gif"%getcwd())
        self.ico_layer2 = PhotoImage(file="%s/images/layer2.gif"%getcwd())
        self.ico_layer3 = PhotoImage(file="%s/images/layer3.gif"%getcwd())
        self.ico_reset = PhotoImage(file="%s/images/fechar.gif"%getcwd())
        self.ico_plotOptions = PhotoImage(file="%s/images/ico_plotOptions.gif"%getcwd())
        self.ico_save = PhotoImage(file="%s/images/salvar.gif"%getcwd())
        self.ico_fit = PhotoImage(file="%s/images/ico_fit.gif"%getcwd())
        self.ico_invOptions = PhotoImage(file="%s/images/opt.gif"%getcwd())

        bt = Button(frame_toolbar,image = self.ico_newProject,command = self.createProject,width=25)
        bt.grid(row = 0, column = 1, sticky="W")
        bl = Balloon(self)
        bl.bind(bt,"Create new project path")
        
        bt = Button(frame_toolbar,image = self.ico_loadProject,command = self.loadProject,width=25)
        bt.grid(row = 0, column = 2, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Load project path")
        
        bt = Button(frame_toolbar, image = self.ico_openPick,command = self.loadPick)
        bt.grid(row = 0, column = 3, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Load pick file")

        bt = Button(frame_toolbar, image = self.ico_layerMode,command = self.loadPick)
        bt.grid(row = 0, column = 4, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Enable/disable layer assignmet mode (time-terms inversion)")

        bt = Button(frame_toolbar, image = self.ico_layer1,command = self.loadPick)
        bt.grid(row = 0, column = 5, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Assign layer 1 (direct wave)")

        bt = Button(frame_toolbar, image = self.ico_layer2,command = self.loadPick)
        bt.grid(row = 0, column = 6, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Assign layer 2 (refracted wave)")

        bt = Button(frame_toolbar, image = self.ico_layer3,command = self.loadPick)
        bt.grid(row = 0, column = 7, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Assign layer 3 (refracted wave)")

        bt = Button(frame_toolbar, image = self.ico_clearLayers,command = self.loadPick)
        bt.grid(row = 0, column = 8, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Clear layer assignment")

        bt = Button(frame_toolbar, image = self.ico_invTimeterms,command = self.loadPick)
        bt.grid(row = 0, column = 9, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Run time-terms inversion")

        bt = Button(frame_toolbar, image = self.ico_invTomo,command = self.runTomography)
        bt.grid(row = 0, column = 10, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Run tomography inversion")

        bt = Button(frame_toolbar, image = self.ico_fit,command = self.showFit)
        bt.grid(row = 0, column = 11, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Show fit and errors")

        bt = Button(frame_toolbar, image = self.ico_save,command = self.loadPick)
        bt.grid(row = 0, column = 12, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Save results")

        bt = Button(frame_toolbar, image = self.ico_invOptions,command = self.loadPick)
        bt.grid(row = 0, column = 13, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Inversion options")

        bt = Button(frame_toolbar, image = self.ico_plotOptions,command = self.loadPick)
        bt.grid(row = 0, column = 14, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Plot options")

        bt = Button(frame_toolbar, image = self.ico_reset,command = self.loadPick)
        bt.grid(row = 0, column = 15, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Reset all")

        self.protocol("WM_DELETE_WINDOW", self.kill)
        self.initiateVariables()

    def initiateVariables(self):

        self.projReady = False
        self.xdata = []
        self.tdata = []
        self.sources = []
        self.dataArts = []
        self.data_sourcesArts = []
        self.data_pg = False
        self.tomoPlot = False
        self.timetermsInv = False
        self.tomoMesh = False
    
    def kill(self):

        out = messagebox.askyesno("Refrainv", "Do you want to close the software?")

        if out: self.destroy(); self.quit()

    def createPanels(self):

        self.frame_plots = Frame(self, bg = "white")
        self.frame_plots.grid(row = 1, column = 0, sticky = "NSWE")

        self.frame_data = Frame(self.frame_plots)
        self.frame_data.grid(row = 0, column = 0, sticky = "W", rowspan = 2)
        self.fig_data = plt.figure(figsize = (6,8.1))
        canvas_data = FigureCanvasTkAgg(self.fig_data, self.frame_data)
        canvas_data.draw()
        toolbar_data = NavigationToolbar2Tk(canvas_data, self.frame_data)
        toolbar_data.update()
        canvas_data._tkcanvas.pack()
        self.ax_data = self.fig_data.add_subplot(111)
        self.fig_data.patch.set_facecolor('#F0F0F0')
        self.ax_data.set_title("Observed data")
        self.ax_data.set_xlabel("POSITION [m]")
        self.ax_data.set_ylabel("TIME [s]")
        self.ax_data.grid(lw = .5, alpha = .5)
        self.ax_data.spines['right'].set_visible(False)
        self.ax_data.spines['top'].set_visible(False)
        self.ax_data.yaxis.set_ticks_position('left')
        self.ax_data.xaxis.set_ticks_position('bottom')
        
        
        self.frame_timeterms = Frame(self.frame_plots)
        self.frame_timeterms.grid(row = 0, column = 1, sticky = "NSWE")
        self.fig_timeterms = plt.figure(figsize = (9.5,3.7))
        canvas_timeterms = FigureCanvasTkAgg(self.fig_timeterms, self.frame_timeterms)
        canvas_timeterms.draw()
        toolbar_timeterms = NavigationToolbar2Tk(canvas_timeterms, self.frame_timeterms)
        toolbar_timeterms.update()
        canvas_timeterms._tkcanvas.pack()
        self.ax_timeterms = self.fig_timeterms.add_subplot(111)
        self.fig_timeterms.patch.set_facecolor('#F0F0F0')
        self.ax_timeterms.set_title("Time-terms velocity model")
        self.ax_timeterms.set_xlabel("POSITION [m]")
        self.ax_timeterms.set_ylabel("DEPTH [m]")
        self.ax_timeterms.grid(lw = .5, alpha = .5)
        self.ax_timeterms.set_aspect("equal")
        self.ax_timeterms.spines['right'].set_visible(False)
        self.ax_timeterms.spines['top'].set_visible(False)
        self.ax_timeterms.yaxis.set_ticks_position('left')
        self.ax_timeterms.xaxis.set_ticks_position('bottom')

        self.frame_tomography = Frame(self.frame_plots)
        self.frame_tomography.grid(row = 1, column = 1, sticky = "NSWE")
        self.fig_tomography = plt.figure(figsize = (9.5,3.7))
        canvas_tomography = FigureCanvasTkAgg(self.fig_tomography, self.frame_tomography)
        canvas_tomography.draw()
        toolbar_tomography = NavigationToolbar2Tk(canvas_tomography, self.frame_tomography)
        toolbar_tomography.update()
        canvas_tomography._tkcanvas.pack()
        self.ax_tomography = self.fig_tomography.add_subplot(111)
        self.fig_tomography.patch.set_facecolor('#F0F0F0')
        self.ax_tomography.set_title("Tomography velocity model")
        self.ax_tomography.set_xlabel("POSITION [m]")
        self.ax_tomography.set_ylabel("DEPTH [m]")
        self.ax_tomography.grid(lw = .5, alpha = .5)
        self.ax_tomography.set_aspect("equal")
        self.ax_tomography.spines['right'].set_visible(False)
        self.ax_tomography.spines['top'].set_visible(False)
        self.ax_tomography.yaxis.set_ticks_position('left')
        self.ax_tomography.xaxis.set_ticks_position('bottom')

        self.frame_plots.tkraise()
      
    def createProject(self):

        self.projPath = filedialog.askdirectory()
        
        if self.projPath:
            
            projName = simpledialog.askstring("Refrapick","Enter the name of the project to be created:")
            
            if not path.exists(self.projPath+"/"+projName):
                
                makedirs(self.projPath+"/"+projName)
                local = self.projPath+"/"+projName+"/"
                makedirs(local+"data")
                self.p_data = local+"data/"
                makedirs(local+"picks")
                self.p_picks = local+"picks/"
                makedirs(local+"models")
                self.p_models = local+"models/"
                makedirs(local+"gps")
                self.p_gps = local+"gps/"
                self.projPath = local
                self.projReady = True
                self.createPanels()
                messagebox.showinfo(title="Refrapick", message="Successfully created the project!")
                self.statusLabel.configure(text="Project path ready!",font=("Arial", 11))
                
            else:
                
                messagebox.showinfo(title="Refrapick", message="A project was detected, please choose another name or directory!")

    def loadProject(self):

        self.projPath = filedialog.askdirectory()
        
        if self.projPath:
            
            if path.exists(self.projPath+"/"+"data") and \
            path.exists(self.projPath+"/"+"picks") and \
            path.exists(self.projPath+"/"+"models") and \
            path.exists(self.projPath+"/"+"gps"):

                self.p_data = self.projPath+"/"+"data/"
                self.p_picks = self.projPath+"/"+"picks/"
                self.p_models = self.projPath+"/"+"models/"
                self.p_gps = self.projPath+"/"+"gps/"
                self.projReady = True
                self.createPanels()
                messagebox.showinfo(title="Refrapick", message="Successfully loaded the project path!")
                self.statusLabel.configure(text="Project path ready!",font=("Arial", 11))
                
            else: messagebox.showerror(title="Refrapick", message="Not all folders were detected!\nPlease, check the structure of the selected project.")

    def loadPick(self):
        
        if self.projReady:

            pickFile = filedialog.askopenfilename(title='Open', initialdir = self.projPath+"/picks/", filetypes=[('Pick file', '*.sgt')])

            if pickFile:

                self.data_pg = pg.DataContainer(pickFile, 's g')

                with open(pickFile, "r") as file:

                    lines = file.readlines()
                    npoints = int(lines[0].split()[0])
                    sgx = [float(i.split()[0]) for i in lines[2:2+npoints]]
                    sgz = [float(i.split()[1]) for i in lines[2:2+npoints]]
                    sgtindx = lines.index("#s g t\n")
                    s = [int(i.split()[0]) for i in lines[sgtindx+1:]]
                    g = [int(i.split()[1]) for i in lines[sgtindx+1:]]
                    t = [float(i.split()[2]) for i in lines[sgtindx+1:]]
                    sx = [sgx[i-1] for i in s]
                    gx = [sgx[i-1] for i in g]
                    self.gx = gx
                    self.sgx = sgx
                    self.sgz = sgz

                    for i,src in enumerate(list(set(sx))):
    
                        self.sources.append(src)
                        self.xdata.append([])
                        self.tdata.append([])
                        self.dataArts.append([])
                        sourcePlot = self.ax_data.scatter(src,0,c="y",edgecolor="k",s=100,marker="*",zorder=99)
                        self.data_sourcesArts.append(sourcePlot)

                        for j,x in enumerate(gx):

                            if sx[j] == src:

                                self.xdata[i].append(x)
                                self.tdata[i].append(t[j])
                                dataPlot = self.ax_data.scatter(x,t[j],facecolors='none',edgecolor="k",picker=5,zorder=99)
                                self.dataArts[i].append(dataPlot)
                            
                        self.ax_data.plot(self.xdata[i], self.tdata[i], c = "k")

                    self.fig_data.canvas.draw()

    def clearTomoPlot(self):

        #self.ax_tomography.cla()
        self.fig_tomography.clf()
        self.ax_tomography = self.fig_tomography.add_subplot(111)
        self.fig_tomography.patch.set_facecolor('#F0F0F0')
        self.ax_tomography.set_title("Tomography velocity model")
        self.ax_tomography.set_xlabel("POSITION [m]")
        self.ax_tomography.set_ylabel("DEPTH [m]")
        self.ax_tomography.grid(lw = .5, alpha = .5)
        self.ax_tomography.set_aspect("equal")
        self.ax_tomography.spines['right'].set_visible(False)
        self.ax_tomography.spines['top'].set_visible(False)
        self.ax_tomography.yaxis.set_ticks_position('left')
        self.ax_tomography.xaxis.set_ticks_position('bottom')
        self.tomoPlot = False
        self.fig_tomography.canvas.draw()
                
    def runTomography(self):

        if self.data_pg:

            self.mgr = TravelTimeManager()

            tomoWindow = Toplevel(self)
            tomoWindow.title('Refrainv - Tomography')
            tomoWindow.configure(bg = "#F0F0F0")
            tomoWindow.geometry("280x610")
            tomoWindow.resizable(0,0)
            tomoWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

            def viewMesh():

                maxDepth = float(maxDepth_entry.get())
                paraDX = float(paraDX_entry.get())
                paraMaxCellSize = float(paraMaxCellSize_entry.get())
                self.tomoMesh = self.mgr.createMesh(data=self.data_pg,paraDepth=maxDepth,paraDX=paraDX,paraMaxCellSize=paraMaxCellSize)

                meshWindow = Toplevel(self)
                meshWindow.title('Refrainv - Mesh')
                meshWindow.configure(bg = "#F0F0F0")
                #meshWindow.geometry("1024x768")
                meshWindow.resizable(0,0)
                meshWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

                frame = Frame(meshWindow)
                frame.grid(row = 0, column = 0)
                fig = plt.figure(figsize = (12,6))#.2,8.62))
                fig.patch.set_facecolor('#F0F0F0')
                canvas = FigureCanvasTkAgg(fig, frame)
                canvas.draw()
                toolbar = NavigationToolbar2Tk(canvas, frame)
                toolbar.update()
                canvas._tkcanvas.pack()
                
                ax = fig.add_subplot(111)
                ax.set_ylabel("POSITION [m]")
                ax.set_xlabel("DEPTH [m]")
                ax.grid(lw = .5, alpha = .5)

                #vel = ra.paraModel()
                pg.show(self.tomoMesh, ax = ax)
                #pg.viewer.mpl.drawSensors(ax, data.sensorPositions(), diam=0.5, color="k")
                ax.set_xlabel('Distance (m)')
                ax.set_ylabel('Elevation (m)')
                ax.set_title('Mesh for traveltimes tomography')

                ax.set_aspect("equal")
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')

                fig.canvas.draw()
                meshWindow.tkraise()
                #print(m.dimension)
                #print(m.yMin())
                #print(m.yMax())

            def runInversion():

                if self.tomoPlot:

                    self.clearTomoPlot()
                    
                if self.tomoMesh == False:

                    maxDepth = float(maxDepth_entry.get())
                    paraDX = float(paraDX_entry.get())
                    paraMaxCellSize = float(paraMaxCellSize_entry.get())
                    self.tomoMesh = self.mgr.createMesh(data=self.data_pg,paraDepth=maxDepth,paraDX=paraDX,paraMaxCellSize=paraMaxCellSize)

                lam = float(lam_entry.get())
                zWeigh = float(zWeigh_entry.get())
                vTop = float(vTop_entry.get())
                vBottom = float(vBottom_entry.get())
                minVelLimit = float(minVelLimit_entry.get())
                maxVelLimit = float(maxVelLimit_entry.get())
                secNodes = int(secNodes_entry.get())
                maxIter = int(maxIter_entry.get())
                    
                vest = self.mgr.invert(data=self.data_pg,mesh=self.tomoMesh,verbose=False,lam=lam,zWeight=zWeigh,useGradient=True,
                               vTop=vTop,vBottom=vBottom,maxIter=maxIter,limits=[minVelLimit,maxVelLimit],secNodes=secNodes)
                
                plotContourModel()

            def plotContourModel():
   
                xzv = column_stack((self.mgr.paraDomain.cellCenters(), self.mgr.model))
                x = (xzv[:,0])
                z = (xzv[:,1])
                v = (xzv[:,3])
                
                nx = int(xngrid_entry.get())
                ny = int(yngrid_entry.get())
                x_grid = linspace(min(x), max(x), nx)
                y_grid = linspace(min(z), max(z), ny)
                xi,zi = meshgrid(x_grid,y_grid)
                vi = griddata((x, z), v,(xi,zi), method = 'linear')

                self.ax_tomography.plot(self.sgx, self.sgz, c= "k", lw = 1.5)
                
                cm = self.ax_tomography.contourf(xi, zi, vi, levels=30,
                                    cmap="jet_r", extend="both")

                divider = make_axes_locatable(self.ax_tomography)
                cax = divider.append_axes("right", size="2%", pad=0.05)

                cbar = self.fig_tomography.colorbar(cm,orientation="vertical", label = "[m/s]",
                             format='%d',cax=cax)

                xblank = self.sgx+[self.sgx[-1],self.sgx[0]]
                zblank = self.sgz+[self.tomoMesh.yMin(),self.tomoMesh.yMin()]
                limits = [(i,j) for i,j in zip(xblank,zblank)]
                
                clippath = Path(limits)
                patch = PathPatch(clippath, facecolor='none', alpha = 0)
                self.ax_tomography.add_patch(patch)

                patch = PathPatch(clippath, facecolor='none', alpha = 0)
                self.ax_tomography.add_patch(patch)

                for c in cm.collections:
                    c.set_clip_path(patch)

                self.mgr.drawRayPaths(self.ax_tomography,color="k")
                self.ax_tomography.set_xlim(min(self.sgx),max(self.sgx))
                self.fig_tomography.canvas.draw()
                self.tomoPlot = True
                self.showFit()
                tomoWindow.destroy()
            
            Label(tomoWindow, text="Mesh options", font=("Arial", 11)).grid(row=0,column=0,columnspan=2,pady=10,sticky="E")
            
            Label(tomoWindow, text = "Maximum depth").grid(row=1,column=0,pady=5,sticky="E")
            maxDepth_entry = Entry(tomoWindow,width=6)
            maxDepth_entry.grid(row=1,column=1,pady=5)
            maxDepth_entry.insert(0,str(int((self.gx[-1]-self.gx[0])*0.4)))

            Label(tomoWindow, text = "# of nodes between receivers").grid(row=2,column=0,pady=5,sticky="E")
            paraDX_entry = Entry(tomoWindow,width=6)
            paraDX_entry.grid(row=2,column=1,pady=5)
            paraDX_entry.insert(0,"0.33")

            Label(tomoWindow, text = "Maximum cell size").grid(row=3,column=0,pady=5,sticky="E")
            paraMaxCellSize_entry = Entry(tomoWindow,width=6)
            paraMaxCellSize_entry.grid(row=3,column=1,pady=5)
            paraMaxCellSize_entry.insert(0,str((self.gx[1]-self.gx[0])))
            
            button = Button(tomoWindow, text="View mesh", command=viewMesh).grid(row=4,column=0,columnspan=2,pady=5,sticky="E")

            Label(tomoWindow, text="Inversion options", font=("Arial", 11)).grid(row=5,column=0,columnspan=2,pady=10,sticky="E")
            
            Label(tomoWindow, text = "Smoothing (lam)").grid(row=6,column=0,pady=5,sticky="E")
            lam_entry = Entry(tomoWindow,width=6)
            lam_entry.grid(row=6,column=1,pady=5)
            lam_entry.insert(0,"50")

            Label(tomoWindow, text = "Vertical to horizontal smoothing (zweigh)").grid(row=7,column=0,pady=5,sticky="E")
            zWeigh_entry = Entry(tomoWindow,width=6)
            zWeigh_entry.grid(row=7,column=1,pady=5)
            zWeigh_entry.insert(0,"0.2")

            Label(tomoWindow, text = "Minimum velocity (top of the model)").grid(row=8,column=0,pady=5,sticky="E")
            vTop_entry = Entry(tomoWindow,width=6)
            vTop_entry.grid(row=8,column=1,pady=5)
            vTop_entry.insert(0,"300")
            
            Label(tomoWindow, text = "Maximum velocity (bottom of the model)").grid(row=9,column=0,pady=5,sticky="E")
            vBottom_entry = Entry(tomoWindow,width=6)
            vBottom_entry.grid(row=9,column=1,pady=5)
            vBottom_entry.insert(0,"3000")

            Label(tomoWindow, text = "Minimum velocity limit").grid(row=10,column=0,pady=5,sticky="E")
            minVelLimit_entry = Entry(tomoWindow,width=6)
            minVelLimit_entry.grid(row=10,column=1,pady=5)
            minVelLimit_entry.insert(0,"100")

            Label(tomoWindow, text = "Maximum velocity limit").grid(row=11,column=0,pady=5,sticky="E")
            maxVelLimit_entry = Entry(tomoWindow,width=6)
            maxVelLimit_entry.grid(row=11,column=1,pady=5)
            maxVelLimit_entry.insert(0,"4000")

            Label(tomoWindow, text = "# of secondary nodes").grid(row=12,column=0,pady=5,sticky="E")
            secNodes_entry = Entry(tomoWindow,width=6)
            secNodes_entry.grid(row=12,column=1,pady=5)
            secNodes_entry.insert(0,"3")

            Label(tomoWindow, text = "Maximum # of iterations").grid(row=13,column=0,pady=5,sticky="E")
            maxIter_entry = Entry(tomoWindow,width=6)
            maxIter_entry.grid(row=13,column=1,pady=5)
            maxIter_entry.insert(0,"20")

            Label(tomoWindow, text="Contour plot options", font=("Arial", 11)).grid(row=14,column=0,columnspan=2,pady=10,sticky="E")
            
            Label(tomoWindow, text = "# of nodes for gridding (x)").grid(row=15,column=0,pady=5,sticky="E")
            xngrid_entry = Entry(tomoWindow,width=6)
            xngrid_entry.grid(row=15,column=1,pady=5)
            xngrid_entry.insert(0,"1000")

            Label(tomoWindow, text = "# of nodes for gridding (y)").grid(row=16,column=0,pady=5,sticky="E")
            yngrid_entry = Entry(tomoWindow,width=6)
            yngrid_entry.grid(row=16,column=1,pady=5)
            yngrid_entry.insert(0,"1000")
            
            button = Button(tomoWindow, text="Run inversion", command=runInversion).grid(row=17,column=0,columnspan=2,pady=5,sticky="E")

            tomoWindow.tkraise()

    def showFit(self):

        if self.tomoPlot:

            fitWindow = Toplevel(self)
            fitWindow.title('Refrainv - Fit')
            fitWindow.configure(bg = "#F0F0F0")
            fitWindow.resizable(0,0)
            fitWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

            frame = Frame(fitWindow)
            frame.grid(row = 0, column = 0)
            fig = plt.figure(figsize = (14.2,8.62))
            fig.patch.set_facecolor('#F0F0F0')
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, frame)
            toolbar.update()
            canvas._tkcanvas.pack()
            
            ax_fitTimeterms = fig.add_subplot(121)
            ax_fitTimeterms.set_ylabel("TRAVELTIME [s]")
            ax_fitTimeterms.set_xlabel("POSITION [m]")
            ax_fitTimeterms.grid(lw = .5, alpha = .5)
            ax_fitTimeterms.set_title("Time-terms inversion fit")

            ax_fitTomography = fig.add_subplot(122)
            
            pg.physics.traveltime.drawFirstPicks(ax_fitTomography, self.data_pg, marker="o", lw = 0)
            pg.physics.traveltime.drawFirstPicks(ax_fitTomography, self.data_pg, tt= self.mgr.inv.response, marker="", linestyle = "--")

            for art in ax_fitTomography.get_lines(): art.set_color("k")

            legend_elements = [Line2D([0], [0], marker='o', color='k', label='Observed data', markerfacecolor='k', markersize=7),
                               Line2D([0], [0], color='k', lw=1, ls = "--", label='Model response')]
                   
            
            ax_fitTomography.legend(handles=legend_elements, loc='best')
            ax_fitTomography.set_ylabel("TRAVELTIME [s]")
            ax_fitTomography.set_xlabel("POSITION [m]")
            ax_fitTomography.grid(lw = .5, alpha = .5)
            ax_fitTomography.set_title("Tomography inversion fit\n%d iterations | RRMSE = %.2f%%"%(self.mgr.inv.maxIter,self.mgr.inv.relrms())) #mgr.absrms() mgr.chi2()
       
            fig.canvas.draw()
            fitWindow.tkraise()
        
app = Refrainv()
app.mainloop()




