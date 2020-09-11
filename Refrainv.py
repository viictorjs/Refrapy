from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import os                                                                              
import numpy as np
import sys
import random
from scipy.interpolate import interp1d, interp2d, griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial import ConvexHull
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import warnings
from tkinter import *
from tkinter import filedialog, messagebox
import datetime
from pygimli.physics import Refraction
import pygimli as pg
from matplotlib.colors import LogNorm
import matplotlib.colors

warnings.filterwarnings('ignore') 

class Sisref(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row = 0, column = 0, sticky = NSEW)
        master.geometry("1360x768")
        master.resizable(0,0)
        #master.protocol("WM_DELETE_WINDOW", self.fechar)
        master.title('REFRAINV')
        menuBar = Menu(master)
        fileMenu = Menu(master, tearoff=0)
        ttMenu = Menu(master, tearoff=0)
        tomoMenu = Menu(master, tearoff=0)
        layerIntMenu = Menu(master, tearoff=0)
        createpygimli = Menu(master, tearoff=0)
        tomoinversion = Menu(master, tearoff=0)
        tomoVMplot = Menu(master, tearoff=0)
        tomocmap = Menu(master, tearoff=0)
        editTTtomo = Menu(master, tearoff=0)
        runInvMenu = Menu(master, tearoff=0)
        editTT = Menu(master, tearoff=0)
        TTplot = Menu(master, tearoff=0)
        VMplot = Menu(master, tearoff=0)
        TTcolors = Menu(master, tearoff=0)
        VMcolors = Menu(master, tearoff=0)
        helpMenu = Menu(master, tearoff=0)

        menuBar.add_cascade(label = 'File', menu = fileMenu)
        fileMenu.add_cascade(label='Open travel times file',
                                      command= lambda: print(""))
        fileMenu.add_cascade(label='Save results',
                                      command= lambda: print(""))
        fileMenu.add_cascade(label='Restart all analysis',
                                      command= lambda: print(""))
        fileMenu.add_separator()
        fileMenu.add_cascade(label='Exit',
                                      command= lambda: print(""))
        
        menuBar.add_cascade(label = 'Time-term analysis', menu = ttMenu)
        ttMenu.add_cascade(label='Layer interpretation', menu = layerIntMenu)
        layerIntMenu.add_command(label="Star/stop layer assignment", command = lambda: print(""))
        layerIntMenu.add_separator()
        layerIntMenu.add_command(label="Layer 1", command = lambda: print(""))
        layerIntMenu.add_command(label="Layer 2", command = lambda: print(""))
        layerIntMenu.add_command(label="Layer 3", command = lambda: print(""))
        layerIntMenu.add_separator()
        layerIntMenu.add_command(label="Clear assignmanets", command = lambda: print(""))
        ttMenu.add_cascade(label='Inversion', menu = runInvMenu)
        runInvMenu.add_command(label="Use elevation file", command = lambda: print(""))
        runInvMenu.add_separator()
        runInvMenu.add_command(label="Run default inversion", command = lambda: print(""))
        runInvMenu.add_command(label="Run inversion choosing regularization parameter", command = lambda: print(""))
        ttMenu.add_cascade(label='Edit travel times', menu = editTT)
        editTT.add_command(label="Open travel times file", command = lambda: print(""))
        editTT.add_command(label="Save travel times file", command = lambda: print(""))
        ttMenu.add_separator()
        ttMenu.add_cascade(label='Travel-times plot', menu = TTplot)
        TTplot.add_cascade(label='Travel-times color', menu = TTcolors)
        TTcolors.add_command(label="Use colors", command = self.tt_TTcolors)
        TTcolors.add_command(label="Black", command = self.tt_TTblack)
        TTplot.add_separator()
        TTplot.add_command(label="Show/hide sources", command = self.tt_TTshowS)
        TTplot.add_command(label="Show/hide grid", command = self.tt_TTshowGrid)
        ttMenu.add_cascade(label='Velocity model plot', menu = VMplot)
        VMplot.add_cascade(label='Layer colors', menu = VMcolors)
        VMcolors.add_command(label="Use colors", command = self.tt_LayerColors)
        VMcolors.add_command(label="Black", command = self.tt_LayerBlack)
        VMplot.add_separator()
        VMplot.add_command(label="Show/hide sources", command = self.tt_VMshowS)
        VMplot.add_command(label="Show/hide geophones", command = self.tt_VMshowG)
        VMplot.add_command(label="Show/hide grid", command = self.tt_VMshowGrid)
        ttMenu.add_separator()
        ttMenu.add_command(label="Save analysis results", command = self.tt_save)
        ttMenu.add_command(label="Restart analysis", command = self.restart)

        menuBar.add_cascade(label = 'Tomography analysis', menu = tomoMenu)
        tomoMenu.add_cascade(label='Create pyGIMLi travel-times file', command = self.tomo_create)
        tomoMenu.add_cascade(label='Inversion', menu = tomoinversion)
        tomoinversion.add_command(label="Run inversion", command = self.tomo_invert)
        tomoinversion.add_separator()
        tomoinversion.add_command(label="Load parameters", command = self.tomo_loadParams)
        tomoinversion.add_separator()
        tomoinversion.add_command(label="Show fit", command = self.tomo_showFit)
        tomoMenu.add_cascade(label='Edit travel-times', menu = editTTtomo)
        editTTtomo.add_command(label="Open travel-times file", command = self.tomo_editTT)
        editTTtomo.add_command(label="Save travel-times file", command = self.tomo_saveTT)
        tomoMenu.add_separator()
        tomoMenu.add_cascade(label='Velocity model plot', menu = tomoVMplot)
        tomoVMplot.add_cascade(label='Colormap', menu = tomocmap)
        tomocmap.add_command(label="jet", command = self.tomo_cmapJet)
        tomocmap.add_command(label="gist rainbow", command = self.tomo_cmapGistr)
        tomocmap.add_command(label="gist ncar", command = self.tomo_cmapGistn)
        tomocmap.add_command(label="nipy spectral", command = self.tomo_cmapNipys)
        tomocmap.add_command(label="brw", command = self.tomo_cmapbrw)
        tomocmap.add_command(label="greys", command = self.tomo_cmapGreys)
        tomoVMplot.add_separator()
        tomoVMplot.add_command(label="Show triangular mesh model", command = self.tomo_triangular)
        tomoVMplot.add_command(label="Show interpolated model", command = self.tomo_interpolated)
        tomoVMplot.add_separator()
        tomoVMplot.add_command(label="1D profile", command = self.tomo_profile)
        tomoVMplot.add_separator()
        tomoVMplot.add_command(label="Plot time-terms results", command = self.tomo_usett)
        tomoVMplot.add_separator()
        tomoVMplot.add_command(label="Show/hide sources", command = lambda: print(""))
        tomoVMplot.add_command(label="Show/hide geophones", command = lambda: print(""))
        tomoVMplot.add_command(label="Show/hide ray path", command = self.tomo_showRP)
        tomoVMplot.add_command(label="Show/hide grid", command = lambda: print(""))
        tomoMenu.add_separator()
        tomoMenu.add_cascade(label='Save analysis result',command= self.tomo_save)
        tomoMenu.add_cascade(label='Restart analysis',command= self.restart)
        menuBar.add_cascade(label = 'Help', menu = helpMenu)
        helpMenu.add_cascade(label='Tutorial',command= lambda: print(""))
        helpMenu.add_cascade(label='Report a bug',command= lambda: print(""))
        helpMenu.add_cascade(label='Credits',command= lambda: print(""))
        
        
        master.configure(menu=menuBar)

        plt.rcParams.update({'font.size': 8})
        self.tt_frame1 = Frame(self)
        self.tt_frame1.grid(row = 1, column = 0, sticky = NSEW)
        self.tt_fig1 = plt.figure(figsize = (6.85,3.65))
        self.tt_ax1 = self.tt_fig1.add_subplot(111)
        tt_tela1 = FigureCanvasTkAgg(self.tt_fig1, self.tt_frame1)
        tt_tela1.draw()
        tt_tela1.get_tk_widget().pack(fill='both', expand=True)
        tt_toolbar1 = NavigationToolbar2Tk(tt_tela1, self.tt_frame1)
        tt_toolbar1.update()
        tt_tela1._tkcanvas.pack(fill='both', expand=True)

        self.tt_frame2 = Frame(self)
        self.tt_frame2.grid(row = 1, column = 2, sticky = NSEW)
        self.tt_fig2 = plt.figure(figsize = (6.85,3.65), facecolor = "white")
        self.tt_ax2 = self.tt_fig2.add_subplot(111)
        tt_tela2 = FigureCanvasTkAgg(self.tt_fig2, self.tt_frame2)
        tt_tela2.draw()
        tt_tela2.get_tk_widget().pack(fill='both', expand=True)
        tt_toolbar2 = NavigationToolbar2Tk(tt_tela2, self.tt_frame2)
        tt_toolbar2.update()
        tt_tela2._tkcanvas.pack(fill='both', expand=True)

        self.tt_frame3 = Frame(self)
        self.tt_frame3.grid(row = 2, column = 0, columnspan=3, sticky = NSEW)
        self.tt_fig3 = plt.figure(figsize = (13.7,3.04))
        self.tt_ax3 = self.tt_fig3.add_subplot(111)
        self.tt_ax3.set_aspect("equal")
        tt_tela3 = FigureCanvasTkAgg(self.tt_fig3, self.tt_frame3)
        tt_tela3.draw()
        tt_tela3.get_tk_widget().pack(fill='both', expand=True)
        tt_toolbar3 = NavigationToolbar2Tk(tt_tela3, self.tt_frame3)
        tt_toolbar3.update()
        tt_tela3._tkcanvas.pack(fill='both', expand=True)

        #---------------

        self.tomo_frame1 = Frame(self)
        self.tomo_frame1.grid(row = 1, column = 0, sticky = NSEW)
        self.tomo_fig1 = plt.figure(figsize = (6.85,3.65))
        self.tomo_ax1 = self.tomo_fig1.add_subplot(111)
        tomo_tela1 = FigureCanvasTkAgg(self.tomo_fig1, self.tomo_frame1)
        tomo_tela1.draw()
        tomo_tela1.get_tk_widget().pack(fill='both', expand=True)
        tomo_toolbar1 = NavigationToolbar2Tk(tomo_tela1, self.tomo_frame1)
        tomo_toolbar1.update()
        tomo_tela1._tkcanvas.pack(fill='both', expand=True)

        self.tomo_frame2 = Frame(self)
        self.tomo_frame2.grid(row = 1, column = 2, sticky = NSEW)
        self.tomo_fig2 = plt.figure(figsize = (6.85,3.65))
        self.tomo_ax2 = self.tomo_fig2.add_subplot(111)
        tomo_tela2 = FigureCanvasTkAgg(self.tomo_fig2, self.tomo_frame2)
        tomo_tela2.draw()
        tomo_tela2.get_tk_widget().pack(fill='both', expand=True)
        tomo_toolbar2 = NavigationToolbar2Tk(tomo_tela2, self.tomo_frame2)
        tomo_toolbar2.update()
        tomo_tela2._tkcanvas.pack(fill='both', expand=True)

        self.tomo_frame3 = Frame(self)
        self.tomo_frame3.grid(row = 2, column = 0, columnspan=3, sticky = NSEW)
        self.tomo_fig3 = plt.figure(figsize = (13.7,3.04))
        self.tomo_ax3 = self.tomo_fig3.add_subplot(111)
        self.tomo_ax3.set_aspect("equal")
        tomo_tela3 = FigureCanvasTkAgg(self.tomo_fig3, self.tomo_frame3)
        tomo_tela3.draw()
        tomo_tela3.get_tk_widget().pack(fill='both', expand=True)
        tomo_toolbar3 = NavigationToolbar2Tk(tomo_tela3, self.tomo_frame3)
        tomo_toolbar3.update()
        tomo_tela3._tkcanvas.pack(fill='both', expand=True)

        self.tomo_frame4 = Frame(self)
        self.tomo_frame4.grid(row = 2, column = 0, columnspan=3, sticky = NSEW)
        self.tomo_fig4 = plt.figure(figsize = (13.7,3.04))
        self.tomo_ax4 = self.tomo_fig4.add_subplot(111)
        self.tomo_ax4.set_aspect("equal")
        tomo_tela4 = FigureCanvasTkAgg(self.tomo_fig4, self.tomo_frame4)
        tomo_tela4.draw()
        tomo_tela4.get_tk_widget().pack(fill='both', expand=True)
        tomo_toolbar4 = NavigationToolbar2Tk(tomo_tela4, self.tomo_frame4)
        tomo_toolbar4.update()
        tomo_tela4._tkcanvas.pack(fill='both', expand=True)

        toolbar_frame = Frame(self)
        toolbar_frame.grid(row = 0, column = 0, columnspan=3, sticky = NSEW)
        self.img_abrir = PhotoImage(file="%s/imagens/abrir.gif"%os.getcwd())
        self.img_salvar = PhotoImage(file="%s/imagens/salvar.gif"%os.getcwd())
        self.img_proximo = PhotoImage(file="%s/imagens/proximo.gif"%os.getcwd())
        self.img_voltar = PhotoImage(file="%s/imagens/voltar.gif"%os.getcwd())
        self.img_camadas = PhotoImage(file="%s/imagens/camadas.gif"%os.getcwd())
        self.img_edit = PhotoImage(file="%s/imagens/edit.gif"%os.getcwd())
        self.img_L1 = PhotoImage(file="%s/imagens/layer1.gif"%os.getcwd())
        self.img_L2 = PhotoImage(file="%s/imagens/layer2.gif"%os.getcwd())
        self.img_L3 = PhotoImage(file="%s/imagens/layer3.gif"%os.getcwd())
        self.img_vm = PhotoImage(file="%s/imagens/vm.gif"%os.getcwd())
        self.img_limpar = PhotoImage(file="%s/imagens/limpar.gif"%os.getcwd())
        self.img_topo = PhotoImage(file="%s/imagens/topo.gif"%os.getcwd())
        self.img_editOK = PhotoImage(file="%s/imagens/editOK.gif"%os.getcwd())
        self.img_star = PhotoImage(file="%s/imagens/star.gif"%os.getcwd())
        self.img_geophone = PhotoImage(file="%s/imagens/geophone.gif"%os.getcwd())
        self.img_tomogram = PhotoImage(file="%s/imagens/tomogram.gif"%os.getcwd())
        self.img_restart = PhotoImage(file="%s/imagens/restart.gif"%os.getcwd())
        self.img_create = PhotoImage(file="%s/imagens/create.gif"%os.getcwd())
        self.img_inv = PhotoImage(file="%s/imagens/inv.gif"%os.getcwd())
        root.tk.call('wm', 'iconphoto', root._w, self.img_inv) 
        
        Abrir = Button(toolbar_frame, command = self.openTT)
        Abrir.config(image = self.img_abrir)
        Abrir.grid(row=0,column=0,sticky=W)
        Salvar = Button(toolbar_frame, command = lambda: print("ai"))
        Salvar.config(image = self.img_salvar)
        Salvar.grid(row=0,column=1,sticky=W)
        Voltar = Button(toolbar_frame, command = self.back)
        Voltar.config(image = self.img_voltar)
        Voltar.grid(row=0,column=2,sticky=W)
        Proximo = Button(toolbar_frame, command = self.next)
        Proximo.config(image = self.img_proximo)
        Proximo.grid(row=0,column=3,sticky=W)
        Camadas = Button(toolbar_frame, command = self.tt_layerInterpretation)
        Camadas.config(image = self.img_camadas)
        Camadas.grid(row=0,column=4,sticky=W)
        L1 = Button(toolbar_frame, command = self.tt_L1)
        L1.config(image = self.img_L1)
        L1.grid(row=0,column=5,sticky=W)
        L2 = Button(toolbar_frame, command = self.tt_L2)
        L2.config(image = self.img_L2)
        L2.grid(row=0,column=6,sticky=W)
        L3 = Button(toolbar_frame, command = self.tt_L3)
        L3.config(image = self.img_L3)
        L3.grid(row=0,column=7,sticky=W)
        VM = Button(toolbar_frame, command = self.tt_invert)
        VM.config(image = self.img_vm)
        VM.grid(row=0,column=8,sticky=W)
        Edit = Button(toolbar_frame, command = self.tt_editTT)
        Edit.config(image = self.img_edit)
        Edit.grid(row=0,column=9,sticky=W)
        EditOK = Button(toolbar_frame, command = self.tt_saveTT)
        EditOK.config(image = self.img_editOK)
        EditOK.grid(row=0,column=10,sticky=W)
        Limpar = Button(toolbar_frame, command = self.tt_clearInterpretation)
        Limpar.config(image = self.img_limpar)
        Limpar.grid(row=0,column=11,sticky=W)
        #Topo = Button(toolbar_frame, command = self.tt_topo)
        #Topo.config(image = self.img_topo)
        #Topo.grid(row=0,column=12,sticky=W)
        Create = Button(toolbar_frame, command = self.tomo_create)
        Create.config(image = self.img_create)
        Create.grid(row=0,column=12,sticky=W)
        Tomogram = Button(toolbar_frame, command = self.tomo_invert)
        Tomogram.config(image = self.img_tomogram)
        Tomogram.grid(row=0,column=13,sticky=W)
        '''Fonte = Button(toolbar_frame, command = self.tt_topo)
        Fonte.config(image = self.img_star)
        Fonte.grid(row=0,column=14,sticky=W)
        Geofone = Button(toolbar_frame, command = self.tt_topo)
        Geofone.config(image = self.img_geophone)
        Geofone.grid(row=0,column=15,sticky=W)'''
        Restart = Button(toolbar_frame, command = self.restart)
        Restart.config(image = self.img_restart)
        Restart.grid(row=0,column=14,sticky=W)

        self.tt_pltTT = False
        self.tt_vmGrid = True
        self.tt_TTGrid = True
        self.tt_TTSources = True
        self.tt_VMSources = False
        self.tt_VMGeophones = False
        self.cm = False
        self.TTfile = False
        self.TTfile_ext = False
        self.tomo_TTplot = False
        self.tomo_cmap = plt.cm.get_cmap("nipy_spectral")
        self.tt_frame1.tkraise()
        self.tt_frame2.tkraise()
        self.tt_frame3.tkraise()
        self.page = 1

    def openTT(self):
        
        try:
            self.TTfile = filedialog.askopenfilename(title='Open',filetypes=[('Refrapy pick','*.rp'),
                                                                        ('pyGIMLi pick','*.sgt')])                                                     
            filename, file_extension = os.path.splitext(self.TTfile)
            if file_extension == ".rp":
                self.TTfile_ext = ".rp"
                self.tt_openTT()
            elif file_extension == ".sgt":
                self.TTfile_ext = ".sgt"
                self.tomo_openTT()
                
        except:
            pass

    def tomo_interpolated(self):
        if self.cm:
            self.tomo_raise()
            self.tomo_frame3.tkraise()
    
    def tomo_triangular(self):
        if self.cm:
            self.tomo_ax4.cla()
            self.tomo_ax4.set_xlabel("Distance (m)")
            self.tomo_ax4.set_ylabel("Depth (m)")
            self.tomo_ax4.set_title("Velocity model")
            pg.show(self.m, self.vest, label="Velocity [m/s]", cMap = self.tomo_cmap,
                    ax = self.tomo_ax4, colorBar = False, logScale = False)
            self.tomo_raise()
            self.tomo_frame4.tkraise()

    def tomo_showRP(self):
        if self.cm:
            self.ra.showRayPaths(lw=0.75, color = "white", ax = self.tomo_ax3)
            self.ra.showRayPaths(lw=0.75, color = "white", ax = self.tomo_ax4)
            #self.tomo_raise()
            self.tomo_frame4.tkraise()

    def tomo_updateCmap(self):
        if self.cm:
            self.cm.set_cmap(self.tomo_cmap)
            self.tomo_ax4.cla()
            pg.show(self.m, self.vest, label="Velocity [m/s]", cMap = self.tomo_cmap,
                    ax = self.tomo_ax4, colorBar = False, logScale = False)
            self.tomo_fig3.canvas.draw()
            self.tomo_fig4.canvas.draw()
    
    def tomo_cmapNipys(self):
        if self.cm:
            self.tomo_cmap = plt.cm.get_cmap("nipy_spectral")
            self.tomo_updateCmap()


    def tomo_cmapJet(self):
        if self.cm:
            self.tomo_cmap = plt.cm.get_cmap("jet")
            self.tomo_updateCmap()

    def tomo_cmapGistr(self):
        if self.cm:
            self.tomo_cmap = plt.cm.get_cmap("gist_rainbow")
            self.tomo_updateCmap()

    def tomo_cmapGreys(self):
        if self.cm:
            self.tomo_cmap = plt.cm.get_cmap("Greys")
            self.tomo_updateCmap()

    def tomo_cmapbrw(self):
        if self.cm:
            self.tomo_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","red","white"])
            self.tomo_updateCmap()

    def tomo_cmapGistn(self):
        if self.cm:
            self.tomo_cmap = plt.cm.get_cmap("gist_ncar")
            self.tomo_updateCmap()

    def tomo_usett(self):
        if self.tt_pltVM and self.cm:
            if self.layer2:
                self.tomo_ax3.scatter(self.gp, self.depthLayer2, c="k", marker = "x", s = 10)
                self.tomo_ax4.scatter(self.gp, self.depthLayer2, c="k", marker = "x", s = 10)
            if self.layer3:
                self.tomo_ax3.scatter(self.gp, self.depthLayer3, c="k", marker = "x", s = 10)
                self.tomo_ax4.scatter(self.gp, self.depthLayer3, c="k", marker = "x", s = 10)
            self.tomo_fig3.canvas.draw()
            self.tomo_fig4.canvas.draw()
            #self.tomo_raise()

    def tomo_create(self):
        tomo_topoFile = False
        tomo_rpTTfile = False
        if messagebox.askyesno("Refrapy", "Use elevation file?"):
            try:
                tomo_topoFile = filedialog.askopenfilename(title='Open',filetypes=[('Elevation file','*.txt'), ('All files','*.*')])
            except:
                pass
            
            if tomo_topoFile:
                p, e = np.loadtxt(tomo_topoFile, usecols = (0,1), unpack = True)
                messagebox.showinfo('Refrapy','Elevation data loaded successfully!')
        try:
            tomo_rpTTfile = filedialog.askopenfilename(title='Open',filetypes=[('Refrapy pick file','*.rp'), ('All files','*.*')])
        except:
            pass
        if tomo_rpTTfile:
            x, t = np.genfromtxt(tomo_rpTTfile, usecols = (0,1), unpack = True)
            fg = x[1]
            gn = t[0]
            gs = t[1]
            x = np.delete(x,[0,1])
            t = np.delete(t,[0,1])
            sp = []
            for i in range(len(t)):
                if np.isnan(x[i]):
                    sp.append(t[i])
            gp = np.arange(fg,fg+gn*gs,gs)
            sgp = np.sort(np.concatenate((np.arange(fg,fg+gn*gs,gs),np.array(sp))))
            for i in range(len(sgp)):
                try:
                    if sgp[i+1] == sgp[i]:
                        if sgp[i] <= min(gp):
                            sp[sp.index(sgp[i])] = sgp[i]-0.01
                            sgp[i] = sgp[i]-0.01
                        elif sgp[i] >= max(gp):
                            sp[sp.index(sgp[i])] = sgp[i]+0.01
                            sgp[i] = sgp[i]+0.01
                            
                        else:
                            sp[sp.index(sgp[i])] = sgp[i]+0.01
                            sgp[i] = sgp[i]+0.01    
                except:
                    pass
            out_sgtFile = filedialog.asksaveasfilename(title='Save',filetypes=[('pyGIMLi travel-times file', '*.sgt')])
            with open(out_sgtFile+".sgt", "w") as f:
                f.write("%d # shot/geophone points\n#x y\n"%(gn+len(sp)))
                for i in range(len(sgp)):
                    if tomo_topoFile:
                        f.write("%.2f %.2f\n"%(sgp[i], e[i]))
                    else:
                        f.write("%.2f 0\n"%sgp[i])
                f.write("%d # measurements\n#s g t\n"%(len(t)-len(sp)))
                si = np.where(np.isin(np.sort(np.concatenate((np.arange(fg,fg+gn*gs,gs),np.array(sp)))), sp))[0]
                a = 0
                for i in range(len(t)):
                    if a <= len(si)-1:
                        if not np.isnan(x[i]):  
                            f.write("%d %d %.6f\n"%(1+np.where(np.isclose(sgp, sp[a]))[0][0],
                            1+np.where(np.isclose(np.sort(np.concatenate((np.arange(fg,fg+gn*gs,gs),np.array(sp)))), x[i]))[0][-1],
                            t[i]/1000))
                        else:
                            a += 1
            messagebox.showinfo('Refrapy',"pyGIMLI's travel-times file has been created succesfully!")

    def tomo_openTT(self):
        if self.tomo_TTplot:
            messagebox.showinfo('Refrapy','A tomographic analysis is already happening\nTo start a new one, please restart the current analysis.')
        else:
            from pygimli.physics import Refraction
            import pygimli as pg

            data = pg.DataContainer(self.TTfile, 's g')
            ra = Refraction(data)
            ra.showData(ax = self.tomo_ax1)
            self.tomo_ax1.invert_yaxis()
            self.tomo_raise()
            self.pars = []
            self.tomo_TTplot = True
            messagebox.showinfo('Refrapy',"pyGIMLI's travel-times file has been loaded succesfully!")
                
    def tomo_saveTT(self):
        if self.TTfile:
            out_ttFile = filedialog.asksaveasfilename(title='Save',filetypes=[('Refrapy pick', '*.rp')])
            with open(out_ttFile+".sgt",'w') as arqpck:
                arqpck.write("%d %d\n%.2f %.2f\n"%(len(self.sp),self.gn,self.fg,self.gs))
                for i in range(len(self.sp)):
                    for j in range(len(self.datax[i][self.sp[i]])):
                        arqpck.write('%f %f 1\n'%(self.datax[i][self.sp[i]][j],self.datat[i][self.sp[i]][j]*1000))
                    arqpck.write('/ %f\n'%self.sp[i])
            messagebox.showinfo('Refrapy',"Travel-times file has been saved succesfully!")

    def tomo_showFit(self):
        if self.TTfile:
            self.ra.showData(response = self.ra.inv.response(), ax = self.tomo_ax2)
            self.tomo_raise()
    
    def tomo_editTT(self):
        if self.TTfile:
            #self.ra.showData(response = self.ra.inv.response(), ax = self.tomo_ax2)
            try:
                ttFile = filedialog.askopenfilename(title='Open',filetypes=[('Refrapy pick','*.rp'),('All files','*.*')])
            except:
                pass
            if ttFile:
                x, t = np.genfromtxt(ttFile, usecols = (0,1), unpack = True)
                fg = x[1]
                self.fg = fg
                gn = t[0]
                self.gn = gn
                gs = t[1]
                self.gs = gs
                x = np.delete(x,[0,1])
                t = np.delete(t,[0,1])/1000
                sp = []
                for i in range(len(t)):
                    if np.isnan(x[i]):
                        sp.append(t[i])
                sp = np.array(sp)*1000
                self.sp = sp
                self.datax, self.datat = [], []
                artb = []
                for i in range(len(sp)):
                    self.datax.append({sp[i]:[]})
                    self.datat.append({sp[i]:[]})
                    artb.append({sp[i]:[]})
                colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(sp))]
                s = 0
                for i in range(len(t)):
                    if not np.isnan(x[i]):
                        self.datax[s][sp[s]].append(x[i])
                        self.datat[s][sp[s]].append(t[i])
                        if i == 0:
                            b = self.tomo_ax2.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4,zorder=10,
                                           label = "Observed travel-times")
                        else:
                            b = self.tomo_ax2.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4,zorder=10)
                        artb[s][sp[s]].append(b)
                    else:
                        s+=1
                lines = []
                for i in range(len(sp)):
                    self.tomo_ax2.scatter(sp[i],0, marker = "*", c = "yellow", edgecolor = "k", s = 200, zorder=10)
                    l = self.tomo_ax2.plot(self.datax[i][sp[i]],self.datat[i][sp[i]], c = "k", lw = 0.75)
                    lines.append(l)
           
                def onpick(event):
                    self.art = event.artist
                    artx = self.art.get_offsets()[0][0]
                    artt = self.art.get_offsets()[0][1]
                    
                    for i in range(len(sp)):
                        for b in artb[i][sp[i]]:
                            bx = b.get_offsets()[0][0]
                            bt = b.get_offsets()[0][1]
                            if artx == bx and artt == bt:
                                self.arts = sp[i]
                                self.i = i
                                self.arti = np.where(np.array(self.datax[i][sp[i]]) == artx)[0][0]
          
                def onrelease(event):
                    try:
                        self.datat[self.i][self.arts][self.arti] = event.ydata
                        self.art.set_offsets((self.art.get_offsets()[0][0],event.ydata))
                        for i in range(len(sp)):
                            lines[i][0].set_data(self.datax[i][sp[i]],self.datat[i][sp[i]])
                        self.tomo_fig2.canvas.draw()
                    except:
                        pass
                    self.art = None
                    self.arts = None
                    self.i = None
                    self.arti = None

                event = self.tomo_fig2.canvas.mpl_connect('pick_event', onpick)
                event2 = self.tomo_fig2.canvas.mpl_connect('button_release_event', onrelease)
                self.tomo_ax2.legend(loc="best")
                self.tomo_raise()
                messagebox.showinfo('Refrapy','Travel-times file loaded successfully!\nDrag and drop travel-times (circles) to edit\nWhen done, save the results into a new file')

    def tomo_loadParams(self):
        self.pars = []
        tomoParFile = filedialog.askopenfilename(title='Open',filetypes=[('Parameter file','*.txt'),('All files','*.*')])
        if tomoParFile:
            try:
                with open(tomoParFile, "r") as arq:
                    for i in arq:
                        self.pars.append(float(i.split()[1]))
                messagebox.showinfo('Refrapy',"Tomography inversion parameters loaded successfully!")
            except:
                messagebox.showinfo('Refrapy',"Invalid parameters! Please, check the file (in doubt view the Help menu)")

    def tomo_save(self):
        if self.cm:
            now = datetime.datetime.now()
            np.savetxt("tomoXYZ_%s-%s-%s__%sh%s.txt"%(now.day, now.month, now.year, now.hour, now.minute),
                       np.c_[self.tomo_cellsx, self.tomo_cellsy, self.tomo_cellsv], fmt='%.2f')
            messagebox.showinfo('Refrapy',"The velocity tomogram XYZ file has been saved successfully!")

    def tomo_profile(self):
        if True:#self.cm:
            rt = Tk()
            fr = Frame(master = rt)
            fr.grid(row = 4, column = 2, sticky = "w")
            rt.title('REFRAINV') 
            fig = plt.figure()
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, rt)
            canvas.get_tk_widget().grid(row = 0, column = 2, rowspan = 4, sticky='e', padx = 10)
            canvas.draw()
            tb = NavigationToolbar2Tk(canvas, fr)
            tb.update()
            
            vtop, vbottom, vnsamples, vpos = StringVar(),StringVar(),StringVar(),StringVar()
            top = Label(rt, text = 'Top of profile (m)').grid(row = 0, column = 0, sticky='e')
            bottom = Label(rt, text = 'Bottom of profile (m)').grid(row = 1, column = 0, sticky='e')
            nSamples = Label(rt, text = 'Sample number').grid(row = 2, column = 0, sticky='e')
            pos = Label(rt, text = 'Profile position (m)').grid(row = 3, column = 0, sticky='e')

            etop = Entry(rt, textvariable = vtop, width=10)
            etop.grid(row = 0, column = 1, sticky = 'w')
            ebottom = Entry(rt, textvariable = vbottom, width=10)
            ebottom.grid(row = 1, column = 1, sticky = 'w')
            enSamples = Entry(rt, textvariable = vnsamples, width=10)
            enSamples.grid(row = 2, column = 1, sticky = 'w')
            epos = Entry(rt, textvariable = vpos, width=10)
            epos.grid(row = 3, column = 1, sticky = 'w')

            rt.resizable(0,0)

            def plot():
                #try:
                if etop.get() and ebottom.get() and enSamples.get() and epos.get():
                    #mask = ((self.tomo_cellsx >= (p*0.8)) & (self.tomo_cellsx <= (p*1.2)))
                    #f = interp2d(self.tomo_cellsx,self.tomo_cellsy,self.tomo_cellsv, kind='cubic')

                    top_px = self.tomo_ax3.transData.transform((float(epos.get()),float(etop.get())))
                    bottom_px = self.tomo_ax3.transData.transform((float(epos.get()),float(ebottom.get())))
               

                    #x, y = np.linspace(0, 100, int(enSamples.get()))*0+top_px[0], np.linspace(top_px[1], bottom_px[1], int(enSamples.get()))
                
                    
                    xnew = np.linspace(float(ebottom.get()), float(etop.get()), int(enSamples.get()))*0+float(epos.get())
                    ynew = np.linspace(float(etop.get()), float(ebottom.get()), int(enSamples.get()))

                    znew = profile_line(self.zi,top_px,bottom_px)
                                        #(float(epos.get()),float(ebottom.get())),
                                        #(float(epos.get()),float(etop.get())))
                    print(znew)
                    print(len(znew))

                    
                    
                    
                    #znew = scipy.ndimage.map_coordinates(self.zi.T, np.vstack((x,y)))
                    
                    
                    #znew = f(xnew, ynew)
                    ax.cla()
                    ax.set_title('1D velocity profile')    
                    ax.set_xlabel('Velocity (m/s)')
                    ax.set_ylabel('Depth (m)')
                    ax.grid(ls = "--", alpha = 0.75)
                    ax.plot(znew, ynew, c = "k")
                    #ax.plot(znew[np.where(znew > 0)], ynew[np.where(znew > 0)], c = "k")
                    fig.canvas.draw()
                else:
                    messagebox.showinfo('Refrapy',"Please, enter all values before plotting!")
                #except:
                 #   messagebox.showinfo('Refrapy',"Invalid values for profile plotting!")

            def save():
                np.savetxt("teste_1d.txt",znew)
            
            plotp = Button(rt, text = 'Plot', command = plot).grid(row = 4, column = 0)
            savep = Button(rt, text = 'Save', command = save).grid(row = 4, column = 1)
            rt.mainloop()

    def tomo_invert(self):
        if self.TTfile_ext == ".sgt":
            self.tomo_ax3.cla()
            a = np.genfromtxt(self.TTfile, usecols = (0), unpack = True)
            with open(self.TTfile) as f:
                head = [next(f).split() for x in range(2+int(a[0]))][2:]
            data = pg.DataContainer(self.TTfile, 's g')
            ra = Refraction(data)
            self.ra = ra
            if len(self.pars) == 0:
                m = ra.createMesh()
                vest = ra.invert()
            else:
                m = ra.createMesh(paraMaxCellSize=float(self.pars[2]), secNodes=int(self.pars[3]))
                vest = ra.invert(mesh = m, useGradient = True, vtop = self.pars[0], vbottom = self.pars[1],
                                 zWeight=self.pars[4], lam = float(self.pars[6]), verbose = int(self.pars[5]))
                    
                    #except:
                     #   messagebox.showinfo('Refrapy',"Invalid parameters! Please, check the file (in doubt view the Help menu)")
            self.m = m
            self.vest = vest
            rrms = ra.inv.relrms() # relative RMS
            arms = ra.inv.absrms() # Absolute RMS
            messagebox.showinfo('Refrapy',"Relative RMS = %.2f%%\nAbsolute RMS = %.6f ms"%(rrms,1000*arms))
            x = np.array([i for i in pg.x(m.cellCenters())])
            y = np.array([i for i in pg.y(m.cellCenters())])
            v = np.array([i for i in vest])
            self.tomo_cellsx, self.tomo_cellsy, self.tomo_cellsv = x,y,v
            spi = np.unique(ra.dataContainer("s"), return_inverse=False)
            gi = np.unique(ra.dataContainer("g"), return_inverse=False)
            a = np.genfromtxt(self.TTfile, usecols = (0), skip_header = 2, unpack = True)
            sp = [a[:len(spi)+len(gi)][int(i)] for i in spi]
            gp = [a[:len(spi)+len(gi)][int(i)] for i in gi]
            x_grid = np.linspace(x.min(), x.max(), 500)
            y_grid = np.linspace(y.min(), y.max(), 500)
            xi,yi = np.meshgrid(x_grid,y_grid)
            self.xi, self.yi = xi,yi
            zi = griddata((x, y), v,(xi,yi), method='cubic')
            self.zi = zi
            if min(v) < 0:
                vmin = 0
            else:
                vmin = min(v)
            d = ra.getDepth()
            head = [(float(head[i][0]),float(head[i][1])) for i in range(len(head))]
            e = np.array([head[i][1] for i in range(len(head))])
            sgp = np.array([head[i][0] for i in range(len(head))])
            tail = [(head[i][0],max(y)-d) for i in range(len(head))]
            p = head+list(reversed(tail))
            poly = plt.Polygon(p, ec="none", fc="none")
            self.tomo_ax3.add_patch(poly)
            cm = self.tomo_ax3.imshow(zi, cmap = "nipy_spectral", origin='lower', interpolation = 'spline36',
                         vmin = vmin, vmax = max(v),
                         extent=[x.min(),x.max(),y.min(),y.max()], clip_path=poly, clip_on=True)
            pg.show(self.m, self.vest, label="Velocity [m/s]", cMap = self.tomo_cmap,
                    ax = self.tomo_ax4, colorBar = False, logScale = False)
            self.tomo_ax4.set_xlabel("Distance (m)")
            self.tomo_ax4.set_ylabel("Depth (m)")
            self.tomo_ax4.set_title("Velocity model")
            #gx = np.linspace(0,63,24)
            #self.tomo_ax3.plot(gx, [-5+(i*0) for i in range(len(gx))], lw = 1, ls = "--", c = "black")
            #self.tomo_ax3.plot(gx, [-10+(i*0) for i in range(len(gx))],lw = 1, ls = "--", c = "black")
            #cm = self.tomo_ax3.imshow(zi, norm=LogNorm(vmin = vmin, vmax= max(v)), cmap = "gist_rainbow", origin='lower', interpolation = 'spline36',
            #             extent=[x.min(),x.max(),y.min(),y.max()], clip_path=poly, clip_on=True)
            self.cm = cm
            ge = [e[np.where(np.array(sgp) == np.array(gp)[i])[0]][0] for i in range(len(gp))]
            se = [e[np.where(np.array(sgp) == np.array(sp)[i])[0]][0] for i in range(len(sp))]
            divider = make_axes_locatable(self.tomo_ax3)
            divider2 = make_axes_locatable(self.tomo_ax4)
            cax = divider.append_axes("right", size="1%", pad=0.05)
            cax2 = divider2.append_axes("right", size="1%", pad=0.05)
            #plt.colorbar(cm,orientation="vertical",aspect =20,
             #            cax = cax, label = "Velocity (m/s)")
            self.tomo_fig3.colorbar(cm,orientation="vertical",aspect =20,
                         cax = cax, label = "Velocity (m/s)")
            self.tomo_fig4.colorbar(cm,orientation="vertical",aspect =20,
                         cax = cax2, label = "Velocity (m/s)")
            self.tomo_ax3.set_xlabel("Distance (m)")
            self.tomo_ax3.set_ylabel("Elevation (m)")
            self.tomo_ax3.set_title("Velocity model")
        
            self.tomo_raise()

    def restart(self):
        self.tt_ax1.cla()
        self.tt_ax2.cla()
        self.tt_ax3.cla()
        self.tt_pltTT = False
        self.tomo_TTplot = False
        self.tt_vmGrid = True
        self.tt_TTGrid = True
        self.tt_TTSources = True
        self.tt_VMSources = False
        self.tt_VMGeophones = False
        self.tomo_ax1.cla()
        self.tomo_ax2.cla()
        self.tomo_ax3.cla()
        self.tomo_ax4.cla()
        self.tomo_fig3.clf()
        self.tomo_fig4.clf()
        self.tomo_ax3 = self.tomo_fig3.add_subplot(111)
        self.tomo_ax3.set_aspect("equal")
        self.tomo_ax4 = self.tomo_fig4.add_subplot(111)
        self.tomo_ax4.set_aspect("equal")
        self.TTfile = False
        self.TTfile_ext = False
        self.pars = []
        self.tt_raise()
        messagebox.showinfo('Refrapy','All analysis have been restarted!')


    def tt_save(self):
        if self.tt_pltVM == True:
            now = datetime.datetime.now()
            with open("timeterms_%s-%s-%s__%sh%s.txt"%(now.day, now.month, now.year, now.hour, now.minute), "w") as arq:
                print(self.depthLayer2)
                if self.tt_topoFile:
                    arq.write("Layer 1\n")
                    arq.write("Velocity = %.2f m/s\n"%self.velocity1)
                    for i in range(len(self.gp)):
                        arq.write("%.2f %.2f\n"%(self.gp[i], self.ge[i]))
                    arq.write("\nLayer 2\n")
                    arq.write("Velocity = %.2f m/s\n"%self.velocity2)
                    for i in range(len(self.gp)):
                        arq.write("%.2f %.2f\n"%(self.gp[i], self.depthLayer2[i]))
                else:
                    arq.write("Layer 1\n")
                    arq.write("Velocity = %.2f m/s\n"%self.velocity1)
                    for i in range(len(self.gp)):
                        arq.write("%.2f 0\n"%self.gp[i])
                    arq.write("\nLayer 2\n")
                    arq.write("Velocity = %.2f m/s\n"%self.velocity2)
                    for i in range(len(self.gp)):
                        arq.write("%.2f %.2f\n"%(self.gp[i], self.depthLayer2[i]))
                    if self.layer3:
                        arq.write("\nLayer 3\n")
                        arq.write("Velocity = %.2f m/s\n"%self.velocity3)
                        for i in range(len(self.gp)):
                            arq.write("%.2f %.2f\n"%(self.gp[i], self.depthLayer3[i]))
            self.tt_fig1.savefig('timeterms_layerInterpretation_%s-%s-%s__%sh%s.png'%(now.day, now.month, now.year, now.hour, now.minute))
            self.tt_fig3.savefig('timeterms_velocityModel_%s-%s-%s__%sh%s.png'%(now.day, now.month, now.year, now.hour, now.minute))
            messagebox.showinfo('Refrapy',"All figures were saved and time-terms analysis results are in timeterms_%s-%s-%s__%sh%s.txt"%(now.day, now.month, now.year, now.hour, now.minute))

    def tt_raise(self):
        self.tt_frame1.tkraise()
        self.tt_frame2.tkraise()
        self.tt_frame3.tkraise()
        self.tt_fig1.canvas.draw()
        self.tt_fig2.canvas.draw()
        self.tt_fig3.canvas.draw()
        self.page = 1

    def tomo_raise(self):
        self.tomo_frame1.tkraise()
        self.tomo_frame2.tkraise()
        self.tomo_frame3.tkraise()
        self.tomo_fig1.canvas.draw()
        self.tomo_fig2.canvas.draw()
        self.tomo_fig3.canvas.draw()
        self.page = 2              

    def back(self):
        if self.page == 2:
            self.tt_raise()
        
    def next(self):
        if self.page == 1:
            self.tomo_raise()

    def tt_VMshowG(self):
        if self.tt_pltVM == True:
            if self.tt_VMGeophones == False:
                self.tt_vmGeophones = []
                if self.tt_topoFile:
                    tt_pltG = self.tt_ax3.scatter(self.gp, self.ge ,marker = 7, color = 'k',
                             edgecolor = "k", s = 100)
                    self.tt_vmGeophones.append(tt_pltG)
                else:
                    tt_pltG = self.tt_ax3.scatter(self.gp, [i*0 for i in range(len(self.gp))],marker = 7, color = 'k',
                             edgecolor = "k", s = 100)
                    self.tt_vmGeophones.append(tt_pltG)
                
                self.tt_VMGeophones = True
            else:
                for i in self.tt_vmGeophones:
                    i.set_alpha(0)
                    self.tt_VMGeophones = False
            self.tt_fig3.canvas.draw()

    def tt_VMshowS(self):
        if self.tt_pltVM == True:
            if self.tt_VMSources == False:
                self.tt_vmSources = []
                if self.tt_topoFile:
                    tt_pltS = self.tt_ax3.scatter(self.sp, self.se ,marker = "*", color = 'yellow',
                             edgecolor = "k", s = 100)
                    self.tt_vmSources.append(tt_pltS)
                else:
                    tt_pltS = self.tt_ax3.scatter(self.sp, [i*0 for i in range(len(self.sp))],marker = "*", color = 'yellow',
                             edgecolor = "k", s = 100)
                    self.tt_vmSources.append(tt_pltS)
                self.tt_VMSources = True
            else:
                for i in self.tt_vmSources:
                    i.set_alpha(0)
                    self.tt_VMSources = False
                    
            self.tt_fig3.canvas.draw()

    def tt_TTshowGrid(self):
        if self.tt_pltTT == True:
            if self.tt_TTGrid == True:
                self.tt_ax1.grid(False)
                self.tt_ax2.grid(False)
                self.tt_TTGrid = False
            else:
                self.tt_ax1.grid(ls = '--', lw = 0.5)
                self.tt_ax2.grid(ls = '--', lw = 0.5)
                self.tt_TTGrid = True
            self.tt_fig1.canvas.draw()
            self.tt_fig2.canvas.draw()

    def tt_TTshowS(self):
        if self.tt_pltTT == True:
            if self.tt_TTSources == True:
                for i in range(len(self.tt_S)):
                    self.tt_S[i].set_alpha(0)
                    self.tt_TTSources = False
            else:
                for i in range(len(self.tt_S)):
                    self.tt_S[i].set_alpha(1)
                    self.tt_TTSources = True
            self.tt_fig1.canvas.draw()
            self.tt_fig2.canvas.draw()

    def tt_VMshowGrid(self):
        if self.tt_pltVM == True:
            if self.tt_vmGrid == True:
                self.tt_ax3.grid(False)
                self.tt_vmGrid = False
            else:
                self.tt_ax3.grid(ls = '--', lw = 0.5)
                self.tt_vmGrid = True
            self.tt_fig3.canvas.draw()
            

    def tt_LayerColors(self):
        if self.tt_pltVM == True:
            self.tt_layer1.set_color("red")
            self.tt_layer2.set_color("green")
            if self.layer3:
                self.tt_layer3.set_color("blue")
            self.tt_ax3.legend(loc="best")
            self.tt_fig3.canvas.draw()

    def tt_LayerBlack(self):
        if self.tt_pltVM == True:
            self.tt_layer1.set_color("lightgrey")
            self.tt_layer2.set_color("grey")
            if self.layer3:
                self.tt_layer3.set_color("black")
            self.tt_ax3.legend(loc="best")
            self.tt_fig3.canvas.draw()

    def tt_TTcolors(self):
        if self.tt_pltTT:
            colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(self.sp))]
            for i in range(len(self.tt_TTlines)):
                self.tt_TTlines[i][0].set_color(colors[i])
            self.tt_fig1.canvas.draw()


    def tt_TTblack(self):
        if self.tt_pltTT:
            for i in range(len(self.tt_TTlines)):
                self.tt_TTlines[i][0].set_color("k")
            self.tt_fig1.canvas.draw()

    def tt_openTT(self):
        
        if self.tt_pltTT:
            messagebox.showinfo('Refrapy','An analysis of travel-time curves is already happening\nTo start a new one, please clear the current analysis.')
            
        else:
            #if ttFile != None:
            x, t = np.genfromtxt(self.TTfile, usecols = (0,1), unpack = True)
            self.fg = x[1]
            self.gn = t[0]
            self.gs = t[1]
            x = np.delete(x,[0,1])
            t = np.delete(t,[0,1])
            self.sp = []
            for i in range(len(t)):
                if np.isnan(x[i]):
                    self.sp.append(t[i])
            self.gp = np.arange(self.fg,self.fg+self.gn*self.gs,self.gs)
            self.tt_ax1.grid(ls = '--', lw = 0.5)
            self.tt_ax1.set_xlabel("Distance (m)")
            self.tt_ax1.set_ylabel("Time (ms)")
            datax, datat = [], []
            self.artb = []
            for i in range(len(self.sp)):
                datax.append({self.sp[i]:[]})
                datat.append({self.sp[i]:[]})
                self.artb.append({self.sp[i]:[]})

            colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(self.sp))]
            
            s = 0
            for i in range(len(t)):
                if not np.isnan(x[i]):
                    datax[s][self.sp[s]].append(x[i])
                    datat[s][self.sp[s]].append(t[i])
                    b = self.tt_ax1.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4)
                    self.artb[s][self.sp[s]].append(b)
                else:
                    s+=1
            self.tt_TTlines = []
            self.tt_S = []
            for i in range(len(self.sp)):
                sPlot = self.tt_ax1.scatter(self.sp[i],0, marker = "*", c = 'white', edgecolor = "k", s = 200)
                self.tt_S.append(sPlot)
                l = self.tt_ax1.plot(datax[i][self.sp[i]],datat[i][self.sp[i]], c = colors[i], lw = 0.75)
                self.tt_TTlines.append(l)
                
            self.tt_fig1.canvas.draw()
            self.tt_topoFile = False
            self.tt_interpretation = False
            self.layer1, self.layer2, self.layer3 = [],[],[]
            self.layer = 1
            self.tt_pltS = False
            self.tt_pltG = False
            self.tt_pltTT = True
            self.tt_pltVM = False
            self.tt_raise()
            messagebox.showinfo('Refrapy','Travel-times file was loaded successfully!')

    def tt_L1(self):
        if self.tt_interpretation:
            self.layer = 1
            self.tt_ax1.set_title('Layer %d interpratation activated!'%self.layer)
            self.tt_fig1.canvas.draw()

    def tt_L2(self):
        if self.tt_interpretation:
            self.layer = 2
            self.tt_ax1.set_title('Layer %d interpratation activated!'%self.layer)
            self.tt_fig1.canvas.draw()

    def tt_L3(self):
        if self.tt_interpretation:
            self.layer = 3
            self.tt_ax1.set_title('Layer %d interpratation activated!'%self.layer)
            self.tt_fig1.canvas.draw()

    def tt_clearInterpretation(self):
        if self.tt_interpretation:
            if messagebox.askyesno("Refrainv", "Clear layer interpretation?"):
                del self.layer1[:]
                del self.layer2[:]
                del self.layer3[:]
                for i in range(len(self.sp)):
                    for b in self.artb[i][self.sp[i]]:
                        b.set_color("white")
                        b.set_edgecolor("k")
                self.tt_fig1.canvas.draw()
                messagebox.showinfo('Refrapy','Layer interpretation was restarted!')
    
    def tt_layerInterpretation(self):

        if self.tt_interpretation == False:
            self.tt_interpretation = True
            self.tt_ax1.set_title('Layer %d interpratation activated!'%self.layer)
                
            def onpick(event):
                art = event.artist
                artx = art.get_offsets()[0][0]
                artt = art.get_offsets()[0][1]

                for i in range(len(self.sp)):
                    if art in self.artb[i][self.sp[i]]:
                        arts = self.sp[i]
                        iS = i 
                        
                if artx >= arts:
                    for b in self.artb[iS][arts]:
                        bx = b.get_offsets()[0][0]
                        iG = np.where(np.array(self.artb[iS][arts]) == b)[0][0]
                        if arts <= bx <= artx:
                            bt = b.get_offsets()[0][1]
                            if self.layer == 1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1:
                                b.set_color("red")
                                self.layer1.append((bx,bt,arts,abs(arts-bx),iS, iG))#geophone_position , arrival_time , source_poisition , offset , index_source , index_geophone
                                if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer2:
                                    self.layer2.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                            elif self.layer == 2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2:
                                b.set_color("lightgreen")
                                self.layer2.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer3:
                                    self.layer3.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                            elif self.layer == 3 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer3:
                                b.set_color("blue")
                                self.layer3.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                
                elif artx <= arts:
                    for b in self.artb[iS][arts]:
                        bx = b.get_offsets()[0][0]
                        iG = np.where(np.array(self.artb[iS][arts]) == b)[0][0]
                        if arts >= bx >= artx:
                            bt = b.get_offsets()[0][1]
                            if self.layer == 1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1:
                                b.set_color("red")
                                self.layer1.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer2:
                                    self.layer2.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                            elif self.layer == 2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2:
                                b.set_color("lightgreen")
                                self.layer2.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer3:
                                    self.layer3.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                            elif self.layer == 3 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer3:
                                b.set_color("blue")
                                self.layer3.append((bx,bt,arts,abs(arts-bx),iS, iG))
                
                self.tt_fig1.canvas.draw()

            def onkey(event):
                if event.key == "1":
                    self.layer = 1
                elif event.key == "2":
                    self.layer = 2
                elif event.key == "3":
                    self.layer = 3
                self.tt_ax1.set_title('Layer %d interpratation activated!'%self.layer)
                
                if event.key == "C" or event.key == "c":
                    if messagebox.askyesno("Refrainv", "Clear layer interpretation?"):
                        del self.layer1[:]
                        del self.layer2[:]
                        del self.layer3[:]
                        for i in range(len(self.sp)):
                            for b in self.artb[i][self.sp[i]]:
                                b.set_color("white")
                                b.set_edgecolor("k")

                self.tt_fig1.canvas.draw()

            self.tt_pickEvent = self.tt_fig1.canvas.mpl_connect('pick_event', onpick)
            self.tt_keyEvent = self.tt_fig1.canvas.mpl_connect('key_press_event', onkey)
            messagebox.showinfo('Refrapy','Layer interpretation is now activated!')
            self.tt_raise()

        else:
            self.tt_fig1.canvas.mpl_disconnect(self.tt_pickEvent)
            self.tt_fig1.canvas.mpl_disconnect(self.tt_keyEvent)
            self.tt_ax1.set_title('Layer interpratation off')
            messagebox.showinfo('Refrapy','Layer interpretation is now off!')
            self.tt_raise()
            self.tt_interpretation = False

    def tt_saveTT(self):
        
        out_ttFile = filedialog.asksaveasfilename(title='Save',filetypes=[('Refrapy pick', '*.rp')])
        with open(out_ttFile+".rp",'w') as arqpck:
            arqpck.write("%d %d\n%.2f %.2f\n"%(len(self.spED),self.gnED,self.fgED,self.gsED))
            for i in range(len(self.spED)):
                for j in range(len(self.dataxED[i][self.spED[i]])):
                    arqpck.write('%f %f 1\n'%(self.dataxED[i][self.spED[i]][j],self.datatED[i][self.spED[i]][j]))
                arqpck.write('/ %f\n'%self.spED[i])
        messagebox.showinfo('Refrapy',"%s was saved!"%out_ttFile)

    def tt_editTT(self):

        try:
            ttFile = filedialog.askopenfilename(title='Open',filetypes=[('Refrapy pick','*.rp'),
                                                                        ('Refrapy pick old','*.gp'),
                                                                ('All files','*.*')])
        except:
            pass

        if ttFile:
            self.tt_ax2.cla()
            x, t = np.genfromtxt(ttFile, usecols = (0,1), unpack = True)
            self.fgED = x[1]
            self.gnED = t[0]
            self.gsED = t[1]
            x = np.delete(x,[0,1])
            t = np.delete(t,[0,1])
            self.spED = []
            for i in range(len(t)):
                if np.isnan(x[i]):
                    self.spED.append(t[i])
            self.spED = np.array(self.spED)
            self.tt_ax2.grid(ls = '--', lw = 0.5)
            self.tt_ax2.set_xlabel("Distance (m)")
            self.tt_ax2.set_ylabel("Time (ms)")
                
            self.dataxED, self.datatED = [], []
            artb = []
            for i in range(len(self.spED)):
                self.dataxED.append({self.spED[i]:[]})
                self.datatED.append({self.spED[i]:[]})
                artb.append({self.spED[i]:[]})

            #colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(sp))]
            s = 0
            for i in range(len(t)):
                if not np.isnan(x[i]):
                    self.dataxED[s][self.spED[s]].append(x[i])
                    self.datatED[s][self.spED[s]].append(t[i])
                    if i == 0:
                        b = self.tt_ax2.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4,zorder=10)
                    else:
                        b = self.tt_ax2.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4,zorder=10)
                    artb[s][self.spED[s]].append(b)
                else:
                    s+=1
            lines = []
            self.tt_S = []
            for i in range(len(self.spED)):
                sPlot = self.tt_ax2.scatter(self.spED[i],0, marker = "*", c = "yellow", edgecolor = "k", s = 200, zorder=10)
                self.tt_S.append(sPlot)
                l = self.tt_ax2.plot(self.dataxED[i][self.spED[i]],self.datatED[i][self.spED[i]], c = "k", lw = 0.75)
                lines.append(l)
           
            def onpick(event):
                self.art = event.artist
                artx = self.art.get_offsets()[0][0]
                artt = self.art.get_offsets()[0][1]
                
                for i in range(len(self.spED)):
                    for b in artb[i][self.spED[i]]:
                        bx = b.get_offsets()[0][0]
                        bt = b.get_offsets()[0][1]
                        if artx == bx and artt == bt:
                            self.arts = self.spED[i]
                            self.i = i
                            self.arti = np.where(np.array(self.dataxED[i][self.spED[i]]) == artx)[0][0]

            def onrelease(event):
             
                self.datatED[self.i][self.arts][self.arti] = event.ydata
                self.art.set_offsets((self.art.get_offsets()[0][0],event.ydata))
                for i in range(len(self.spED)):
                    lines[i][0].set_data(self.dataxED[i][self.spED[i]],self.datatED[i][self.spED[i]])
                self.tt_fig2.canvas.draw()
             
                self.art = None
                self.arts = None
                self.i = None
                self.arti = None

            event = self.tt_fig2.canvas.mpl_connect('pick_event', onpick)
            event2 = self.tt_fig2.canvas.mpl_connect('button_release_event', onrelease)
            self.tt_raise()
            messagebox.showinfo('Refrapy','Travel-times file loaded successfully!\nDrag and drop travel-times (circles) to edit\nWhen done, save the results into a new file')

    '''def tt_topo(self):

        if self.tt_pltTT:
            try:
                self.tt_topoFile = filedialog.askopenfilename(title='Open',filetypes=[('Elevation file','*.txt'), ('All files','*.*')])
            except:
                pass
            
            if self.tt_topoFile:
                self.p, self.e = np.loadtxt(self.tt_topoFile, usecols = (0,1), unpack = True)
                self.ge = [self.e[np.where(np.array(self.p) == np.array(self.gp)[i])[0]][0] for i in range(len(self.gp))]
                self.se = [self.e[np.where(np.array(self.p) == np.array(self.sp)[i])[0]][0] for i in range(len(self.sp))]
                messagebox.showinfo('Refrapy','Elevation data loaded successfully!')'''
    
    def tt_invert(self):

        if self.TTfile_ext == ".rp":
            if messagebox.askyesno("Refrapy", "Use elevation file?"):
                try:
                    self.tt_topoFile = filedialog.askopenfilename(title='Open',filetypes=[('Elevation file','*.txt'), ('All files','*.*')])
                except:
                    pass
                
                if self.tt_topoFile:
                    self.p, self.e = np.loadtxt(self.tt_topoFile, usecols = (0,1), unpack = True)
                    self.ge = [self.e[np.where(np.array(self.p) == np.array(self.gp)[i])[0]][0] for i in range(len(self.gp))]
                    self.se = [self.e[np.where(np.array(self.p) == np.array(self.sp)[i])[0]][0] for i in range(len(self.sp))]
                    messagebox.showinfo('Refrapy','Elevation data loaded successfully!')
            self.tt_ax3.cla()
            def solve(layer, G, d, w):
                rMs = np.zeros((int(len(layer)), int(len(self.sp)+self.gn+1)))
                r = 0
                for i in range(len(self.gp)):
                    for j in range(len(self.sp)):
                        if  self.sp[j] > min(self.gp) and self.sp[j] < max(self.gp): #se for fonte intermediaria                       
                            if self.gp[i]+self.gs >= self.sp[j] and self.gp[i]-self.gs <= self.sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(self.sp)+i] = -w
                                r += 1
                        elif self.sp[j] <= min(self.gp):
                            if self.gp[i]-self.gs <= self.sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(self.sp)+i] = -w
                                r += 1
                        elif self.sp[j] >= max(self.gp):
                            if self.gp[i]+self.gs >= self.sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(self.sp)+i] = -w
                                r += 1      
                rMs = rMs[~np.all(rMs == 0, axis=1)] #regularization matrix of time-terms from sources
                rMg = np.zeros((int(len(layer)), int(len(self.sp)+self.gn+1)))
                for i,j in zip(range(np.shape(rMg)[0]), range(np.shape(rMg)[1])):
                    try:
                        rMg[i][len(self.sp)+j] = w
                        rMg[i][len(self.sp)+j+1] = -w
                    except:
                        pass
                   
                rMg = rMg[~np.all(rMg == 0, axis=1)][:-2] #regularization matrix of time-terms from geophones
                rM = np.concatenate((rMs, rMg))
                rd = np.hstack((d, [i*0 for i in range(np.shape(rM)[0])]))
                rG = np.concatenate((G, rM))
                sol, sse, rank, sv = np.linalg.lstsq(rG, rd)
                return sol, sse[0]

            if self.layer1:
                d1 = np.array([self.layer1[i][1] for i in range(len(self.layer1))])
                G1 = np.array([self.layer1[i][3] for i in range(len(self.layer1))])
                G1 = np.reshape(G1, (len(G1),1))

                with open("dados_camada1_Nogueira.txt","w") as arq:
                    for i in range(len(d1)):
                        arq.write("%.5f %.5f\n"%(d1[i], G1[i][0]))

                sol_layer1, res1, rank1, sv1 = np.linalg.lstsq(G1, d1)
                v1 = 1000/sol_layer1[0] #m/s
                self.velocity1 = v1
                rms1 = np.sqrt(res1/len(sol_layer1))

                if self.layer2:
                    d2 = np.array([self.layer2[i][1] for i in range(len(self.layer2))])
                    G2 = np.zeros((int(len(self.layer2)),
                                   int(len(self.sp)+self.gn+1)))

                    for i in range(len(self.layer2)):
                        G2[i][self.layer2[i][-2]] = 1
                        G2[i][self.layer2[i][-1]+len(self.sp)] = 1
                        G2[i][-1] = self.layer2[i][-3]

                    sol_layer2, sse = solve(self.layer2, G2, d2, 0.1)
                    v2 = 1000/sol_layer2[-1] #m/s
                    self.velocity2 = v2
                    rms2 = np.sqrt(sse/len(sol_layer2))

                if self.layer3:
                    d3 = np.array([self.layer3[i][1] for i in range(len(self.layer3))])
                    G3 = np.zeros((int(len(self.layer3)),
                                   int(len(self.sp)+self.gn+1)))

                    for i in range(len(self.layer3)):
                        G3[i][self.layer3[i][-2]] = 1
                        G3[i][self.layer3[i][-1]+len(self.sp)] = 1
                        G3[i][-1] = self.layer3[i][-3]

                    sol_layer3, sse = solve(self.layer3, G3, d3, 0.1)
                    v3 = 1000/sol_layer3[-1] #m/s
                    self.velocity3 = v3
                    rms3 = np.sqrt(sse/len(sol_layer3))
                    rmsMed = (rms2+rms3)/2

                
                self.tt_ax3.grid(lw = .5, ls = "-", color = "grey", alpha = .35)
                self.tt_ax3.set_title(label='Velocity model')
                self.tt_ax3.set_xlabel("Distance (m)")
                self.tt_ax3.set_aspect('equal', adjustable='box')
                self.sgp = np.sort(np.concatenate((np.arange(self.fg,self.fg+self.gn*self.gs,self.gs),np.array(self.sp))))
            
                if self.layer1 and self.layer2 and not self.layer3:
                    
                    dtg = np.array([i for i in sol_layer2[len(self.sp):-1]]) #delay-time of all geophones
                    if self.tt_topoFile:
                        self.tt_ax3.set_ylabel("Elevation (m)")
                        dlayer2 = self.ge-((dtg*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000)
                        self.depthLayer2 = dlayer2
                        
                        try:
                            f = interp1d(self.gp, dlayer2, kind = 'cubic', fill_value='extrapolate')
                            sdlayer2 = f(np.linspace(self.gp[0], self.gp[-1], 1000))
                            f = interp1d(self.gp, self.ge, kind = 'cubic', fill_value='extrapolate')
                            s_surf = f(np.linspace(self.gp[0], self.gp[-1], 1000))
                            self.tt_layer1 = self.tt_ax3.fill_between(np.linspace(self.gp[0], self.gp[-1], 1000),sdlayer2,s_surf, color = "red",
                                              alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(np.linspace(self.gp[0], self.gp[-1], 1000),sdlayer2, min(sdlayer2)*0.99,
                                              alpha = .5,edgecolor = "k", color = "green",
                                              label = "%.0f m/s"%v2)
                        except:
                            self.tt_layer1 = self.tt_ax3.fill_between(self.gp,dlayer2, self.ge, color = "red", alpha = .5,edgecolor = "k",
                                              label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(self.gp,dlayer2, min(dlayer2)*0.99, alpha = .5,edgecolor = "k",
                                              color = "green", label = "%.0f m/s"%v2)
                    else:
                        dlayer2 = -1*(dtg*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000
                        self.depthLayer2 = dlayer2
                        self.tt_ax3.set_ylabel("Depth (m)")
                        try:
                            f = interp1d(self.gp, dlayer2, kind = 'cubic', fill_value='extrapolate')
                            sdlayer2 = f(np.linspace(self.gp[0], self.gp[-1], 1000))
                            self.tt_layer1 = self.tt_ax3.fill_between(np.linspace(self.gp[0], self.gp[-1], 1000),
                                              sdlayer2,0, color = "red", alpha = .5,edgecolor = "k",
                                              label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(np.linspace(self.gp[0], self.gp[-1], 1000), sdlayer2,
                                              min(sdlayer2)*1.1, alpha = .5,edgecolor = "k", color = "green",
                                              label = "%.0f m/s"%v2)
                        except:
                            self.tt_layer1 = self.tt_ax3.fill_between(self.gp,dlayer2,0, color = "red", alpha = .5,edgecolor = "k",
                                              label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(self.gp,dlayer2, min(dlayer2)*1.1, alpha = .5,edgecolor = "k",
                                              color = "green", label = "%.0f m/s"%v2)

                    self.tt_ax3.legend(loc="best")
                    #axvm.set_ylim((min(sdlayer2)*1.1-5,5))
                    messagebox.showinfo('Refrapy','The velocity model was created!\n RMS = %.5f ms'%rms2)
                    self.tt_pltVM = True
                    self.tt_raise()
                            
                elif self.layer1 and self.layer2 and self.layer3:
                    dtg2 = np.array([i for i in sol_layer2[len(self.sp):-1]]) #delay-time of all geophones
                    dtg3 = np.array([i for i in sol_layer3[len(self.sp):-1]]) #delay-time of all geophones
                    upvmed = (v1+v2)/2
                    if self.tt_topoFile:
                        dlayer2 = self.ge-((dtg2*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000)
                        self.depthLayer2 = dlayer2
                        dlayer3 = self.ge-((dtg3*upvmed*v3)/(np.sqrt((v3**2)-(upvmed**2)))/1000)
                        self.depthLayer3 = dlayer3
                        try:
                            s_surf = f(np.linspace(self.gp[0], self.gp[-1], 1000))
                            f2 = interp1d(np.arange(self.fg, (self.gn*self.gs)+self.fg, self.gs), dlayer2, kind = 'cubic', fill_value='extrapolate')
                            sdlayer2 = f2(np.linspace(self.fg, self.fg+(self.gn*self.gs)-self.gs, 1000))
                            f3 = interp1d(np.arange(self.fg, (self.gn*self.gs)+self.fg, self.gs), dlayer3, kind = 'cubic', fill_value='extrapolate')
                            sdlayer3 = f3(np.linspace(self.fg, self.fg+(self.gn*self.gs)-self.gs, 1000))
                            self.tt_layer1 = self.tt_ax3.fill_between(np.linspace(self.gp[0], self.gp[-1], 1000),sdlayer2,s_surf, color = "red",
                                              alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(np.linspace(self.gp[0], self.gp[-1], 1000),sdlayer2, sdlayer3, alpha = .5,
                                              edgecolor = "k", color = "green", label = "%.0f m/s"%v2)
                            self.tt_layer3 = self.tt_ax3.fill_between(np.linspace(self.gp[0], self.gp[-1], 1000),sdlayer3, min(sdlayer3)*1.1,
                                              alpha = .5,edgecolor = "k", color = "blue",
                                              label = "%.0f m/s"%v3)
                        except:
                            self.tt_layer1 = self.tt_ax3.fill_between(self.gp,dlayer2,self.ge, color = "red", alpha = .5,edgecolor = "k",
                                              label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(self.gp,dlayer2, dlayer3, alpha = .5,edgecolor = "k", color = "green",
                                              label = "%.0f m/s"%v2)
                            self.tt_layer3 = self.tt_ax3.fill_between(self.gp,dlayer3, min(dlayer3)*1.1, alpha = .5,edgecolor = "k",
                                              color = "blue", label = "%.0f m/s"%v3)

                    else:
                        dlayer2 = -1*(dtg2*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000
                        dlayer3 = -1*(dtg3*upvmed*v3)/(np.sqrt((v3**2)-(upvmed**2)))/1000
                        self.depthLayer2 = dlayer2
                        self.depthLayer3 = dlayer3
                        
                        try:
                            f2 = interp1d(self.gp, dlayer2, kind = 'cubic',fill_value='extrapolate')
                            sdlayer2 = f2(np.linspace(self.gp[0], self.gp[-1], 1000))
                            f3 = interp1d(self.gp, dlayer3, kind = 'cubic',fill_value='extrapolate')
                            sdlayer3 = f3(np.linspace(self.gp[0], self.gp[-1], 1000))
                            self.tt_layer1 = self.tt_ax3.fill_between(np.linspace(self.fg, self.fg+(self.gn*self.gs)-self.gs, 1000),sdlayer2,0, color = "red",
                                              alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(np.linspace(self.fg, self.fg+(self.gn*self.gs)-self.gs, 1000),
                                              sdlayer2, sdlayer3, alpha = .5,edgecolor = "k",
                                              color = "green", label = "%.0f m/s"%v2)
                            self.tt_layer3 = self.tt_ax3.fill_between(np.linspace(self.fg, self.fg+(self.gn*self.gs)-self.gs, 1000),sdlayer3,
                                              min(sdlayer3)*1.1, alpha = .5,edgecolor = "k", color = "blue",
                                              label = "%.0f m/s"%v3)
                        except:
                            self.tt_layer1 = self.tt_ax3.fill_between(self.gp,dlayer2,0, color = "red", alpha = .5,edgecolor = "k",
                                              label = "%.0f m/s"%v1)
                            self.tt_layer2 = self.tt_ax3.fill_between(self.gp,dlayer2, dlayer3, alpha = .5,edgecolor = "k",
                                              color = "green", label = "%.0f m/s"%v2)
                            self.tt_layer3 = self.tt_ax3.fill_between(self.gp,dlayer3, min(dlayer3)*1.1, alpha = .5,edgecolor = "k",
                                              color = "blue",label = "%.0f m/s"%v3)
                        
                    self.tt_ax3.legend(loc="best")
                    #axvm.set_ylim((min(sdlayer3)*1.1-5,5))
                    self.tt_pltVM = True
                    messagebox.showinfo('Refrapy','The velocity model was created!\nRMS layer 1 = %.5f\nRMS layer 2 = %.5f ms\nRMS layer 3 = %.2f'%(rms1,rms2,rms3))
                    self.tt_raise()
 

root = Tk()
Sisref(root)
root.mainloop()
