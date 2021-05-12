from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from obspy import read
import matplotlib                                                                
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import os                                                                              
import numpy as np
from scipy import stats,arange
import sys
import warnings
import platform

warnings.filterwarnings('ignore')

class Sispick(Frame):

    def __init__(self, master, *args, **kwargs):                         

        Frame.__init__(self, master)
        self.grid(row = 0, column = 0, sticky = NSEW)
        self.memory()
        self.winConfig()
        self.menus()
        self.icons()
        self.buttons()
        self.statusBar()
        self.mplConfig()

    def winConfig(self):

        root.geometry("1360x768")
        root.resizable(0,0)
        root.config(background='#F3F3F3')
        root.title('REFRAPICK')
        root.bind('<Alt-s>', lambda x: self.destroy())
        root.bind('<Alt-S>', lambda x: self.destroy())
        root.bind('A', lambda x: self.pickAmostra())
        root.bind('a', lambda x: self.pickAmostra())
        root.bind('<Alt-L>', lambda x: self.ligarPicks())
        root.bind('<Alt-l>', lambda x: self.ligarPicks())
        root.bind('l', lambda x: self.ligarPicks())
        root.bind('V', lambda x: self.pickVelocidade())
        root.bind('v', lambda x: self.pickVelocidade())
        root.bind('<Control-a>', lambda x: self.abrirSismogramas())
        root.bind('<Control-A>', lambda x: self.abrirSismogramas())
        root.bind('<Control-l>', lambda x: self.limparplot())
        root.bind('<Control-L>', lambda x: self.limparplot())
        root.bind('<Control-s>', lambda x: self.salvarpick())
        root.bind('<Control-S>', lambda x: self.salvarpick())
        root.bind('<Control-x>', lambda x: self.fecharPlot())
        root.bind('<Control-X>', lambda x: self.fecharPlot())
        root.bind('<Control-o>', lambda x: self.configPlot())
        root.bind('<Control-O>', lambda x: self.configPlot())
        root.bind('<Control-g>', lambda x: self.verCurva())
        root.bind('<Control-G>', lambda x: self.verCurva())
        root.bind('<Control-h>', lambda x: self.cabecalho())
        root.bind('<Control-H>', lambda x: self.cabecalho())
        root.bind('<Shift-Left>', lambda x: self.ampdown())
        root.bind('<Shift-Right>', lambda x: self.ampup())
        root.bind('<Up>', lambda x: self.maisy())
        root.bind('<Down>', lambda x: self.menosy())
        root.bind('i', lambda x: self.invert())
        root.bind('n', lambda x: self.normalizar())
        root.bind('<Alt-Right>', lambda x: self.sombNeg())
        root.bind('<Alt-Left>', lambda x: self.sombPos())
        root.bind('<Alt-Down>', lambda x: self.sombNull())
        root.bind('c', lambda x: self.clip())
        root.bind('I', lambda x: self.invert())
        root.bind('N', lambda x: self.normalizar())
        root.bind('S', lambda x: self.fill())
        root.bind('s', lambda x: self.fill())
        root.bind('C', lambda x: self.clip())
        root.bind('P', lambda x: self.ativarPick())
        root.bind('p', lambda x: self.ativarPick())
        root.bind('<Left>', lambda x: self.backpage())
        root.bind('<Right>', lambda x: self.nextpage())
        root.protocol("WM_DELETE_WINDOW", self.fechar)
    

    def menus(self):
        
        menuBar = Menu(root)
        fileMenu = Menu(menuBar)
        menuBar.add_cascade(label = 'File', menu = fileMenu)
        fileMenu.add_command(label='Open <CTRL+A>',
                                      command=self.abrirSismogramas)
        fileMenu.add_separator()
        fileMenu.add_command(label='Save pick file (Seisimager) <CTRL+S>',
                                      command=self.salvarpick)
        fileMenu.add_command(label='Save pick file (Refrapy) <CTRL+S>',
                                      command=self.salvargp)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit <ALT+S>',
                                      command=self.destroy)
        viewMenu = Menu(menuBar)
        menuBar.add_cascade(label='Visualization',menu=viewMenu)
        viewMenu.add_command(label='Next <right arrow>',
                                         command=self.nextpage)
        viewMenu.add_command(label='Previous <left arrow>',
                                         command=self.backpage)
        viewMenu.add_separator()
        viewMenu.add_command(label='Inver time axis <I>',
                                         command=self.backpage)
        viewMenu.add_separator()
        viewMenu.add_command(label='Decrease time axis <down arrow>',
                                         command=self.menosy)
        viewMenu.add_command(label='Increase time axis <up arrow>',
                                         command=self.maisy)
        traceMenu = Menu(menuBar)
        menuBar.add_cascade(label='Waveform processing',menu=traceMenu)
        traceMenu.add_command(label='Increase scale gain <SHIFT+right>',
                                     command=self.ampup)
        traceMenu.add_command(label='Decrease scale gain <SHIFT+left>',
                                     command=self.ampdown)
        traceMenu.add_separator()
        traceMenu.add_command(label='Apply/Remove normalization <N>',
                                     command=self.normalizar)
        traceMenu.add_separator()
        traceMenu.add_command(label='Shade negative amplitudes <ALT+right>',
                                     command=self.sombNeg)
        traceMenu.add_command(label='Shade positive amplitudes <ALT+left>',
                                     command=self.sombPos)
        traceMenu.add_command(label='Remove shades <ALT+down>',
                                     command=self.sombNull)
        traceMenu.add_separator()
        traceMenu.add_command(label='Clip amplitudes <C>',
                                     command=self.clip)
        editMenu = Menu(menuBar)
        menuBar.add_cascade(label='Editing',menu=editMenu)
        editMenu.add_command(label='Enable/Disable first breaks picking <P>',
                                     command=self.ativarPick)
        editMenu.add_command(label='Clear picks <CTRL+L>',
                                     command=self.limparplot)
        editMenu.add_separator()
        editMenu.add_command(label='Trim section lenght <A>',
                                 command=self.pickAmostra)
        editMenu.add_command(label='Use default section lenght <ALT+A>',
                                         command=self.amostrasDefault)
        editMenu.add_separator()
        editMenu.add_command(label='Enable/disable pick lines <L>',
                                         command=self.removerLinhaPicks)
        editMenu.add_separator()
        editMenu.add_command(label='View travel time curves <CTRL+G>',
                                         command=self.verCurva)
        editMenu.add_separator()
        editMenu.add_command(label='Close current sections <CTRL+X>',
                                     command=self.fecharPlot)
        '''filterMenu = Menu(menuBar)
        menuBar.add_cascade(label='Filtering',menu=filterMenu)
        filterMenu.add_command(label='Low pass filter <Ctrl+L>',command=self.filtroLP)
        filterMenu.add_command(label='High pass filter <CTRL+H>',command=self.filtroHP)
        filterMenu.add_separator()
        filterMenu.add_command(label='Remove filter <CTRL+C>',command=self.removerFiltros)'''
        optMenu = Menu(menuBar)
        menuBar.add_cascade(label='Options',menu=optMenu)
        optMenu.add_command(label='Plot options <CTRL+O>',command=self.configPlot)
        optMenu.add_separator()
        optMenu.add_command(label='Edit section info <CTRL+H>',command = self.cabecalho)
        helpMenu = Menu(menuBar)
        menuBar.add_cascade(label='Help',menu=helpMenu)
        helpMenu.add_command(label='Tutorial',command = lambda: print(''))
        root.configure(menu=menuBar)

    def icons(self):

        self.img_abrir = PhotoImage(file="%s/imagens/abrir.gif"%os.getcwd())
        self.img_salvar = PhotoImage(file="%s/imagens/salvar.gif"%os.getcwd())
        self.img_voltar = PhotoImage(file="%s/imagens/voltar.gif"%os.getcwd())
        self.img_proximo = PhotoImage(file="%s/imagens/proximo.gif"%os.getcwd())
        self.img_baixo = PhotoImage(file="%s/imagens/baixo.gif"%os.getcwd())
        self.img_cima = PhotoImage(file="%s/imagens/cima.gif"%os.getcwd())
        self.img_menos = PhotoImage(file="%s/imagens/menos.gif"%os.getcwd())
        self.img_mais = PhotoImage(file="%s/imagens/mais.gif"%os.getcwd())
        self.img_norm = PhotoImage(file="%s/imagens/norm.gif"%os.getcwd())
        self.img_invert = PhotoImage(file="%s/imagens/invert.gif"%os.getcwd())
        self.img_cortar = PhotoImage(file="%s/imagens/cortar.gif"%os.getcwd())
        self.img_sombnull = PhotoImage(file="%s/imagens/fill_null.gif"%os.getcwd())
        self.img_sombneg = PhotoImage(file="%s/imagens/fill_neg.gif"%os.getcwd())
        self.img_sombpos = PhotoImage(file="%s/imagens/fill_pos.gif"%os.getcwd())
        self.img_clip = PhotoImage(file="%s/imagens/clip.gif"%os.getcwd())
        self.img_PA = PhotoImage(file="%s/imagens/PA.gif"%os.getcwd())
        self.img_PB = PhotoImage(file="%s/imagens/PB.gif"%os.getcwd())
        self.img_RF = PhotoImage(file="%s/imagens/RF.gif"%os.getcwd())
        self.img_pick = PhotoImage(file="%s/imagens/pick.gif"%os.getcwd())
        self.img_ligar = PhotoImage(file="%s/imagens/ligar.gif"%os.getcwd())
        self.img_limpar = PhotoImage(file="%s/imagens/limpar.gif"%os.getcwd())
        self.img_vel = PhotoImage(file="%s/imagens/vel.gif"%os.getcwd())
        self.img_grafico = PhotoImage(file="%s/imagens/grafico.gif"%os.getcwd())
        self.img_opt = PhotoImage(file="%s/imagens/opt.gif"%os.getcwd())
        self.img_header = PhotoImage(file="%s/imagens/header.gif"%os.getcwd())
        self.img_fechar = PhotoImage(file="%s/imagens/fechar.gif"%os.getcwd())
        root.tk.call('wm', 'iconphoto', root._w, self.img_pick) 

    def buttons(self):

        Abrir = Button(self, command = self.abrirSismogramas)
        Abrir.config(image=self.img_abrir)
        Abrir.grid(row=0,column=0,sticky=W)
        Salvar = Button(self, command = self.salvargp)
        Salvar.config(image=self.img_salvar)
        Salvar.grid(row=0,column=1,sticky=W)
        Back = Button(self, command = self.backpage)
        Back.config(image=self.img_voltar)
        Back.grid(row=0,column=2,sticky=W)
        Next = Button(self, command = self.nextpage)
        Next.config(image=self.img_proximo)
        Next.grid(row=0,column=3,sticky=W)
        menosY = Button(self, command = self.menosy)
        menosY.config(image=self.img_baixo)
        menosY.grid(row=0,column=4,sticky=W)
        maisY = Button(self, command = self.maisy)
        maisY.config(image=self.img_cima)
        maisY.grid(row=0,column=5,sticky=W)
        ampDown = Button(self,command = self.ampdown)
        ampDown.config(image=self.img_menos)
        ampDown.grid(row=0,column=6,sticky=W)
        ampUp = Button(self, command = self.ampup)
        ampUp.config(image=self.img_mais)
        ampUp.grid(row=0,column=7,sticky=W)
        normal = Button(self, command = self.normalizar)
        normal.config(image=self.img_norm)
        normal.grid(row=0,column=8,sticky=W)
        inverttime = Button(self, command = self.invert)
        inverttime.config(image=self.img_invert)
        inverttime.grid(row=0,column=9,sticky=W)
        pickAmostras = Button(self, command = self.pickAmostra)
        pickAmostras.config(image=self.img_cortar)
        pickAmostras.grid(row=0,column=10,sticky=W)
        somb_null = Button(self, command = self.sombNull)
        somb_null.config(image=self.img_sombnull)
        somb_null.grid(row=0,column=11,sticky=W)
        somb_neg = Button(self, command = self.sombNeg)
        somb_neg.config(image=self.img_sombneg)
        somb_neg.grid(row=0,column=12,sticky=W)
        somb_pos = Button(self, command = self.sombPos)
        somb_pos.config(image=self.img_sombpos)
        somb_pos.grid(row=0,column=13,sticky=W) 
        clipar = Button(self, command = self.clip)
        clipar.config(image=self.img_clip)
        clipar.grid(row=0,column=14,sticky=W)
        PA = Button(self, command = self.filtroHP)
        PA.config(image=self.img_PA)
        PA.grid(row=0,column=15,sticky=W)
        PB = Button(self, command = self.filtroLP)
        PB.config(image=self.img_PB)
        PB.grid(row=0,column=16,sticky=W)
        RF = Button(self, command = self.removerFiltros)
        RF.config(image=self.img_RF)
        RF.grid(row=0,column=17,sticky=W)
        Pick = Button(self, command = self.ativarPick)
        Pick.config(image=self.img_pick)
        Pick.grid(row=0,column=18,sticky=W)
        ligar = Button(self, command = self.ligarPicks)
        ligar.config(image=self.img_ligar)
        ligar.grid(row=0,column=19,sticky=W)
        limpar = Button(self, command = self.limparplot)
        limpar.config(image=self.img_limpar)
        limpar.grid(row=0,column=20,sticky=W)
        vel = Button(self, command = self.pickVelocidade)
        vel.config(image=self.img_vel)
        vel.grid(row=0,column=21,sticky=W)
        grafico = Button(self, command = self.verCurva)
        grafico.config(image=self.img_grafico)
        grafico.grid(row=0,column=22,sticky=W)
        opt = Button(self, command = self.configPlot)
        opt.config(image=self.img_opt)
        opt.grid(row=0,column=23,sticky=W)
        header = Button(self, command = self.cabecalho)
        header.config(image=self.img_header)
        header.grid(row=0,column=24,sticky=W)
        FecharPlot = Button(self, command = self.fecharPlot)
        FecharPlot.config(image=self.img_fechar)
        FecharPlot.grid(row=0,column=25,sticky=W)

    def statusBar(self):

        self.statusPick = Label(self,text = ' ', fg='red',font=("Helvetica", 12), bg='#F3F3F3')
        self.statusPick.grid(row=0,column=26,sticky=E)
        self.statusVel = Label(self,text = ' ', fg='red',font=("Helvetica", 12), bg='#F3F3F3')
        self.statusVel.grid(row=0,column=27,sticky=E)
        self.statusCortador = Label(self,text = ' ', fg='red',font=("Helvetica", 12), bg='#F3F3F3')
        self.statusCortador.grid(row=0,column=28,sticky=E)
        self.statusPA = Label(self,text = ' ', fg='green',font=("Helvetica", 12),bg='#F3F3F3')
        self.statusPA.grid(row=0,column=29,sticky=E)
        self.statusPB = Label(self,text = ' ', fg='green',font=("Helvetica", 12),bg='#F3F3F3')
        self.statusPB.grid(row=0,column=30,sticky=E)
        self.status = Label(self,text = ' ', fg='red',font=("Helvetica", 12),bg='#F3F3F3')
        self.status.grid(row=0,column=31,sticky=E)

    def memory(self):

        self.frames, self.figs, self.axes, self.telas, self.listSource, self.sts, self.ticksLabel, self.toolbars, self.dadosNorms, self.dadosCrus, \
        self.ganho, self.filtros,self.filtrosHP, self.filtrosLP, self.copiasCruas, self.copiasNorms, self.okpicks, self.clips, \
        self.sombreamentos, self.picks, self.picksArts, self.coordx, self.coordy, self.conPickClick, self.conPickMov, self.conPickSoltar, \
        self.conVelClick, self.conVelMov, self.conVelSoltar, self.conAmostra, self.ndados, self.linhasPick, self.freqLP, \
        self.freqHP = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[], \
        [],[],[],[],[],[],[],[]
        self.sublinhas, self.bolas, self.indicadores, self.plotArts, self.sombArts, self.coordsx, self.coordsy, self.linhasVel, \
        self.textoVel, self.tracosMax = {},{},{},{},{},{}, {}, {}, {}, {}
        self.plotExiste, self.pickMode, self.yinvertido, self.normalizado, self.optAberto, self.pickAmostraAtivado, self.clickOn, \
        self.pickVelOn = False,False,False,False,False,False,False,False
        self.arquivos, self.formato, self.posicaoGeof1, self.eventCon, self.pagina, self.recordlen, self.valordx, self.linhaVel, self.linhaPick, \
        self.valorFigx, self.valorFigy = None,None,None,None,None,None,None,None,None,None,None
        self.fatorY, self.valorGanho, self.fatorLP, self.fatorHP = 0.8, 2, 0.8, 1.5

    def mplConfig(self):

        plt.rcParams['keymap.zoom'] = 'z,Z'
        plt.rcParams['keymap.back'] = 'b,B'
        plt.rcParams['keymap.home'] = 'ctrl+z,ctrl+Z'
        plt.rcParams['keymap.save'] = 'ctrl+i,ctrl+I'
        plt.rcParams['keymap.pan'] = 'm,M'

    def fechar(self):
        
        if self.plotExiste == True:
            self.fecharPlot()
            self.destroy()
            root.destroy()
            sys.exit()
        else:
            self.destroy()
            root.destroy()
            sys.exit()
            
    def abrirSismogramas(self):
        
        if self.plotExiste == False:    
            self.arquivos = sorted(filedialog.askopenfilenames(title='Open',
                                                               filetypes=[('seg2','*.dat'),
                                                                ('SG2','*.sg2'),
                                                                ('segy','*.sgy'),
                                                                ('SU','*.SU'),
                                                                ("All files", '*')]))
            if len(self.arquivos) > 0:
                self.status.configure(text=' Opening %d files. Please wait...'%len(self.arquivos))
                for i in range(len(self.arquivos)):
                    self.sts.append(read(self.arquivos[i]))
                    self.ndados.append(len(self.sts[i][0]))
                    if self.sts[i][0].stats._format == 'SEG2':
                        self.formato = 'seg2'
                        try: 
                            self.listSource.append(self.sts[i][0].stats.seg2['SOURCE_LOCATION'])
                        except:
                            sourcep = simpledialog.askfloat("Refrapy", "Source position not found for file %s\nPlease, enter a value below:"%os.path.basename(self.arquivos[i]))
                            if sourcep == None:
                                sourcep = 0
                            self.listSource.append(sourcep)
                        try:
                            self.posicaoGeof1 = float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])
                        except:
                            firstgeofpos = simpledialog.askfloat("Refrapy", "First geophone position not found for file %s\nPlease, enter a value below:"%os.path.basename(self.arquivos[i]))
                            if firstgeofpos == None:
                                firstgeofpos = 0
                            self.posicaoGeof1 = firstgeofpos
                        try:
                            self.valordx = float(self.sts[0][1].stats.seg2['RECEIVER_LOCATION'])-float(self.sts[0][0].stats.seg2['RECEIVER_LOCATION'])
                        except:
                            spa = simpledialog.askfloat("Refrapy", "Geophones interval not found for file %s\nPlease, enter a value below:"%os.path.basename(self.arquivos[i]))
                            if spa == None:
                                spa = 0
                            self.valordx = spa

                    elif self.sts[i][0].stats._format == 'SU':
                        self.formato = 'SU'
                        try: 
                            self.listSource.append(self.sts[i][0].stats.su['SOURCE_LOCATION'])
                        except:
                            sourcep = simpledialog.askfloat("Refrapy", "Source position not found for file %s\nPlease, enter a value below:"%os.path.basename(self.arquivos[i]))
                            if sourcep == None:
                                sourcep = 0
                            self.listSource.append(sourcep)
                        try:
                            self.posicaoGeof1 = float(self.sts[i][0].stats.su['RECEIVER_LOCATION'])
                        except:
                            firstgeofpos = simpledialog.askfloat("Refrapy", "First geophone position not found for file %s\nPlease, enter a value below:"%os.path.basename(self.arquivos[i]))
                            if firstgeofpos == None:
                                firstgeofpos = 0
                            self.posicaoGeof1 = firstgeofpos
                        try:
                            self.valordx = float(self.sts[0][1].stats.su['RECEIVER_LOCATION'])-float(self.sts[0][0].stats.su['RECEIVER_LOCATION'])
                        except:
                            spa = simpledialog.askfloat("Refrapy", "Geophones interval not found for file %s\nPlease, enter a value below:"%os.path.basename(self.arquivos[i]))
                            if spa == None:
                                spa = 0
                            self.valordx = spa
                            
                    elif self.sts[i][0].stats._format == 'SEGY':
                        self.formato = 'segy'
                        try:
                            self.listSource.append(self.sts[i][0].stats.segy['SOURCE_LOCATION'])
                        except:
                            messagebox.showinfo('Refrapy','Source positions not found, so 999 m will be used.\nTo change values go to Options > Edit section info')
                            self.listSource.append(999)
                        try:
                            self.posicaoGeof1 = float(self.sts[i][0].stats.segy['RECEIVER_LOCATION'])
                        except:
                            self.posicaoGeof1 = 0
                            messagebox.showinfo('Refrapy', 'First geophone position not found, so 0 m will be used.\nTo change values go to Options > Edit section info')
                        try:
                            self.valordx = float(self.sts[0][1].stats.segy['RECEIVER_LOCATION'][0])-float(self.sts[0][0].stats.segy['RECEIVER_LOCATION'][0])
                        except:
                            messagebox.showinfo('Refrapy', 'Geophone spacing not found, so 2 m will be used.\nTo change values go to Options > Edit section info')
                            self.valordx = 2 
                    else:
                        messagebox.showinfo('Refrapy', 'File format is not SEG2/SEGY.\nDefault values for geophones spacing, source and first geophone position were used.\nTo change values go to Options > Edit section info')
                        self.valordx = 2
                        self.posicaoGeof1 = 0
                        self.listSource.append(999)
                        
                if self.ndados[0] > 10000:
                    messagebox.showinfo('Refrapy','Traces have a great ammount of samples.\nTo speed up processing, you might want to consider trimming the sections lenght in Edit > Trim section lenght')

                for i in range(len(self.arquivos)):
                    frame = Frame(root,bg='#F3F3F3')
                    frame.grid(row=1, column=0, sticky = NSEW)
                    self.frames.append(frame)
                    fig = plt.figure(i,figsize=(13.75,7.05),facecolor='#F3F3F3')
                    fig.tight_layout()
                    self.figs.append(fig)
                    ax = self.figs[i].add_subplot(111)
                    self.axes.append(ax)
                    self.dadosCrus.append({})
                    self.dadosNorms.append({})
                    self.plotArts[i] = []
                    self.sombArts[i] = []
                    self.picks.append({})
                    self.picksArts.append({})
                    self.coordsx[i] = []
                    self.coordsy[i] = []
                    self.linhasVel[i] = []
                    self.textoVel[i] = []
                    self.bolas[i] = []
                    self.indicadores[i] = []
                    self.linhasPick.append(None)
                    self.sublinhas[i] = []
                    self.conPickClick.append(None)
                    self.conPickMov.append(None)
                    self.conPickSoltar.append(None)
                    self.conVelClick.append(None)
                    self.conVelMov.append(None)
                    self.conVelSoltar.append(None)
                    self.conAmostra.append(None)
                    for j in range(len(self.arquivos)):
                        self.sublinhas[i].append(None)
                    self.canais = len(self.sts[0])                      
                    self.recordlen = self.sts[0][0].stats.endtime-self.sts[0][0].stats.starttime
                    self.intervaloAmostragem = self.sts[0][0].stats.delta     
                    self.ganho.append(1)
                    self.clips.append(False)
                    self.sombreamentos.append('null')
                    self.filtros.append(False)
                    self.copiasCruas.append(None)
                    self.copiasNorms.append(None)
                    self.freqLP.append(1000)
                    self.freqHP.append(5)
                    self.filtrosLP.append(False)
                    self.filtrosHP.append(False)
                    self.tracosMax[i] = [max(self.sts[i][j]) for j in range(self.canais)]
                    for j in range(self.canais):
                        self.dadosCrus[i][j] = self.sts[i][j].data/max(self.tracosMax[i])
                        self.dadosNorms[i][j] = self.sts[i][j].data/max(self.sts[i][j].data)
                        self.okpicks.append(self.posicaoGeof1+self.valordx*j)
                        self.ticksLabel.append(str(int(j*self.valordx)))
                        traco, = self.axes[i].plot(self.dadosCrus[i][j][0:self.ndados[i]]*(-1)+self.posicaoGeof1+self.valordx*j,
                                                   [self.sts[i][0].stats.delta*k*1000 for k in range(int(self.ndados[i]))],color='black')
                        self.plotArts[i].append(traco)
                    plt.figure(i)    
                    plt.title(' %s | %d channels'%(os.path.basename(self.arquivos[i]),int(self.canais)))     
                    plt.xlabel('Distance (m)')
                    plt.ylabel('Time (ms)')
                    plt.ylim(0,1000*(self.sts[i][0].stats.delta*self.ndados[i]))
                    plt.xlim(self.posicaoGeof1-self.valordx,self.posicaoGeof1+self.valordx*len(self.sts[i]))   
                    tela = FigureCanvasTkAgg(self.figs[i], self.frames[i])
                    self.telas.append(tela)
                    self.telas[i].draw()
                    self.telas[i].get_tk_widget().pack(fill='both', expand=True)
                    toolbar = NavigationToolbar2Tk(self.telas[i], self.frames[i])
                    self.toolbars.append(toolbar)
                    self.toolbars[i].update()
                    self.telas[i]._tkcanvas.pack(fill='both', expand=True)
                    
                self.status.configure(text=' ')
                self.frames[0].tkraise()
                self.pagina = 0
                plt.figure(self.pagina)
                def do(event):
                    key_press_handler(event, self.telas[self.pagina], self.toolbars[self.pagina])
                self.figs[-1].canvas.mpl_connect('key_press_event', do)
                self.plotExiste = True
                self.yinvertido = False
                self.sombreamento = False
                self.normalizado = False
                self.clickOn = False
                self.pickVelOn = False
        else:
            messagebox.showinfo('','Close the current sections to open a new one!')

    def nextpage(self):
        
        if self.plotExiste == True and self.pagina < len(self.arquivos)-1:
            frame = self.frames[self.pagina+1]
            frame.tkraise()
            self.pagina += 1
            self.telas[self.pagina].draw()
            if self.filtrosHP[self.pagina] == True:
                self.statusPA.configure(text = 'High pass: %.2f Hz'%float(self.freqHP[self.pagina]/self.fatorHP))
            if self.filtrosLP[self.pagina] == True:
                self.statusPB.configure(text = 'Low pass: %.2f Hz'%float(self.freqLP[self.pagina]/self.fatorLP))
            if self.filtrosHP[self.pagina] != True:
                self.statusPA.configure(text = '')
            if self.filtrosLP[self.pagina] != True:
                self.statusPB.configure(text = '')

    def backpage(self):

        if self.plotExiste == True and self.pagina != 0:  
            frame = self.frames[self.pagina-1] 
            frame.tkraise()
            self.pagina -= 1
            self.telas[self.pagina].draw()
            if self.filtrosHP[self.pagina] == True:
                self.statusPA.configure(text = 'High pass: %.2f Hz'%float(self.freqHP[self.pagina]/self.fatorHP))
            if self.filtrosLP[self.pagina] == True:
                self.statusPB.configure(text = 'Low pass: %.2f Hz'%float(self.freqLP[self.pagina]/self.fatorLP))
            if self.filtrosHP[self.pagina] != True:
                self.statusPA.configure(text = '')
            if self.filtrosLP[self.pagina] != True:
                self.statusPB.configure(text = '')
                    
    def ativarPick(self):
        
        if self.plotExiste == True:
            if self.pickMode == False:
                self.pickMode = True
                self.statusPick.configure(text=' Pick mode on',fg='blue')
                
                def pick(event):
                    try:
                        if event.button == 1:
                            nearestMagnetValue = min(self.okpicks, key=lambda x: abs(event.xdata - x))
                            if nearestMagnetValue in self.picks[self.pagina]:
                                self.picks[self.pagina][nearestMagnetValue] = event.ydata
                                self.picksArts[self.pagina][nearestMagnetValue].remove()
                                pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-(self.valordx*0.5),
                                                                    nearestMagnetValue+(self.valordx*0.5),colors='r',linestyle='solid')
                                self.picksArts[self.pagina][nearestMagnetValue] = pickline
                                self.telas[self.pagina].draw()         
                            else:
                                pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-(self.valordx*0.5),
                                                                    nearestMagnetValue+(self.valordx*0.5),colors='r',linestyle='solid')
                                self.picksArts[self.pagina].update({nearestMagnetValue:pickline})
                                self.picks[self.pagina].update({nearestMagnetValue:event.ydata})
                                self.telas[self.pagina].draw()
                            for i in range(len(self.arquivos)):
                                if i != self.pagina:
                                    if self.sublinhas[i][self.pagina] == None:
                                        sublinha, = self.axes[i].plot([key for key in sorted(self.picks[self.pagina])],
                                                [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])], color = 'green')
                                        self.sublinhas[i][self.pagina] = sublinha
                                    else: 
                                        self.sublinhas[i][self.pagina].set_data([key for key in sorted(self.picks[self.pagina])],
                                                [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])]) 
                            if self.indicadores[self.pagina]:
                                for i in self.indicadores[self.pagina]:
                                    if float(i.get_offsets()[0][0]) == nearestMagnetValue:  
                                        i.remove()
                                        self.telas[self.pagina].draw() 
                        elif event.button == 3:
                            self.coordx.append(event.xdata)
                            self.coordy.append(event.ydata)
                            self.linhaPick, = self.axes[self.pagina].plot(self.coordx,self.coordy,color='red')
                            self.clickOn = True
                            if self.linhasPick[self.pagina] != None and bool(self.picks[self.pagina]) == True:
                                self.linhasPick[self.pagina].set_data([key for key in sorted(self.picks[self.pagina])],
                                        [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])])
                                self.telas[self.pagina].draw()
                    except:
                       pass

                def movimento(event):

                    if self.clickOn == True:
                        try:
                            self.coordx.append(event.xdata)
                            self.coordy.append(event.ydata)
                            self.linhaPick.set_data(self.coordx,self.coordy)
                            self.telas[self.pagina].draw()
                            del self.coordx[1:-1]
                            del self.coordy[1:-1]
                        except:
                            pass

                def soltar(event):
                    if self.clickOn == True:
                        try:
                            self.coordx.append(event.xdata)
                            self.coordy.append(event.ydata)
                            m, b = np.polyfit([int(i) for i in self.coordx], self.coordy, 1)
                            self.linhaPick.remove()
                            valorMaisproximo1 = min(self.okpicks, key=lambda x: abs(self.coordx[0] - x))
                            valorMaisproximo2 = min(self.okpicks, key=lambda x: abs(self.coordx[-1] - x))
                            if valorMaisproximo1 < valorMaisproximo2:
                                for i in arange(valorMaisproximo1,valorMaisproximo2+self.valordx, self.valordx):
                                    if i in self.okpicks:
                                        if i in self.picks[self.pagina]:
                                            self.picks[self.pagina][i] = m*i+b
                                            self.picksArts[self.pagina][i].remove()
                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-(self.valordx*0.5),
                                                                                i+(self.valordx*0.5),colors='r',linestyle='solid')
                                            self.picksArts[self.pagina][i] = pickline
                                        else:
                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-(self.valordx*0.5),
                                                                        i+(self.valordx*0.5),colors='r',linestyle='solid')
                                            self.picksArts[self.pagina].update({i:pickline})
                                            self.picks[self.pagina].update({i:m*i+b})
                            else:
                                for i in arange(valorMaisproximo1,valorMaisproximo2-self.valordx, -self.valordx):
                                    if i in self.okpicks:
                                        if i in self.picks[self.pagina]:
                                            self.picks[self.pagina][i] = m*i+b
                                            self.picksArts[self.pagina][i].remove()
                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-(self.valordx*0.5),
                                                                                i+(self.valordx*0.5),colors='r',linestyle='solid')
                                            self.picksArts[self.pagina][i] = pickline
                                        else:
                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-(self.valordx*0.5),
                                                                        i+(self.valordx*0.5),colors='r',linestyle='solid')
                                            self.picksArts[self.pagina].update({i:pickline})
                                            self.picks[self.pagina].update({i:m*i+b})
                            for i in range(len(self.arquivos)):
                                if i != self.pagina:
                                    if self.sublinhas[i][self.pagina] == None:
                                        sublinha, = self.axes[i].plot([key for key in sorted(self.picks[self.pagina])],
                                                [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])], color = 'green')
                                        self.sublinhas[i][self.pagina] = sublinha
                                    else:
                                        self.sublinhas[i][self.pagina].set_data([key for key in sorted(self.picks[self.pagina])],
                                                [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])])
                            if self.linhasPick[self.pagina] != None and bool(self.picks[self.pagina]) == True:
                                self.linhasPick[self.pagina].set_data([key for key in sorted(self.picks[self.pagina])],
                                        [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])])
                            self.telas[self.pagina].draw()
                            del self.coordx[:]
                            del self.coordy[:]
                            self.clickOn = False
                        except:
                            self.clickOn = False
                            self.linhaPick.remove()
                            self.linhaPick = None
                if self.pickVelOn == True:
                    for i in range(len(self.arquivos)):
                        self.figs[i].canvas.mpl_disconnect(self.conVelClick[i])
                        self.figs[i].canvas.mpl_disconnect(self.conVelMov[i])
                        self.figs[i].canvas.mpl_disconnect(self.conVelSoltar[i])
                        self.conVelClick[i] = None
                        self.conVelMov[i] = None
                        self.conVelSoltar[i] = None
                    self.pickVelOn = False
                    self.statusVel.configure(text='',fg='blue') 
                if self.pickAmostraAtivado == True:
                    for i in range(len(self.arquivos)):
                        self.figs[self.pagina].canvas.mpl_disconnect(self.conAmostra[i])
                        self.conAmostra[i] = None
                    self.statusCortador.configure(text='', fg='blue')
                    self.pickAmostraAtivado = False            
                for i in range(len(self.arquivos)):
                    con1 = self.figs[i].canvas.mpl_connect('motion_notify_event', movimento)
                    con2 = self.figs[i].canvas.mpl_connect('button_release_event', soltar)
                    con3 = self.figs[i].canvas.mpl_connect('button_press_event', pick)
                    self.conPickClick[i] = con3
                    self.conPickMov[i] = con1
                    self.conPickSoltar[i] = con2
            else:
                for i in range(len(self.arquivos)):
                    self.figs[i].canvas.mpl_disconnect(self.conPickClick[i])
                    self.figs[i].canvas.mpl_disconnect(self.conPickMov[i])
                    self.figs[i].canvas.mpl_disconnect(self.conPickSoltar[i])
                    self.conPickClick[i] = None
                    self.conPickMov[i] = None
                    self.conPickSoltar[i] = None
                self.pickMode = False
                self.statusPick.configure(text='',fg='blue')

    def verCurva(self):

        if self.plotExiste == True:
            root = Tk()
            root.title('Refrapy - Sispick') 
            fig = plt.figure()
            ax = fig.add_subplot(111)
            for i in range(len(self.arquivos)):
                del self.bolas[i][:]
                del self.indicadores[i][:]
            for i in range(len(self.arquivos)):
                if bool(self.picks[i]) == True:
                    ax.plot([key for key in sorted(self.picks[i])],
                        np.array([self.picks[i][key] for key in sorted(self.picks[i])]))
                    for key in sorted(self.picks[i]):
                        bola = ax.scatter(key, self.picks[i][key],s=40,c = 'white',edgecolors='b',picker = 5)
                        self.bolas[i].append(bola)

            def click(event):
                for i in range(len(self.arquivos)):
                    if event.artist in self.bolas[i]:
                        event.artist.set_color('blue')
                        indicador = self.axes[i].scatter(float(event.artist.get_offsets()[0][0]),
                                float(event.artist.get_offsets()[0][1]), s = 300, c ='blue', alpha = .5)
                        self.indicadores[i].append(indicador)
                        fig.canvas.draw()
                        self.figs[i].canvas.draw()

            plt.title('Preview of travel time curves')    
            plt.xlabel('Distance (m)')
            plt.ylabel('Time (ms)')
            plt.grid()
            canvas = FigureCanvasTkAgg(fig, root)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            fig.canvas.mpl_connect('pick_event', click)
            root.mainloop()

    def ligarPicks(self):

        if self.plotExiste == True:
            if self.linhasPick[self.pagina] == None and bool(self.picks[self.pagina]) == True:
                linhaPick, = self.axes[self.pagina].plot([key for key in sorted(self.picks[self.pagina])],
                        [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])], color = 'red')
                self.linhasPick[self.pagina] = linhaPick
                self.figs[self.pagina].canvas.draw()

            elif self.linhasPick[self.pagina] != None:
                try:
                    self.linhasPick[self.pagina].remove()
                    self.linhasPick[self.pagina] = None
                    self.figs[self.pagina].canvas.draw()
                except:
                    pass

    def removerLinhaPicks(self):

        if self.plotExiste == True:
            if self.linhasPick[self.pagina] != None:
                self.linhasPick[self.pagina].remove()
                self.linhasPick[self.pagina] = None
                self.figs[self.pagina].canvas.draw()

    def limparplot(self):

        if self.plotExiste == True:
            if len(self.picks[self.pagina]) > 0:
                if messagebox.askyesno("Refrapy - Sispick", "Limpar picks do sismograma atual?"):
                    for i in self.picksArts[self.pagina].values():
                        i.remove()
                    self.picks[self.pagina].clear()
                    self.picksArts[self.pagina].clear()
                    self.telas[self.pagina].draw()
                    if self.linhasPick[self.pagina] != None:
                        self.linhasPick[self.pagina].remove()
                        self.linhasPick[self.pagina] = None
                        self.figs[self.pagina].canvas.draw()
                    for i in range(len(self.arquivos)):
                        if i == self.pagina:
                            pass
                        else:
                            if self.sublinhas[i][self.pagina] != None:
                                self.sublinhas[i][self.pagina].remove()
                                self.sublinhas[i][self.pagina] = None    
                        self.telas[i].draw()
                    
    def fecharPlot(self):
          
        if self.plotExiste == True:
            if messagebox.askyesno("Refrapy - Sispick", "Fechar o projeto atual?"):
                for i in self.frames:
                    i.destroy()
                for i in self.axes:
                    i.cla()
                for i in self.figs:
                    i.clf()
                del self.frames[:],self.figs[:],self.axes[:],self.telas[:],self.listSource[:],self.sts[:], \
                    self.ticksLabel[:],self.toolbars[:],self.dadosCrus[:],self.dadosNorms[:],self.ganho[:], \
                    self.filtros[:],self.filtrosHP[:],self.filtrosLP[:],self.copiasCruas[:],self.copiasNorms[:], \
                    self.okpicks[:],self.clips[:],self.sombreamentos[:],self.picks[:],self.picksArts[:],self.ndados[:], \
                    self.freqLP[:],self.freqHP[:],self.coordx[:],self.coordy[:],self.conPickClick[:], \
                    self.conPickMov[:],self.conPickSoltar[:],self.conVelClick[:],self.conVelMov[:],self.conVelSoltar[:], \
                    self.conAmostra[:]
                self.sublinhas.clear()
                self.bolas.clear()
                self.indicadores.clear()
                self.plotArts.clear()
                self.sombArts.clear()
                self.coordsx.clear()
                self.coordsy.clear()
                self.linhasVel.clear()
                self.textoVel.clear()
                self.tracosMax.clear()
                self.plotExiste, self.pickMode, self.yinvertido, self.normalizado, self.optAberto, self.pickAmostraAtivado, \
                self.clickOn,self.pickVelOn = False,False,False,False,False,False,False,False
                self.arquivos, self.formato, self.posicaoGeof1, self.eventCon, self.pagina, self.recordlen, self.valordx, self.linhaVel, \
                self.linhaPick = None,None,None,None,None,None,None,None,None
                self.fatorY, self.valorGanho, self.fatorLP, self.fatorHP = 0.8, 2, 0.8, 1.5
                self.status.configure(text = '',fg='red')
                self.statusPick.configure(text = '',fg='blue')
                self.statusVel.configure(text = '',fg='blue')
                self.statusCortador.configure(text = '',fg='blue')
                self.statusPA.configure(text = '', fg = 'green')
                self.statusPB.configure(text = '', fg = 'green')

    def conferidorIndividual(self):

        if self.clips[self.pagina] == True:
            for j in range(self.canais):
                self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() < self.posicaoGeof1+j*self.valordx-((self.valordx/2)*0.9)] = self.posicaoGeof1+j*self.valordx-((self.valordx/2)*0.9)
                self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() > self.posicaoGeof1+j*self.valordx+((self.valordx/2)*0.9)] = self.posicaoGeof1+j*self.valordx+((self.valordx/2)*0.9)
                self.plotArts[self.pagina][j].set_xdata(self.plotArts[self.pagina][j].get_xdata())
        if self.sombreamentos[self.pagina] == 'neg':
            for j in range(self.canais):
                self.sombArts[self.pagina][:].pop(j).remove()  
            del self.sombArts[self.pagina][:]
            for j in range(self.canais):   
                somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                            self.posicaoGeof1+self.valordx*j,
                            self.plotArts[self.pagina][j].get_xdata(),
                            where = self.plotArts[self.pagina][j].get_xdata() >= self.posicaoGeof1+j*self.valordx,color='black')
                self.sombArts[self.pagina].append(somb)
        elif self.sombreamentos[self.pagina] == 'pos':
            for j in range(self.canais):
                self.sombArts[self.pagina][:].pop(j).remove()    
            del self.sombArts[self.pagina][:]
            for j in range(self.canais):      
                somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                            self.posicaoGeof1+self.valordx*j,
                            self.plotArts[self.pagina][j].get_xdata(),
                            where = self.plotArts[self.pagina][j].get_xdata() <= self.posicaoGeof1+j*self.valordx,color='black')   
                self.sombArts[self.pagina].append(somb)
        self.figs[self.pagina].canvas.draw()

    def conferidorGeral(self):

        for i in range(len(self.arquivos)):    
            if self.clips[i] == True:   
                for j in range(self.canais):
                    self.plotArts[i][j].get_xdata()[self.plotArts[i][j].get_xdata() < self.posicaoGeof1+j*self.valordx-((self.valordx/2)*0.9)] = self.posicaoGeof1+j*self.valordx-((self.valordx/2)*0.9)
                    self.plotArts[i][j].get_xdata()[self.plotArts[i][j].get_xdata() > self.posicaoGeof1+j*self.valordx+((self.valordx/2)*0.9)] = self.posicaoGeof1+j*self.valordx+((self.valordx/2)*0.9)
                    self.plotArts[self.pagina][j].set_xdata(self.plotArts[self.pagina][j].get_xdata())   
            if self.sombreamentos[i] == 'neg':
                for j in range(self.canais):
                    self.sombArts[i][:].pop(j).remove()
                del self.sombArts[i][:]
                for j in range(self.canais):  
                    somb = self.axes[i].fill_betweenx(self.plotArts[i][j].get_ydata(),
                                self.posicaoGeof1+self.valordx*j,
                                self.plotArts[i][j].get_xdata(),
                                where = self.plotArts[i][j].get_xdata() >= self.posicaoGeof1+j*self.valordx,color='black') 
                    self.sombArts[i].append(somb)
            elif self.sombreamentos[i] == 'pos':
                for j in range(self.canais):
                    self.sombArts[i][:].pop(j).remove()           
                del self.sombArts[i][:]
                for j in range(self.canais):          
                    somb = self.axes[i].fill_betweenx(self.plotArts[i][j].get_ydata(),
                                self.posicaoGeof1+self.valordx*j,
                                self.plotArts[i][j].get_xdata(),
                                where = self.plotArts[i][j].get_xdata() <= self.posicaoGeof1+j*self.valordx,color='black')   
                    self.sombArts[i].append(somb)
            self.telas[i].draw()

    def ampup(self):

        if self.plotExiste == True:
            self.ganho[self.pagina] += self.valorGanho
            if self.normalizado == True:
                if self.filtros[self.pagina] != True:
                    for j in range(self.canais):           
                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                else:
                    for j in range(self.canais):      
                        self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx) 
            else:
                if self.filtros[self.pagina] != True:
                    for j in range(self.canais):
                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                else:
                    for j in range(self.canais):     
                        self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
            self.conferidorIndividual()

    def ampdown(self):

        if self.plotExiste == True and self.ganho[self.pagina] > self.valorGanho:
            self.ganho[self.pagina] -= self.valorGanho
            if self.normalizado == True:
                if self.filtros[self.pagina] != True:
                    for j in range(self.canais):       
                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                else:
                    for j in range(self.canais):          
                        self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)               
            else:
                if self.filtros[self.pagina] != True:
                    for j in range(self.canais):
                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                else:
                    for j in range(self.canais):
                        self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
            self.conferidorIndividual()

    def amostrasDefault(self):

        if self.plotExiste == True:
            if int(self.ndados[self.pagina]) != int(len(self.sts[0][0])): 
                if messagebox.askyesno('Refrapy - Sispick', 'Atualizar os plots para número de amostras original (%d)?'%int(len(self.sts[0][0]))):
                    self.ndados[self.pagina] = int(len(self.sts[0][0]))
                    if self.normalizado == True:
                        for j in range(self.canais):
                            self.plotArts[self.pagina][j].set_data(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx,
                                                         [self.sts[self.pagina][0].stats.delta*k*1000 for k in range(int(self.ndados[self.pagina]))])
                    else:
                        for j in range(self.canais):                  
                            self.plotArts[self.pagina][j].set_data(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx,
                                                         [self.sts[self.pagina][0].stats.delta*k*1000 for k in range(int(self.ndados[self.pagina]))])
                    self.axes[self.pagina].set_ylim([0,1000*(self.sts[self.pagina][0].stats.delta*self.ndados[self.pagina])])
                    if self.yinvertido == True:                      
                        plt.figure(self.pagina)
                        plt.gca().invert_yaxis()
                    self.conferidorIndividual()
                    
    def menosy(self):

        if self.plotExiste == True:
            if self.yinvertido == True:
                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[0])*self.fatorY])
                plt.figure(self.pagina)
                plt.gca().invert_yaxis()
            else:
                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[1])*self.fatorY])
            self.figs[self.pagina].canvas.draw()

    def maisy(self):

        if self.plotExiste == True:
            if self.yinvertido == True:
                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[0])/self.fatorY])
                plt.figure(self.pagina)
                plt.gca().invert_yaxis()
            else:
                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[1])/self.fatorY]) 
            self.figs[self.pagina].canvas.draw()

    def normalizar(self):

        if self.plotExiste == True:
            if self.normalizado == False:
                for i in range(len(self.arquivos)):
                    if self.filtros[i] != True:
                        for j in range(self.canais):
                            self.plotArts[i][j].set_xdata(self.dadosNorms[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+self.posicaoGeof1+j*self.valordx)
                    else:
                        messagebox.showinfo('','Retire os filtros aplicados no sismograma para normalizar os traços')
                self.normalizado = True
            else:
                for i in range(len(self.arquivos)):
                    if self.filtros[i] != True:                   
                        for j in range(self.canais):
                            self.plotArts[i][j].set_xdata(self.dadosCrus[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+self.posicaoGeof1+j*self.valordx)
                    else:
                        messagebox.showinfo('','Retire os filtros aplicados no sismograma para desnormalizar os traços')
                self.normalizado = False
            self.conferidorGeral()

    def sombNull(self):

        if self.plotExiste == True:
            if self.sombreamentos[self.pagina] == 'pos' or self.sombreamentos[self.pagina] == 'neg':
                for j in range(self.canais):
                    self.sombArts[self.pagina][:].pop(j).remove()  
                del self.sombArts[self.pagina][:]
                self.figs[self.pagina].canvas.draw()
                self.sombreamentos[self.pagina] = 'null'
    
    def sombNeg(self):

        if self.plotExiste == True:
            if self.sombreamentos[self.pagina] == 'pos' or self.sombreamentos[self.pagina] == 'null':
                try:
                    for j in range(self.canais):
                        self.sombArts[self.pagina][:].pop(j).remove()         
                    del self.sombArts[self.pagina][:]
                except:
                    pass
                for j in range(self.canais): 
                    somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                                self.posicaoGeof1+self.valordx*j,
                                self.plotArts[self.pagina][j].get_xdata(),
                                where = self.plotArts[self.pagina][j].get_xdata() >= self.posicaoGeof1+j*self.valordx,color='black')     
                    self.sombArts[self.pagina].append(somb)
                self.sombreamentos[self.pagina] = 'neg'
                self.figs[self.pagina].canvas.draw()

    def sombPos(self):

        if self.plotExiste == True:
            if self.sombreamentos[self.pagina] == 'neg' or self.sombreamentos[self.pagina] == 'null':
                try:
                    for j in range(self.canais):
                        self.sombArts[self.pagina][:].pop(j).remove()      
                    del self.sombArts[self.pagina][:]
                except:
                    pass
                for j in range(self.canais):   
                    somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                                self.posicaoGeof1+self.valordx*j,
                                self.plotArts[self.pagina][j].get_xdata(),
                                where = self.plotArts[self.pagina][j].get_xdata() <= self.posicaoGeof1+j*self.valordx,color='black')    
                    self.sombArts[self.pagina].append(somb)
                self.sombreamentos[self.pagina] = 'pos'
                self.figs[self.pagina].canvas.draw()

    def clip(self):

        if self.plotExiste == True:
            if self.clips[self.pagina] == False:
                for j in range(self.canais):
                    self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() < self.posicaoGeof1+j*self.valordx-((self.valordx/2)*0.9)] = self.posicaoGeof1+j*self.valordx-((self.valordx/2)*0.9)
                    self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() > self.posicaoGeof1+j*self.valordx+((self.valordx/2)*0.9)] = self.posicaoGeof1+j*self.valordx+((self.valordx/2)*0.9)
                    self.plotArts[self.pagina][j].set_xdata(self.plotArts[self.pagina][j].get_xdata())
                self.clips[self.pagina] = True
            else:
                if self.normalizado == True:
                    for j in range(self.canais):
                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                else:
                    for j in range(self.canais):
                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                self.clips[self.pagina] = False
            if self.sombreamentos[self.pagina] == 'neg':
                for j in range(self.canais):
                    self.sombArts[self.pagina][:].pop(j).remove()      
                del self.sombArts[self.pagina][:]
                for j in range(self.canais):      
                    somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                                self.posicaoGeof1+self.valordx*j,
                                self.plotArts[self.pagina][j].get_xdata(),
                                where = self.plotArts[self.pagina][j].get_xdata() >= self.posicaoGeof1+j*self.valordx,color='black')   
                    self.sombArts[self.pagina].append(somb)
            elif self.sombreamentos[self.pagina] == 'pos':
                for j in range(self.canais):
                    self.sombArts[self.pagina][:].pop(j).remove()       
                del self.sombArts[self.pagina][:]
                for j in range(self.canais):        
                    somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                                self.posicaoGeof1+self.valordx*j,
                                self.plotArts[self.pagina][j].get_xdata(),
                                where = self.plotArts[self.pagina][j].get_xdata() <= self.posicaoGeof1+j*self.valordx,color='black')      
                    self.sombArts[self.pagina].append(somb)
            self.figs[self.pagina].canvas.draw()
  
    def invert(self):

        if self.plotExiste == True:
            if self.yinvertido == False:
                for i in range(len(self.arquivos)):   
                    plt.figure(i)
                    plt.gca().invert_yaxis()
                    self.figs[i].canvas.draw()
                self.yinvertido = True
            elif self.yinvertido == True:
                for i in range(len(self.arquivos)):    
                    plt.figure(i)
                    plt.gca().invert_yaxis()
                    self.figs[i].canvas.draw()
                self.yinvertido = False

    def removerFiltros(self):

        if self.plotExiste == True:
            if self.filtros[self.pagina] == True:
                if self.normalizado == True:
                    for j in range(self.canais):
                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                    self.copiasNorms[self.pagina] = None
                else:
                    for j in range(self.canais):
                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
                    self.copiasCruas[self.pagina] = None
                self.statusPA.configure(text = '')
                self.statusPB.configure(text = '')
                self.filtros[self.pagina] = False
                self.filtrosHP[self.pagina] = False
                self.filtrosLP[self.pagina] = False
                self.freqLP[self.pagina] = 1000
                self.freqHP[self.pagina] = 5
                self.conferidorIndividual()
                self.telas[self.pagina].draw()

    def filtroLP(self):

        if self.plotExiste == True:
            if self.normalizado == True:
                if self.filtros[self.pagina] != True:
                    self.copiasNorms[self.pagina] = self.sts[self.pagina].copy().normalize()
                    self.copiasNorms[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Low pass: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP
                else:
                    self.copiasNorms[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Low pass: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP           
                for j in range(self.canais):
                    self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
            else:
                if self.filtros[self.pagina] != True:
                    self.copiasCruas[self.pagina] = self.sts[self.pagina].copy().normalize(1)
                    self.copiasCruas[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Low pass: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP
                else:
                    self.copiasCruas[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Low pass: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP            
                for j in range(self.canais):
                    self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
            self.filtrosLP[self.pagina] = True        
            self.filtros[self.pagina] = True
            self.conferidorIndividual()
            self.telas[self.pagina].draw()

    def filtroHP(self):

        if self.plotExiste == True:
            if self.normalizado == True:
                if self.filtros[self.pagina] != True:
                    self.copiasNorms[self.pagina] = self.sts[self.pagina].copy().normalize()
                    self.copiasNorms[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'High pass: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP
                else:
                    self.copiasNorms[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'High pass: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP         
                for j in range(self.canais):
                    self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
            else:
                if self.filtros[self.pagina] != True:
                    self.copiasCruas[self.pagina] = self.sts[self.pagina].copy().normalize(1)
                    self.copiasCruas[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'High pass: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP
                else:
                    self.copiasCruas[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'High pass: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP = self.freqHP[self.pagina]*self.fatorHP         
                for j in range(self.canais):
                    self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)
            self.filtrosHP[self.pagina] = True
            self.filtros[self.pagina] = True
            self.conferidorIndividual()
            self.telas[self.pagina].draw()

    def salvargp(self):

        if not self.picks[:]:
            messagebox.showerror('Refrapy - Sispick','Nao há picks')
        else:
            try:
                arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('Refrapy pick', '*.rp')])
                if platform.system() == 'Windows':
                    with open(arquivoSaida+'.rp','a') as arqpck:
                        arqpck.write("%d %d\n%.2f %.2f\n"%(len(self.listSource),self.canais,self.posicaoGeof1,self.valordx))
                        for i in range(len(self.arquivos)):       
                            for key in sorted(self.picks[i]):   
                                arqpck.write('%f %f 1\n'%(key,self.picks[i][key]))    
                            arqpck.write('/ %f\n'%(float(self.listSource[i])))
                    arqpck.close()
                elif platform.system() == 'Linux':
                    with open(arquivoSaida,'a') as arqpck:
                        for i in range(len(self.arquivos)):       
                            for key in sorted(self.picks[i]):    
                                arqpck.write('%f %f 1\n'%(key,self.picks[i][key])) 
                            arqpck.write('/ %f\n'%(float(self.listSource[i])))
                    arqpck.close()  
                messagebox.showinfo('Refrapy - Sispick','Pick salvo')
            except:
                pass

    def salvarpick(self):

        if not self.picks[:]:
            messagebox.showerror('Refrapy - Sispick','Nao há picks')
        else:  
            try:   
                arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('Seisimager', '.vs')])
                if platform.system() == 'Windows':
                    with open(arquivoSaida+'.vs','a') as arqpck:
                        arqpck.write('1996 0 3.0\n0 %d %f\n'%(len(self.arquivos),self.valordx))
                        for i in range(len(self.arquivos)):
                            arqpck.write('%f %d 0.0\n'%(float(self.listSource[i]), self.canais))     
                            for key in sorted(self.picks[i]):    
                                arqpck.write('%f %f 1 \n'%(key,self.picks[i][key]))
                        arqpck.write('0 0 \n 0 \n 0 0 \n')
                    arqpck.close()
                elif platform.system() == 'Linux':
                    with open(arquivoSaida,'a') as arqpck:
                        arqpck.write('1996 0 3.0\n0 %d %f\n'%(len(self.arquivos),self.valordx))
                        for i in range(len(self.arquivos)):
                            arqpck.write('%f %d 0.0\n'%(float(self.listSource[i]), self.canais))     
                            for key in sorted(self.picks[i]):    
                                arqpck.write('%f %f 1 \n'%(key,self.picks[i][key]))
                        arqpck.write('0 0 \n 0 \n 0 0 \n')
                    arqpck.close()  
                messagebox.showinfo('Refrapy - Sispick','Pick salvo')
            except:
                pass

    def pickVelocidade(self):

        if self.plotExiste == True:
            if self.pickVelOn == False:
                self.statusVel.configure(text = 'Apparent velocity mode on',fg='blue')
                def clicar(event):
                    try:
                        self.coordsx[self.pagina].append(event.xdata)
                        self.coordsy[self.pagina].append(event.ydata)
                        self.linhaVel, = self.axes[self.pagina].plot(self.coordsx[self.pagina],
                                        self.coordsy[self.pagina],color='blue')
                        self.linhasVel[self.pagina].append(self.linhaVel)
                        self.clickOn = True
                    except:
                        pass

                def movimento(event):

                    if self.clickOn == True:
                        try:
                            self.coordsx[self.pagina].append(event.xdata)
                            self.coordsy[self.pagina].append(event.ydata)
                            self.linhaVel.set_data(self.coordsx[self.pagina],self.coordsy[self.pagina])
                            self.figs[self.pagina].canvas.draw()
                            del self.coordsx[self.pagina][1:-1]
                            del self.coordsy[self.pagina][1:-1]
                        except:
                            pass

                def soltar(event):

                    try:
                        self.coordsx[self.pagina].append(event.xdata)
                        self.coordsy[self.pagina].append(event.ydata)
                        self.linhaVel.set_data(self.coordsx[self.pagina],self.coordsy[self.pagina])
                        slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(self.coordsx[self.pagina]),
                                                            np.array(self.coordsy[self.pagina]))
                        if np.isnan(slope) == False:
                            ltex = self.axes[self.pagina].text(self.coordsx[self.pagina][0],self.coordsy[self.pagina][0], '%.2f m/s'%(abs(1/slope)*1000),
                                        size=12, rotation=0, color = 'blue', ha="center", va="center",bbox = dict(ec='1',fc='1'))
                            self.textoVel[self.pagina].append(ltex)
                            self.figs[self.pagina].canvas.draw()
                            del self.coordsx[self.pagina][:]
                            del self.coordsy[self.pagina][:]
                            self.clickOn = False
                    except:
                        pass
                if self.pickMode == True:

                    for i in range(len(self.arquivos)):
                        self.figs[i].canvas.mpl_disconnect(self.conPickClick[i])
                        self.figs[i].canvas.mpl_disconnect(self.conPickMov[i])
                        self.figs[i].canvas.mpl_disconnect(self.conPickSoltar[i])
                        self.conPickClick[i] = None
                        self.conPickMov[i] = None
                        self.conPickSoltar[i] = None  
                    self.pickMode = False
                    self.statusPick.configure(text='',fg='blue')
                if self.pickAmostraAtivado == True:
                    for i in range(len(self.arquivos)):
                        self.figs[self.pagina].canvas.mpl_disconnect(self.conAmostra[i])
                        self.conAmostra[i] = None
                    self.statusCortador.configure(text='', fg='blue')
                    self.pickAmostraAtivado = False
                for i in range(len(self.arquivos)):
                    con1 = self.figs[i].canvas.mpl_connect('motion_notify_event', movimento)
                    con2 = self.figs[i].canvas.mpl_connect('button_release_event', soltar)
                    con3 = self.figs[i].canvas.mpl_connect('button_press_event', clicar)
                    self.conVelClick[i] = con3
                    self.conVelMov[i] = con1
                    self.conVelSoltar[i] = con2
                self.pickVelOn = True
            else:
                self.statusVel.configure(text = '',fg='blue')
                self.pickVelOn = False
                for i in range(len(self.arquivos)):
                    self.figs[i].canvas.mpl_disconnect(self.conVelClick[i])
                    self.figs[i].canvas.mpl_disconnect(self.conVelMov[i])
                    self.figs[i].canvas.mpl_disconnect(self.conVelSoltar[i])
                    self.conVelClick[i] = None
                    self.conVelMov[i] = None
                    self.conVelSoltar[i] = None
                    for j,k in zip(self.linhasVel[i],self.textoVel[i]):
                        j.remove()
                        k.remove()   
                    self.figs[i].canvas.draw()
                for i in range(len(self.arquivos)): 
                    del self.linhasVel[i][:]
                    del self.textoVel[i][:]    

    def pickAmostra(self):

        if self.plotExiste == True:
            self.statusCortador.configure(text=' Corte ativado', fg='blue')
            def pick(event):
                if int((event.ydata/self.sts[0][0].stats.delta)/1000) <= int(len(self.sts[0][0])):
                    marcador = self.axes[self.pagina].hlines(event.ydata,float(self.axes[0].get_xlim()[0]),
                                            float(self.axes[0].get_xlim()[1]),colors='r',linestyle='--',
                                            alpha = 1,linewidth = 3)
                    self.figs[self.pagina].canvas.draw()
                    if messagebox.askyesno('Refrapy - Sispick', 'Cortar o plot para %d ms?'%int(event.ydata)):
                        marcador.remove()
                        self.ndados[self.pagina] = int((event.ydata/self.sts[0][0].stats.delta)/1000)
                        if self.normalizado == True:
                            for j in range(self.canais):
                                self.plotArts[self.pagina][j].set_data(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx,
                                                             [self.sts[self.pagina][0].stats.delta*k*1000 for k in range(int(self.ndados[self.pagina]))])
                        else:
                            for j in range(self.canais):
                                self.plotArts[self.pagina][j].set_data(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx,
                                                             [self.sts[self.pagina][0].stats.delta*k*1000 for k in range(int(self.ndados[self.pagina]))])
                        self.axes[self.pagina].set_ylim([0,1000*(self.sts[self.pagina][0].stats.delta*self.ndados[self.pagina])])
                        if self.yinvertido == True:
                            plt.figure(self.pagina)
                            plt.gca().invert_yaxis()
                            self.figs[self.pagina].canvas.draw()
                        for i in range(len(self.arquivos)):
                            self.figs[i].canvas.mpl_disconnect(self.conAmostra[i])
                            self.conAmostra[i] = None
                        self.pickAmostraAtivado = False
                        self.statusCortador.configure(text='',fg='blue')
                        self.conferidorIndividual()
                    else:                      
                        for i in range(len(self.arquivos)):
                            self.figs[self.pagina].canvas.mpl_disconnect(self.conAmostra[i])
                            self.conAmostra[i] = None   
                        self.statusCortador.configure(text='',fg='blue')
                        self.pickAmostraAtivado = False
                        marcador.remove()
                        self.figs[self.pagina].canvas.draw()
            if self.pickAmostraAtivado == False:
                if self.pickVelOn == True:
                    for i in range(len(self.arquivos)):
                        self.figs[i].canvas.mpl_disconnect(self.conVelClick[i])
                        self.figs[i].canvas.mpl_disconnect(self.conVelMov[i])
                        self.figs[i].canvas.mpl_disconnect(self.conVelSoltar[i])
                        self.conVelClick[i] = None
                        self.conVelMov[i] = None
                        self.conVelSoltar[i] = None
                    self.pickVelOn = False
                    self.statusVel.configure(text='',fg='blue')
                if self.pickMode == True:
                    for i in range(len(self.arquivos)):
                        self.figs[i].canvas.mpl_disconnect(self.conPickClick[i])
                        self.figs[i].canvas.mpl_disconnect(self.conPickMov[i])
                        self.figs[i].canvas.mpl_disconnect(self.conPickSoltar[i])
                        self.conPickClick[i] = None
                        self.conPickMov[i] = None
                        self.conPickSoltar[i] = None 
                    self.pickMode = False
                    self.statusPick.configure(text='',fg='blue')
                for i in range(len(self.arquivos)):
                    cid = self.figs[i].canvas.mpl_connect('button_press_event', pick)
                    self.conAmostra[i] = cid
                self.statusCortador.configure(text='Corte ativado', fg='blue')                    
                self.pickAmostraAtivado = True
            else:
                for i in range(len(self.arquivos)):
                    self.figs[self.pagina].canvas.mpl_disconnect(self.conAmostra[i])
                    self.conAmostra[i] = None    
                self.statusCortador.configure(text='', fg='blue')
                self.pickAmostraAtivado = False

    def cabecalho (self):

        if self.plotExiste == True:
            root = Tk()
            root.geometry('430x300')
            root.title('Refrapy - Sispick')
            root.resizable(0,0)
            fonte = StringVar()
            dx = StringVar()
            comp = StringVar()
            pos1 = StringVar()
            main = Label(root, text = 'Dados do cabeçalho (%s)'%os.path.basename(self.arquivos[self.pagina]),font=("Helvetica", 14),
                         fg='green').grid(row = 0, column = 0, sticky='w', padx = 10, pady = 10)
            fonte = Label(root, text = 'Posição da fonte (atual: %.2f m):'%float(self.listSource[self.pagina]),font=("Helvetica", 10),
                         fg='black').grid(row = 1, column = 0, sticky='w', padx = 10, pady = 10)
            espacamento = Label(root, text = 'Espaçamento entre geofones (atual: %.2f m):'%float(self.valordx),font=("Helvetica", 10),
                         fg='black').grid(row = 2, column = 0, sticky='w', padx = 10, pady = 10)
            comp = Label(root, text = 'Comprimento do perfil (atual: %.2f m):'%(self.valordx*len(self.sts[self.pagina])),
                         font=("Helvetica", 10),fg='black').grid(row = 3, column = 0, sticky='w', padx = 10, pady = 10)
            pos = Label(root, text = 'Posiçao do primeiro geofone (atual: %.2f m):'%self.posicaoGeof1,
                           font=("Helvetica", 10),fg='black').grid(row = 4, column = 0, sticky='w', padx = 10, pady = 10)
            entryf = Entry(root, textvariable = fonte, width=10)
            entryf.grid(row = 1, column = 0, sticky = 'w', pady = 10, padx = 250)
            entrydx = Entry(root, textvariable = dx, width=10)
            entrydx.grid(row = 2, column = 0, sticky = 'w', pady = 10, padx = 330)
            entrycomp = Entry(root, textvariable = comp, width=10)
            entrycomp.grid(row = 3, column = 0, sticky = 'w', pady = 10, padx = 290)
            entrypos1 = Entry(root, textvariable = pos1, width=10)
            entrypos1.grid(row = 4, column = 0, sticky = 'w', pady = 10, padx = 290)
            warning = Label(root, text = ' ', fg = 'red',font=("Helvetica", 12))
            warning.grid(row = 6, column = 0, sticky = 'w', padx = 100, pady= 10)
            
            def salvar():

                if len(entryf.get()) > 0:
                    try:
                        self.listSource[self.pagina] = float(entryf.get())
                        warning.configure(text = 'Dados salvos', fg = 'blue') 
                    except:
                        warning.configure(text = 'Posição de fonte inválida', fg = 'red')
                if len(entrydx.get()) > 0:  
                    try:
                        self.valordx = float(entrydx.get())
                        self.okpicks = [self.posicaoGeof1+self.valordx*j for j in range(self.canais)]
                        warning.configure(text = 'Dados salvos', fg = 'blue')
                        if self.normalizado == True:
                            for i in range(len(self.arquivos)):
                                for j in range(self.canais):
                                    self.plotArts[i][j].set_data(self.dadosNorms[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+self.posicaoGeof1+j*self.valordx,
                                                                 [self.sts[i][0].stats.delta*1000*k for k in range(int(self.ndados[i]))])
                                self.axes[i].set_xlim(self.posicaoGeof1-self.valordx,self.posicaoGeof1+self.valordx*len(self.sts[i]))        
                        else:
                            for i in range(len(self.arquivos)):
                                for j in range(self.canais):
                                    self.plotArts[i][j].set_data(self.dadosCrus[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+self.posicaoGeof1+j*self.valordx,
                                                                 [self.sts[i][0].stats.delta*k*1000 for k in range(int(self.ndados[i]))])
                                self.axes[i].set_xlim(self.posicaoGeof1-self.valordx,self.posicaoGeof1+self.valordx*len(self.sts[i]))
                        self.conferidorGeral()    
                    except:
                        warning.configure(text = 'Espaçamento entre geofones inválido', fg = 'red')
                if len(entrycomp.get()) > 0: 
                    try:
                        warning.configure(text = 'Dados salvos', fg = 'blue')
                        for i in range(len(self.arquivos)):
                            plt.figure(i)
                            self.axes[i].set_xlim(self.posicaoGeof1-self.valordx,self.posicaoGeof1+float(entrycomp.get()))
                            self.telas[i].draw()    
                    except:
                        warning.configure(text = 'Comprimento de perfil inválido', fg = 'red')
                if len(entrypos1.get()) > 0:
                    self.posicaoGeof1 = float(entrypos1.get())
                    self.okpicks = [self.posicaoGeof1+self.valordx*j for j in range(self.canais)]
                    if self.normalizado == True:
                        for i in range(len(self.arquivos)):
                            for j in range(self.canais):
                                self.plotArts[i][j].set_data(self.dadosNorms[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+self.posicaoGeof1+j*self.valordx,
                                                             [self.sts[i][0].stats.delta*1000*k for k in range(int(self.ndados[i]))])
                            self.axes[i].set_xlim(self.posicaoGeof1-self.valordx,self.posicaoGeof1+self.valordx*len(self.sts[i]))    
                    else:
                        for i in range(len(self.arquivos)):
                            for j in range(self.canais):
                                self.plotArts[i][j].set_data(self.dadosCrus[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+self.posicaoGeof1+j*self.valordx,
                                                             [self.sts[i][0].stats.delta*k*1000 for k in range(int(self.ndados[i]))])
                            self.axes[i].set_xlim(self.posicaoGeof1-self.valordx,self.posicaoGeof1+self.valordx*len(self.sts[i]))
                    self.conferidorGeral()

            def fechar():
                root.destroy()

            save = Button(root, text = 'Salvar',font=("Helvetica", 12), width = 6,
                    command = salvar).grid(row = 5, column = 0, sticky = 'w', padx = 80, pady = 10)
            fechar = Button(root, text = 'Fechar',font=("Helvetica", 12), width = 6,
                    command = fechar).grid(row = 5, column = 0, sticky = 'w', padx = 220, pady = 10)
            root.mainloop()

    def configPlot(self):

        if self.plotExiste == True and self.optAberto == False:
            root = Tk()
            root.geometry('420x350+500+250')
            root.title('Refrapy - Sispick')
            vardx = StringVar()
            varY = StringVar()
            varGain = StringVar()    
            varFigx = StringVar()
            varFigy = StringVar()
            mainLabel = Label(root, text='Configurações de plot',
                        font=("Helvetica", 14),fg='green').grid(row=0, column=0, sticky="w",pady=15,padx=110)
            labelY = Label(root, text='Fator de corte temporal (atual: %.1f): '%self.fatorY,
                           font=("Helvetica", 10)).grid(row=1, column=0, sticky="w",padx=20,pady=10)
            entryY = Entry(root, textvariable = varY,width=10)
            entryY.grid(row=1, column=0, sticky="w",padx=235,pady=10)
            labelGain = Label(root, text='Fator de ganho (atual: %.1f): '%self.valorGanho,
                              font=("Helvetica", 10)).grid(row=2, column=0, sticky="w",padx=20,pady=10)
            entryGain = Entry(root, textvariable = varGain,width=10)
            entryGain.grid(row=2, column=0, sticky="w",padx=235,pady=10)
            '''labelFigx = Label(root, text='Tamanho x do plot (atual: %.1f): '%self.valorFigx,
                              font=("Helvetica", 10)).grid(row=3, column=0, sticky="w",padx=20,pady=10)
            entryFigx = Entry(root, textvariable = varFigx,width=10)
            entryFigx.grid(row=3, column=0, sticky="w",padx=235,pady=10)
            labelFigy = Label(root, text='Tamanho y do plot (atual: %.1f): '%self.valorFigy,
                              font=("Helvetica", 10)).grid(row=4, column=0, sticky="w",padx=20,pady=10)
            entryFigy = Entry(root, textvariable = varFigy,width=10)
            entryFigy.grid(row=4, column=0, sticky="w",padx=235,pady=10)'''
            warning = Label(root, text='',font=("Helvetica", 12),fg = 'red')
            warning.grid(row=6, column=0, sticky="w",pady=0,padx=140)

            def fechar():

                self.optAberto = False
                root.destroy()
                
            def do():

                if len(entryY.get()) > 0:
                    try:
                        self.fatorY = float(entryY.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')
                    except:
                        warning.configure(text='Corte temporal inválido',fg = 'red')
                if len(entryGain.get()) > 0:
                    try:
                        self.valorGanho = float(entryGain.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')
                    except:
                        warning.configure(text='Fator de ganho inválido',fg = 'red')
                '''if len(entryFigx.get()) > 0:
                    try:
                        self.valorFigx = float(entryFigx.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')
                        for i in range(len(self.arquivos)):
                            plt.figure(i)
                            plt.gcf().set_size_inches(self.valorFigx, self.valorFigy,forward=True)
                            self.figs[i].canvas.draw()
                    except:
                        warning.configure(text='Tamanho x inválido',fg = 'red')
                if len(entryFigy.get()) > 0:
                    try:
                        self.valorFigy = float(entryFigy.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')
                        for i in range(len(self.arquivos)):
                            plt.figure(i)
                            plt.gcf().set_size_inches(self.valorFigx, self.valorFigy,forward=True)
                            self.figs[i].canvas.draw()
                    except:
                         warning.configure(text='Tamanho y inválido',fg = 'red')'''

            def cancelar():

                self.optAberto = False
                root.destroy()

            botaoOK = Button(root, text='Aplicar', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black',width=8, command = do).grid(row=5, column=0, sticky="w",pady=20,padx=110)
            botaoX = Button(root, text='Fechar', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black',width=8, command = cancelar).grid(row=5, column=0, sticky="w",padx=260,pady=20)
            root.bind('<Return>', lambda x: do())
            root.resizable(0,0)
            root.protocol("WM_DELETE_WINDOW", fechar)
            self.optAberto = True
            root.mainloop()

    def configDx(self):                 
        
        root = Tk()   
        root.geometry('455x230+500+250')
        root.title('Refrapy - Sispick')
        vardx = StringVar()
        mainLabel = Label(root, text='O espaçamento entre geofones não foi encontrado no cabeçalho\ndo arquivo. Insira manualmente no campo abaixo',
                    font=("Helvetica", 11),fg='red').grid(row=0, column=0, sticky="w",pady=15,padx=5)
        labeldx = Label(root, text='Espaçamento entre geofones (metros): ',
                    font=("Helvetica", 12)).grid(row=2, column=0, sticky="w",padx=20,pady=10)
        entrydx = Entry(root, textvariable = vardx,width=10)
        entrydx.grid(row=2, column=0, sticky="w",padx=310,pady=10)
        warning = Label(root, text = '', fg = 'red',font=("Helvetica", 12))
        warning.grid(row = 6, column = 0, sticky = 'w', pady = 5, padx = 180)
        
        def do():
            
            if len(entrydx.get()) > 0:
                try:
                    self.valordx = float(entrydx.get())
                    root.destroy()
                    self.abrir_pt2()
                except: 
                    warning.configure(text = 'Valor inválido')
            else:
                messagebox.showinfo('Refrapy - Sispick', 'Espaçamento entre geofones padrão será usado: 2 m')
                self.valordx = 2
                root.destroy()
                self.abrir_pt2()
                                    
        def cancelar():

            messagebox.showinfo('Refrapy - Sispick', 'Espaçamento entre geofones padrão será usado: 2 m')
            self.valordx = 2
            root.destroy()
            self.abrir_pt2()
        
        botaoOK = Button(root, text='   Ok   ', bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',width=8, command = do).grid(row=5, column=0, sticky="w",pady=20,padx=110)
        botaoX = Button(root, text='Ignorar', bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',width=8, command = cancelar).grid(row=5, column=0, sticky="w",padx=260,pady=20)
        entrydx.focus()
        root.bind('<Return>', lambda x: do())
        root.resizable(0,0)
        root.protocol("WM_DELETE_WINDOW", cancelar)
        root.mainloop()

root = Tk()
Sispick(root)
root.mainloop()
