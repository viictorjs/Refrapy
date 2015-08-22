
from tkinter import * 
from tkinter import filedialog, messagebox
from obspy import read
import matplotlib
matplotlib.use('TkAgg')                                                                  
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import os                                                                              
import numpy as np

liststreams = []                                
sispickOn = False
sisconOn = False

class Launcher(Tk):
    
    def __init__(self):

        Tk.__init__(self)
        print('\n Geosis v1.0 em execuçao.\n\n Fechar esta janela resultará no fechamento do programa.\n')
        self.geometry('640x400')
        self.title('Geosis v1.0')
        self.parentLauncher = Frame(self)
        self.parentLauncher.grid(row=0,column=0,sticky='nsew')
        self.barraDEmenu = Menu(self)
        self.configure(menu=self.barraDEmenu)
        self.menu_modulos=Menu(self.barraDEmenu)
        self.barraDEmenu.add_cascade(label='Módulos',menu=self.menu_modulos)
        self.menu_modulos.add_command(label='Sispick',
                                      command= self.chamarSispick)
        self.menu_modulos.add_command(label='Siscon',
                                      command= self.chamarSiscon)
        self.menu_ajuda = Menu(self.barraDEmenu)
        self.barraDEmenu.add_cascade(label='Ajuda',menu=self.menu_ajuda)
        self.menu_ajuda.add_command(label='Módulos',command = self.SobreModulos)
        self.menu_ajuda.add_command(label='Sobre o software',command = self.Sobre)

        try:
            
            photo = PhotoImage(file="%s/imagens/unb_geof.gif"%os.getcwd())

        except:

            messagebox.showerror('',"Arquivos faltando na pasta 'imagens'")
            
        label = Label(self.parentLauncher,image=photo)
        label.image = photo
        label.grid(row=0,column=0,sticky='nsew')
        botaoSispick = Button(self.parentLauncher, text='sispick',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSispick)
        botaosiscon = Button(self.parentLauncher, text='siscon',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSiscon)
        botaoSispick.grid(row=0,column=0,padx=50,sticky='w')
        botaosiscon.grid(row=0,column=0,padx=50,sticky='e')
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

    def fechar(self):

        if messagebox.askyesno("Geosis", "Fechar o launcher?"):
            
            self.destroy()

        else:

            pass

    def chamarSispick(self):

        global sispickOn
        
        if sispickOn == True:

            pass

        else:

            sispickOn = True
            Sispick()

    def chamarSiscon(self):

        global sisconOn

        if sisconOn == True:

            pass

        else:

            sisconOn = True
            Siscon()

    def Sobre(self):

        root = Tk()
        root.geometry('630x300')
        root.title('Info')
        titulo = Label(root, text='Sobre o software',fg='green',font=("Helvetica", 14))
        label1 = Label(root, text='Geosis 1.0 é um pactode de programas de código aberto para visualização e processamento de',
                      fg='black',font=("Helvetica", 10))
        label2 = Label(root, text='dados sísmicos, originalmente desenvolvido pelo estudante de geofísica da UnB, Victor José,',
                      fg='black',font=("Helvetica", 10))
        label3 = Label(root, text='orientado pelo professor Marcelo Peres Rocha.',fg='black',font=("Helvetica", 10))
        label4 = Label(root, text='Sendo fruto de um projeto de iniciação científica (PIBIC), o software foi desenvolvido em Python 3.4',
                       fg='black',font=("Helvetica", 10))
        label5 = Label(root, text='fazendo uso das seguintes principais bibliotecas livres:',
                       fg='black',font=("Helvetica", 10))
        label6 = Label(root, text='ObsPy 0.10.2 (M. Beyreuther, R. Barsch, L. Krischer, T. Megies, Y. Behr and J. Wassermann)',
                       fg='black',font=("Helvetica", 10))
        label7 = Label(root, text='Matplotlib 1.4.3 (John D. Hunter)',
                       fg='black',font=("Helvetica", 10))
        titulo.grid(row=0, column=0, sticky="w",pady=15,padx=20)
        label1.grid(row=2, column=0, sticky="w",pady=0,padx=20)
        label2.grid(row=3, column=0, sticky="w",pady=0,padx=20)
        label3.grid(row=4, column=0, sticky="w",pady=0,padx=20)
        label4.grid(row=5, column=0, sticky="w",pady=0,padx=20)
        label5.grid(row=6, column=0, sticky="w",pady=0,padx=20)
        label6.grid(row=7, column=0, sticky="w",pady=10,padx=20)
        label7.grid(row=8, column=0, sticky="w",pady=0,padx=20)
        root.resizable(0,0)
        root.mainloop()

    def SobreModulos(self):

        root = Tk()
        root.geometry('670x300')
        root.title('Info')
        titulo = Label(root, text='Sobre os módulos',fg='green',font=("Helvetica", 14))
        label1 = Label(root, text='Geosis v1.0 possui dois módulos prontos para uso: sispick e siscon.',
                      fg='black',font=("Helvetica", 10))
        label2 = Label(root, text='O módulo sispick é uma ferramenta para visualização e processamento de sismogramas formato seg2, segy',
                      fg='black',font=("Helvetica", 10))
        label3 = Label(root, text='e mseed. Edições de traço disponíveis: normalização, sombreamento, ganho, clip e pick de primeira chegada.',fg='black',font=("Helvetica", 10))
        label4 = Label(root, text='O módulo siscon é uma ferramenta para conversão de formatos de arquivos sísmicos. A conversão de',fg='black',font=("Helvetica", 10))
        label5 = Label(root, text='formatos segue a ordem seg2/segy/mseed para segy/mseed.',
                       fg='black',font=("Helvetica", 10))
        titulo.grid(row=0, column=0, sticky="w",pady=15,padx=20)
        label1.grid(row=2, column=0, sticky="w",pady=0,padx=20)
        label2.grid(row=3, column=0, sticky="w",pady=0,padx=20)
        label3.grid(row=4, column=0, sticky="w",pady=0,padx=20)
        label4.grid(row=5, column=0, sticky="w",pady=0,padx=20)
        label5.grid(row=6, column=0, sticky="w",pady=0,padx=20)
        root.resizable(0,0)
        root.mainloop()
        

class Sispick(Tk):
    
    def __init__(self):                         

        Tk.__init__(self)                       
        self.configure(background='#F3F3F3')
        self.geometry('800x400+310+150')        
        self.title('Geosis - Sispick')               

        # LISTAS
        
        self.frames = []                        
        self.figs = []                          
        self.axes = []                      
        self.telas = []                    
        self.listSource = []                    
        self.sts = []                        
        self.ticksLabel = []                    
        self.toolbars = []
        self.stsNorms = []
        self.ganho = []
        self.okpicks = []
        self.clips = []
        self.sombreamentos = []
        self.listSource = []
        self.picks = []
        self.picksArts = []
        self.linhasArts = []
        self.conexoesPick = []
        self.dadosCrus = []
        self.dadosNorms = []

        #DICIONARIOS
                          
        self.plotArts = {}
        self.sombArts = {}
        self.trClipados = {}

        #BOOLEANS
                         
        self.plotExiste = False                 
        self.pickMode = False                                                
        self.pickHappened = False               
        self.yinvertido = False
        self.seg2 = False
        self.normalizado = False
        self.optAberto = False

        #VARIAVEIS NAO BOOLEANS

        self.eventCon = None                                          
        self.pagina = None
        self.recordlen = None                   
        self.valordx = None                                  
        self.valorY = 0.4
        self.valorGanho = 1.2
        
        self.valorFigx = self.winfo_screenwidth()/80.50

        if self.winfo_screenheight() == 1080:
            
            self.valorFigy = self.winfo_screenheight()/93.10

        elif self.winfo_screenheight() == 768:

            self.valorFigy = self.winfo_screenheight()/99.74

        elif self.winfo_screenheight() == 1024:

            self.valorFigy = self.winfo_screenheight()/94.1

        elif self.winfo_screenheight() == 900:

            self.valorFigy = self.winfo_screenheight()/96.5

        elif self.winfo_screenheight() == 720:

            self.valorFigy = self.winfo_screenheight()/101.5

        else: # 800

            self.valorFigy = self.winfo_screenheight()/99
                                     
        self.eixoy = None
        
        self.parent = Frame(self,bg='#F3F3F3')
        self.parent.grid(row=0,column=0,sticky='nsew')
        self.barraDEmenu = Menu(self)
        self.configure(menu=self.barraDEmenu)
        self.menu_arquivo=Menu(self.barraDEmenu)
        self.barraDEmenu.add_cascade(label='Arquivo',menu=self.menu_arquivo)
        self.menu_arquivo.add_command(label='Abrir                    Ctrl+A',
                                      command=self.abrir_pt1)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label='Salvar pick .vs           Ctrl+S',
                                      command=self.salvarpick)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label='Sair                         Alt+S',
                                      command=self.destroy)
        self.menu_visualizar = Menu(self.barraDEmenu)
        self.barraDEmenu.add_cascade(label='Visualizaçao',menu=self.menu_visualizar)
        self.menu_visualizar.add_command(label='Proximo                Direita',
                                         command=self.nextpage)
        self.menu_visualizar.add_command(label='Anterior                Esquerda',
                                         command=self.backpage)
        self.menu_visualizar.add_separator()
        self.menu_visualizar.add_command(label='Inverter eixo y       I',
                                         command=self.backpage)
        self.menu_visualizar.add_separator()
        self.menu_visualizar.add_command(label='Diminuir eixo y      Baixo',
                                         command=self.menosy)
        self.menu_visualizar.add_command(label='Aumentar eixo y    Cima',
                                         command=self.maisy)
        self.menu_editar = Menu(self.barraDEmenu)
        self.barraDEmenu.add_cascade(label='Editar',menu=self.menu_editar)
        self.menu_editar.add_command(label='Ativar/Desativar pick                  P',
                                     command=self.ativarPick)
        self.menu_editar.add_separator()
        self.menu_editar.add_command(label='Dar ganho                                 Shift + Direita',
                                     command=self.ampup)
        self.menu_editar.add_command(label='Retirar ganho                            Shift + Esquerda',
                                     command=self.ampdown)
        self.menu_editar.add_separator()
        self.menu_editar.add_command(label='Aplicar/Retirar normalizaçao       N',
                                     command=self.normalizar)
        self.menu_editar.add_command(label='Aplicar/Retirar sombreamento    S',
                                     command=self.fill)
        self.menu_editar.add_command(label='Clipar         C',
                                     command=self.clip)
        self.menu_editar.add_separator()
        self.menu_editar.add_command(label='Limpar plot                                L',
                                     command=self.limparplot)
        self.menu_editar.add_separator()
        self.menu_editar.add_command(label='Fechar seçao atual                     Ctrl+X',
                                     command=self.fecharPlot)
        self.menu_opcoes = Menu(self.barraDEmenu)
        self.barraDEmenu.add_cascade(label='Opçoes',menu=self.menu_opcoes)
        self.menu_opcoes.add_command(label='Opções de plot          Ctrl+O',command=self.configPlot)
       # self.menu_opçoes.add_command(label='Opçoes de pick',command=self.ativarPick)
        self.menu_ajuda = Menu(self.barraDEmenu)
        self.barraDEmenu.add_cascade(label='Ajuda',menu=self.menu_ajuda)
        self.menu_ajuda.add_command(label='Atalhos de teclado',command = lambda: print('oi'))
        self.Back = Button(self.parent, text='<',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = 'chartreuse3',activeforeground='white',
                      activebackground = 'chartreuse2', command = self.backpage)
        self.Back.grid(row=0,column=0,sticky=W)
        self.Next = Button(self.parent, text='>',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = 'chartreuse3',activeforeground='white',
                      activebackground = 'chartreuse2', command = self.nextpage)
        self.Next.grid(row=0,column=1,sticky=W)
        self.ampDown = Button(self.parent, text='-',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                              bg = 'gold2',activeforeground='white',
                         activebackground = 'yellow2', command = self.ampdown)
        self.ampDown.grid(row=0,column=2,sticky=W)
        self.ampUp = Button(self.parent, text='+',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                            bg = 'gold2',activeforeground='white',
                       activebackground = 'yellow2', command = self.ampup)
        self.ampUp.grid(row=0,column=3,sticky=W)
        self.menosY = Button(self.parent, text='- T',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                             bg = 'DarkOrange2',activeforeground='white',
                            activebackground = 'orange2', command = self.menosy)
        self.menosY.grid(row=0,column=4,sticky=W)
        self.maisY = Button(self.parent, text='+T',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                            bg = 'DarkOrange2',activeforeground='white',
                            activebackground = 'orange2', command = self.maisy)
        self.maisY.grid(row=0,column=5,sticky=W)
        self.Pick = Button(self.parent, text='P', bg = 'red3',font=("Arial", 10,'bold'),width = 4,
                           activebackground = 'red2',
                      activeforeground = 'white', command = self.ativarPick)
        self.Pick.grid(row=0,column=6,sticky=W)
        self.limpar = Button(self.parent, text='L', bg = 'snow2',font=("Arial", 10,'bold'),width = 4,
                           activebackground = 'snow',
                      activeforeground = 'black', command = self.limparplot)
        self.limpar.grid(row=0,column=7,sticky=W)
        self.inverttime = Button(self.parent, text='I',width = 4,font=("Arial", 10,'bold'),
                                 fg= 'black', bg = 'goldenrod4',activeforeground='white',
                            activebackground = 'gold3', command = self.invert)
        self.inverttime.grid(row=0,column=8,sticky=W)
        self.normal = Button(self.parent, text='N',fg= 'black',font=("Arial", 10,'bold'),
                             width = 4, bg = 'purple2',activeforeground='white',
                            activebackground = 'DarkOrchid1', command = self.normalizar)
        self.normal.grid(row=0,column=9,sticky=W)
        self.FILL = Button(self.parent, text='S',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = 'blue2',activeforeground='white',
                            activebackground = 'royal blue', command = self.fill)
        self.FILL.grid(row=0,column=10,sticky=W)
        self.clipar = Button(self.parent, text='C',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = 'bisque4',activeforeground='white',
                            activebackground = 'bisque3', command = self.clip)
        self.clipar.grid(row=0,column=11,sticky=W)
        self.FecharPlot = Button(self.parent, text='x', bg = 'gray3',font=("Arial", 10,'bold'),
                                 width = 4,fg='white', activebackground = 'gray30',
                            activeforeground = 'gold2', command = self.fecharPlot)
        self.FecharPlot.grid(row=0,column=12,sticky=W)
        self.status = Label(self.parent,text = ' ', fg='red',font=("Helvetica", 12))
        self.status.grid(row=0,column=13,sticky=E)
        
        plt.rcParams['keymap.zoom'] = 'z'
        plt.rcParams['keymap.back'] = 'v'
        plt.rcParams['keymap.home'] = 'ctrl+z'
        plt.rcParams['keymap.save'] = 'ctrl+s'
        plt.rcParams['keymap.pan'] = 'ctrl+P'
        self.bind('<Alt-s>', lambda x: self.destroy())
        self.bind('<Alt-S>', lambda x: self.destroy())
        self.bind('<Control-a>', lambda x: self.abrir_pt1())
        self.bind('<Control-A>', lambda x: self.abrir_pt1())
        self.bind('<Control-s>', lambda x: self.salvarpick())
        self.bind('<Control-S>', lambda x: self.salvarpick())
        self.bind('<Control-x>', lambda x: self.fecharPlot())
        self.bind('<Control-X>', lambda x: self.fecharPlot())
        self.bind('<Control-o>', lambda x: self.configPlot())
        self.bind('<Control-O>', lambda x: self.configPlot())
        self.bind('<Shift-Left>', lambda x: self.ampdown())
        self.bind('<Shift-Right>', lambda x: self.ampup())
        self.bind('<Up>', lambda x: self.maisy())
        self.bind('<Down>', lambda x: self.menosy())
        self.bind('i', lambda x: self.invert())
        self.bind('n', lambda x: self.normalizar())
        self.bind('s', lambda x: self.fill())
        self.bind('c', lambda x: self.clip())
        self.bind('I', lambda x: self.invert())
        self.bind('N', lambda x: self.normalizar())
        self.bind('S', lambda x: self.fill())
        self.bind('s', lambda x: self.fill())
        self.bind('C', lambda x: self.clip())
        self.bind('P', lambda x: self.ativarPick())
        self.bind('p', lambda x: self.ativarPick())
        self.bind('<Left>', lambda x: self.backpage())
        self.bind('<Right>', lambda x: self.nextpage())
        self.protocol("WM_DELETE_WINDOW", self.fechar)
    
        self.mainloop()

    def fechar(self):

        global sispickOn

        if messagebox.askyesno("Geosis - Sispick", "Sair do programa?"):

            sispickOn = False

            if self.plotExiste == True:

                self.fecharPlot()

            else:

                pass
            
            self.destroy()

        else:

            pass

    def abrir_pt1(self):
        
        if self.plotExiste == False:
                    
            self.arquivos = filedialog.askopenfilenames(title='Abrir',filetypes=[('seg2','*.dat'),('segy','*.sgy'),
                                                                           ('mseed','*.mseed'),('Todos os arquivos','*.*')])

        else:
        
            messagebox.showinfo('','Feche a seçao sismica atual para abrir uma nova')

        if len(self.arquivos)>0:

            self.configDx()

        else:

            pass

    def abrir_pt2(self):

        self.status.configure(text=' Abrindo %d arquivo(os). Aguarde...'%len(self.arquivos))

        try:
        
            for i in range(len(self.arquivos)):

                self.frame = Frame(self,bg='#F3F3F3')
                self.frame.grid(row=1, column=0,sticky='nsew')
                self.frames.append(self.frame)

                fig = plt.figure(i,figsize=(self.valorFigx,self.valorFigy),facecolor='#F3F3F3')
                self.figs.append(fig)

                ax = self.figs[i].add_subplot(111)
                self.axes.append(ax)
                
                self.sts.append(read(self.arquivos[i]))

                self.stsNorms.append(self.sts[i].copy())

                self.sts[i].normalize(1)
                self.stsNorms[i].normalize()

                self.plotArts[i] = []
                self.sombArts[i] = []
                self.trClipados[i] = []
                self.picks.append({})
                self.picksArts.append({})
                self.linhasArts.append({})
                self.dadosCrus.append({})
                self.dadosNorms.append({})
                
                self.canais = len(self.sts[0])                      
                self.recordlen = self.sts[0][0].stats.endtime-self.sts[0][0].stats.starttime
                self.lenPerfil = float((self.canais*self.valordx)-self.valordx)
                self.intervaloAmostragem = self.sts[0][0].stats.delta

                try:
                    
                    self.listSource.append(self.sts[i][0].stats.seg2['SOURCE_LOCATION'])
                    self.seg2 = True

                except:

                    self.seg2 = False
                    pass
                    
                self.ganho.append(1)
                self.clips.append(False)
                self.sombreamentos.append(False)
                
                for j in range(self.canais):

                    self.dadosCrus[i][j] = []
                    self.dadosNorms[i][j] = []

                    for k in self.sts[i][j]:

                        self.dadosCrus[i][j].append(k)

                    for k in self.stsNorms[i][j]:

                        self.dadosNorms[i][j].append(k)

                    self.trClipados[i].append([])

                    self.okpicks.append(self.valordx*j)
                    
                    self.ticksLabel.append(str(int(j*self.valordx)))

                    traco, = self.axes[i].plot([k*1.3+j*self.valordx for k in self.dadosCrus[i][j]],
                                               [self.sts[i][0].stats.delta*k for k in range(len(self.dadosCrus[i][j]))],color='black')
                    self.plotArts[i].append(traco)
                    
                #plt.figure(i)
                plt.title(' %s | %d canais'%(self.arquivos[i],int(self.canais)))     
                plt.xlabel('Distância (m)')
                plt.ylabel('Tempo (s)')
                plt.ylim(0,self.recordlen)
                plt.xlim(-self.valordx,self.lenPerfil+self.valordx)
                #plt.xticks(int(self.ticksLabel),self.ticksLabel)
                    
                tela = FigureCanvasTkAgg(self.figs[i], self.frames[i])
                self.telas.append(tela)
                self.telas[i].show()
                self.telas[i].get_tk_widget().pack(fill='both', expand=True)
                toolbar = NavigationToolbar2TkAgg(self.telas[i], self.frames[i])
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
            self.eixoy = self.recordlen
            
        except:

            self.status.configure(text=' ')
            messagebox.showerror('Geosis - Sispick','Aquivo inválido')
    

    def nextpage(self):
        
        if self.plotExiste == True and self.pagina < len(self.arquivos)-1:
            
            frame = self.frames[self.pagina+1]
            frame.tkraise()
            self.pagina += 1
            
        else:
            
            pass

    def backpage(self):

        if self.plotExiste == True and self.pagina == 0:
                
             pass

        elif self.plotExiste == True and self.pagina != 0:
                
            frame = self.frames[self.pagina-1] 
            frame.tkraise()
            self.pagina -= 1
                
        else:
            
            pass
                    
    def ativarPick(self):
        
        if self.plotExiste == True:

            if self.pickMode == False:

                self.pickMode = True
                self.status.configure(text=' Pick ativado',fg='blue')
                
                def pick(event):

                    try:

                        nearestMagnetValue = min(self.okpicks, key=lambda x: abs(event.xdata - x))
                        
                        if nearestMagnetValue in self.picks[self.pagina]:

                            self.picks[self.pagina][nearestMagnetValue] = event.ydata
                            self.picksArts[self.pagina][nearestMagnetValue].remove()
                            pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-0.5,
                                                                nearestMagnetValue+0.5,colors='r',linestyle='solid')
                            self.picksArts[self.pagina][nearestMagnetValue] = pickline
                            self.telas[self.pagina].show()

                            for i in range(len(self.arquivos)):

                                if i == self.pagina:

                                    pass

                                else:

                                    self.linhasArts[i][nearestMagnetValue].remove()
                                    linhasverdes = self.axes[i].hlines(event.ydata,nearestMagnetValue-0.5,
                                                                nearestMagnetValue+0.5,colors='green',linestyle='solid')
                                    self.linhasArts[i][nearestMagnetValue] = linhasverdes
                                    self.telas[i].show()
                                    
                        else:
                            
                            pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-0.5,
                                                                nearestMagnetValue+0.5,colors='r',linestyle='solid')
                            self.picksArts[self.pagina].update({nearestMagnetValue:pickline})
                            self.picks[self.pagina].update({nearestMagnetValue:event.ydata})
                            self.telas[self.pagina].show()

                            for i in range(len(self.arquivos)):

                                if i == self.pagina:

                                    pass

                                else:

                                    linhasverdes = self.axes[i].hlines(event.ydata,nearestMagnetValue-0.5,
                                                                nearestMagnetValue+0.5,colors='green',linestyle='solid')
                                    self.linhasArts[i].update({nearestMagnetValue:linhasverdes})
                                    self.telas[i].show()
                            
                            self.pickHappened = True

                    except:

                        pass
                
                for i in range(len(self.arquivos)):
                    
                    cid = self.figs[i].canvas.mpl_connect('button_press_event', pick)
                    self.conexoesPick.append(cid)

            else:

                for i in range(len(self.arquivos)):
                    
                    self.figs[i].canvas.mpl_disconnect(self.conexoesPick[i])
                    
                del self.conexoesPick[:]

                self.pickMode = False
                self.status.configure(text=' ',fg='red')
        
        else:

            pass

    def limparplot(self):

        if self.plotExiste == True:

            if len(self.picks[self.pagina]) > 0:

                if messagebox.askyesno("Geosis - Sispick", "Limpar picks do sismograma atual?"):

                    for i in self.picksArts[self.pagina].values():
                    
                        i.remove()

                    self.picks[self.pagina].clear()
                    self.picksArts[self.pagina].clear()
                    self.telas[self.pagina].show()

                    for i in range(len(self.arquivos)):

                        if i == self.pagina:

                            pass

                        else:

                            for j in self.linhasArts[i].values():

                                j.remove()

                        self.linhasArts[i].clear()
                        self.telas[i].show()

                else:

                    pass

            else:

                pass   

        else:

            pass
                    
    def fecharPlot(self):
          
        if self.plotExiste == True:

            if messagebox.askyesno("Geosis - Sispick", "Fechar o projeto atual?"):

                for i in self.frames:

                    i.destroy()

                del self.frames[:]

                for i in self.axes:

                    i.cla()
                    
                del self.axes[:]

                for i in self.figs:

                    i.clf()
                    
                del self.figs[:]

                del self.telas[:]

                del self.listSource[:]

                del self.sts[:]

                del self.ticksLabel[:]

                del self.toolbars[:]

                del self.stsNorms[:]

                del self.ganho[:]

                del self.okpicks[:]

                del self.clips[:]

                del self.sombreamentos[:]

                del self.picks[:]

                del self.picksArts[:]

                del self.linhasArts[:]

                del self.conexoesPick[:]

                self.plotArts.clear()
                self.sombArts.clear()
                self.trClipados.clear()

                for i in self.dadosCrus:

                    i.clear()

                for i in self.dadosNorms:

                    i.clear()

                del self.dadosCrus[:]
                del self.dadosNorms[:]

                self.plotExiste = False                                 
                self.pickMode = False                                             
                self.pickHappened = False               
                self.yinvertido = False
                self.seg2 = False
                self.eventCon = None                                          
                self.pagina = None
                self.recordlen = None                   
                self.valordx = None                                  
                self.valorY = 0.4
                self.valorGanho = 1.2
                self.valorFigx = self.winfo_screenwidth()/80.50

                if self.winfo_screenheight() == 1080:
                    
                    self.valorFigy = self.winfo_screenheight()/93.10

                elif self.winfo_screenheight() == 768:

                    self.valorFigy = self.winfo_screenheight()/99.74

                elif self.winfo_screenheight() == 1024:

                    self.valorFigy = self.winfo_screenheight()/94.1

                elif self.winfo_screenheight() == 900:

                    self.valorFigy = self.winfo_screenheight()/96.5

                elif self.winfo_screenheight() == 720:

                    self.valorFigy = self.winfo_screenheight()/101.5

                else: # 800

                    self.valorFigy = self.winfo_screenheight()/99
                                    
                self.eixoy = None
                self.normalizado = False

                self.status.configure(text = '',fg='red')

            else:

                pass

        else:

            pass

    def ampup(self):

        if self.plotExiste == True:

            self.status.configure(text=' Aplicando ganho...')

            self.ganho[self.pagina] += self.valorGanho

            if self.normalizado == True:

                for j in range(self.canais):
                    
                    self.plotArts[self.pagina][j].set_xdata([(k*130*self.ganho[self.pagina]+j*self.valordx*100)/100 for k in self.dadosNorms[self.pagina][j]])

            else:

                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata([(k*130*self.ganho[self.pagina]+j*self.valordx*100)/100 for k in self.dadosCrus[self.pagina][j]])

            if self.clips[self.pagina] == True:

                for j in range(self.canais):

                    if len(self.trClipados[self.pagina][j]) > 0:

                        del self.trClipados[self.pagina][j][:]                      

                    for i in self.plotArts[self.pagina][j].get_xdata():

                        if i < (j*self.valordx)-((self.valordx/2)*0.9):

                            self.trClipados[self.pagina][j].append((j*self.valordx)-((self.valordx/2)*0.9))

                        elif i > (j*self.valordx)+((self.valordx/2)*0.9):
                            
                            self.trClipados[self.pagina][j].append((j*self.valordx)+((self.valordx/2)*0.9))

                        else:

                            self.trClipados[self.pagina][j].append(i)

                    self.plotArts[self.pagina][j].set_xdata(self.trClipados[self.pagina][j])

            else:

                pass
             
            if self.sombreamentos[self.pagina] == True:

                for j in range(self.canais):
                    
                    self.sombArts[self.pagina][:].pop(j).remove()
                    
                del self.sombArts[self.pagina][:]

                self.sombreamentos[self.pagina] = False
                self.fill()

            else:

                pass

            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        else:

            pass

    def ampdown(self):

        if self.plotExiste == True and self.ganho[self.pagina] > self.valorGanho:

            self.status.configure(text=' Removendo ganho...')

            self.ganho[self.pagina] -= self.valorGanho

            if self.normalizado == True:

                for j in range(self.canais):
                    
                    self.plotArts[self.pagina][j].set_xdata([(k*130*self.ganho[self.pagina]+j*self.valordx*100)/100 for k in self.dadosNorms[self.pagina][j]])
                    
            else:

                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata([(k*130*self.ganho[self.pagina]+j*self.valordx*100)/100 for k in self.dadosCrus[self.pagina][j]])

            if self.clips[self.pagina] == True:

                for j in range(self.canais):

                    if len(self.trClipados[self.pagina][j]) > 0:

                        del self.trClipados[self.pagina][j][:]                      

                    for i in self.plotArts[self.pagina][j].get_xdata():

                        if i < (j*self.valordx)-((self.valordx/2)*0.9):

                            self.trClipados[self.pagina][j].append((j*self.valordx)-((self.valordx/2)*0.9))

                        elif i > (j*self.valordx)+((self.valordx/2)*0.9):
                            
                            self.trClipados[self.pagina][j].append((j*self.valordx)+((self.valordx/2)*0.9))

                        else:

                            self.trClipados[self.pagina][j].append(i)

                    self.plotArts[self.pagina][j].set_xdata(self.trClipados[self.pagina][j])

            else:

                pass
                
            if self.sombreamentos[self.pagina] == True:

                for j in range(self.canais):
                    
                    self.sombArts[self.pagina][:].pop(j).remove()
                    
                del self.sombArts[self.pagina][:]

                self.sombreamentos[self.pagina] = False
                self.fill()

            else:

                pass

            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        else:

            pass

    def menosy(self):

        if self.plotExiste == True and self.eixoy - self.valorY > 0:

            self.eixoy -= self.valorY

            for i in range(len(self.arquivos)):
                
                plt.figure(i)
                plt.ylim(0,self.eixoy)

                if self.yinvertido == True:

                    plt.gca().invert_yaxis()

                else:

                    pass
                
                self.figs[i].canvas.draw()
     
        else:

            pass

    def maisy(self):

        if self.plotExiste == True and self.eixoy + 0.4 < self.recordlen:

            self.eixoy += self.valorY

            for i in range(len(self.arquivos)):
                
                plt.figure(i)
                plt.ylim(0,self.eixoy)

                if self.yinvertido == True:

                    plt.gca().invert_yaxis()

                else:

                    pass
                
                self.figs[i].canvas.draw()

        else:

            pass

    def normalizar(self):

        if self.plotExiste == True:

            if self.normalizado == False:

                self.status.configure(text=' Normalizando traços...')

                for i in range(len(self.arquivos)):                

                    for j in range(self.canais):

                        self.plotArts[i][j].set_xdata([(k*130*self.ganho[i]+j*self.valordx*100)/100 for k in self.dadosNorms[i][j]])

                self.normalizado = True

            else:

                self.status.configure(text=' Removendo normalização de traços...')

                for i in range(len(self.arquivos)):
                    
                    for j in range(self.canais):

                        self.plotArts[i][j].set_xdata([(k*130*self.ganho[i]+j*self.valordx*100)/100 for k in self.dadosCrus[i][j]])

                self.normalizado = False

            for i in range(len(self.arquivos)):
                
                if self.clips[i] == False:

                    pass

                else:

                    for j in range(self.canais):

                        if len(self.trClipados[i][j]) > 0:

                            del self.trClipados[i][j][:]                      

                        for k in self.plotArts[i][j].get_xdata():

                            if k < (j*self.valordx)-((self.valordx/2)*0.9):

                                self.trClipados[i][j].append((j*self.valordx)-((self.valordx/2)*0.9))

                            elif k > (j*self.valordx)+((self.valordx/2)*0.9):
                                
                                self.trClipados[i][j].append((j*self.valordx)+((self.valordx/2)*0.9))

                            else:

                                self.trClipados[i][j].append(k)

                        self.plotArts[i][j].set_xdata(self.trClipados[i][j])

                if self.sombreamentos[i] == False:

                    pass
                            
                else:

                    for j in range(self.canais):
                
                        self.sombArts[i][:].pop(j).remove()
            
                    del self.sombArts[i][:]

                    for j in range(self.canais):
            
                        somb = self.axes[i].fill_betweenx(self.plotArts[i][j].get_ydata(),
                                        j*self.valordx,self.plotArts[i][j].get_xdata(),
                                        where=np.array(self.plotArts[i][j].get_xdata())>=j*self.valordx,color='black')

                        self.sombArts[i].append(somb)

                self.figs[i].canvas.draw()
                
            self.status.configure(text=' ')

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass
            
        else:

            pass

    def fill(self):
                
        if self.plotExiste == True and self.sombreamentos[self.pagina] == False:

            self.status.configure(text=' Aplicando sombreamento...')
            
            for j in range(self.canais):
                
                somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][0].get_ydata(),j*self.valordx,
                                                            self.plotArts[self.pagina][j].get_xdata(),
                                            where= np.array(self.plotArts[self.pagina][j].get_xdata()) >= j*self.valordx,color='black')
                    
                self.sombArts[self.pagina].append(somb)

            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')
                
            self.sombreamentos[self.pagina]=True

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        elif self.plotExiste == True and self.sombreamentos[self.pagina] == True:

            self.status.configure(text=' Removendo sombreamento...')

            for j in range(self.canais):

                self.sombArts[self.pagina][:].pop(j).remove()
                
            del self.sombArts[self.pagina][:]
            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')

            self.sombreamentos[self.pagina]=False

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        else:

            pass

    def clip(self):

        if self.plotExiste == True:

            if self.clips[self.pagina] == False:

                self.status.configure(text=' Clipando traços...')

                for j in range(self.canais):

                    if len(self.trClipados[self.pagina][j]) > 0:

                        del self.trClipados[self.pagina][j][:]                      

                    for i in self.plotArts[self.pagina][j].get_xdata():

                        if i < (j*self.valordx)-((self.valordx/2)*0.9):

                            self.trClipados[self.pagina][j].append((j*self.valordx)-((self.valordx/2)*0.9))

                        elif i > (j*self.valordx)+((self.valordx/2)*0.9):
                            
                            self.trClipados[self.pagina][j].append((j*self.valordx)+((self.valordx/2)*0.9))

                        else:

                            self.trClipados[self.pagina][j].append(i)

                    self.plotArts[self.pagina][j].set_xdata(self.trClipados[self.pagina][j])

                self.clips[self.pagina] = True

            else:

                self.status.configure(text=' Removendo clip de traços...')

                if self.normalizado == True:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata([(k*130*self.ganho[self.pagina]+j*self.valordx*100)/100 for k in self.dadosNorms[self.pagina][j]])

                else:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata([(k*130*self.ganho[self.pagina]+j*self.valordx*100)/100 for k in self.dadosCrus[self.pagina][j]])

                self.clips[self.pagina] = False
                
            if self.sombreamentos[self.pagina] == True:

                for j in range(self.canais):
                    
                    self.sombArts[self.pagina][:].pop(j).remove()
                    
                del self.sombArts[self.pagina][:]

                self.sombreamentos[self.pagina] = False
                self.fill()

            else:

                pass

            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        else:

            pass
  
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

        else:

            pass

    def salvarpick(self):

        if not self.picks[:]:

            messagebox.showerror('Geosis - Sispick','Nao há picks')
            
        else:
            
            try:
                
                arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('Seisimager', '.vs')])
                
                with open(arquivoSaida+'.vs','a') as arqpck:

                    arqpck.write('1996 0 3.0\n0 %d %f\n'%(len(self.arquivos),self.valordx))

                    for i in range(len(self.arquivos)):

                        if self.seg2 == True:

                            arqpck.write('%f %d 0.0\n'%(float(self.listSource[i]), self.canais))

                        else:

                            arqpck.write('0.0 %d 0.0\n'%self.canais)
                            
                        for key in sorted(self.picks[i]):
                            
                            arqpck.write('%f %f 1 \n'%(key,self.picks[i][key]*1000))

                    arqpck.write('0 0 \n 0 \n 0 0 \n')

                arqpck.close()
                messagebox.showinfo('Geosis - Sispick','Pick salvo')

            except:

                pass

    def configPlot(self):

        if self.plotExiste == True and self.optAberto == False:

            root = Tk()
            root.geometry('420x350+500+250')
            root.title('Sismograma')
            frame = Frame(root)
            frame.grid(row = 0, column = 0, sticky = 'nsew')

            vardx = StringVar()
            varY = StringVar()
            varGain = StringVar()    
            varFigx = StringVar()
            varFigy = StringVar()
            
            mainLabel = Label(frame, text='Configurações de plot',font=("Helvetica", 14),fg='green')
            mainLabel.grid(row=0, column=0, sticky="w",pady=15,padx=110)
            labelY = Label(frame, text='Corte temporal (atual: %.1f s): '%self.valorY,font=("Helvetica", 12))
            entryY = Entry(frame, textvariable = varY,width=10)
            labelY.grid(row=1, column=0, sticky="w",padx=20,pady=10)
            entryY.grid(row=1, column=0, sticky="w",padx=310,pady=10)
            labelGain = Label(frame, text='Fator de ganho (atual: %.1f): '%self.valorGanho,font=("Helvetica", 12))
            entryGain = Entry(frame, textvariable = varGain,width=10)
            labelGain.grid(row=2, column=0, sticky="w",padx=20,pady=10)
            entryGain.grid(row=2, column=0, sticky="w",padx=310,pady=10)
            labelFigx = Label(frame, text='Tamanho x do plot (atual: %.1f): '%self.valorFigx,font=("Helvetica", 12))
            entryFigx = Entry(frame, textvariable = varFigx,width=10)
            labelFigx.grid(row=3, column=0, sticky="w",padx=20,pady=10)
            entryFigx.grid(row=3, column=0, sticky="w",padx=310,pady=10)
            labelFigy = Label(frame, text='Tamanho y do plot (atual: %.1f): '%self.valorFigy,font=("Helvetica", 12))
            entryFigy = Entry(frame, textvariable = varFigy,width=10)
            labelFigy.grid(row=4, column=0, sticky="w",padx=20,pady=10)
            entryFigy.grid(row=4, column=0, sticky="w",padx=310,pady=10)
            warning = Label(frame, text='',font=("Helvetica", 12),fg = 'red')
            warning.grid(row=6, column=0, sticky="w",pady=0,padx=140)

            def fechar():

                self.optAberto = False
                frame.destroy()
                root.destroy()
                
            def do():

                if len(entryY.get()) > 0:

                    try:

                        self.valorY = float(entryY.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')

                    except:

                        warning.configure(text='Corte temporal inválido',fg = 'red')

                if len(entryGain.get()) > 0:

                    try:

                        self.valorGanho = float(entryGain.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')

                    except:

                        warning.configure(text='Fator de ganho inválido',fg = 'red')

                if len(entryFigx.get()) > 0:

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

                         warning.configure(text='Tamanho y inválido',fg = 'red')

            def cancelar():

                frame.destroy()
                self.optAberto = False
                root.destroy()

            botaoOK = Button(frame, text='Aplicar', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black',width=8, command = do)
            botaoX = Button(frame, text='Fechar', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black',width=8, command = cancelar)
            botaoOK.grid(row=5, column=0, sticky="w",pady=20,padx=110)
            botaoX.grid(row=5, column=0, sticky="w",padx=260,pady=20)
            root.bind('<Return>', lambda x: do())
            root.resizable(0,0)
            root.protocol("WM_DELETE_WINDOW", fechar)
            self.optAberto = True
            root.mainloop()

        elif self.plotExiste == True and self.optAberto == True:

            pass

        else:

            pass

    def configDx(self):                 
        
        root = Tk()   
        root.geometry('455x230+500+250')
        root.title('Sismograma')
        self.frame = Frame(root)
        vardx = StringVar()
        self.frame.grid(row=0, column=0, sticky="nsew")
        mainLabel = Label(self.frame, text='Configuração inicial',font=("Helvetica", 14),fg='blue')
        mainLabel.grid(row=0, column=0, sticky="w",pady=15,padx=50)
        labeldx = Label(self.frame, text='Espaçamento entre geofones (metros): ',font=("Helvetica", 12))
        entrydx = Entry(self.frame, textvariable = vardx,width=10)
        labeldx.grid(row=2, column=0, sticky="w",padx=20,pady=10)
        entrydx.grid(row=2, column=0, sticky="w",padx=310,pady=10)
        
        def do():
            
            if len(entrydx.get()) > 0:

                try:
                
                    self.valordx = float(entrydx.get())
                    self.frame.destroy()
                    root.destroy()
                    self.abrir_pt2()

                except:
                    
                    self.warning = Label(self.frame, text='Valor inválido',font=("Helvetica", 12),fg = 'red')
                    self.warning.grid(row=6, column=0, sticky="w",pady=0,padx=140)

            else:
                
                aviso = Label(self.frame, text='Preencha o campo em branco',font=("Helvetica", 12),fg = 'red')
                aviso.grid(row=6, column=0, sticky="w",pady=0,padx=140)
                                    
        def cancelar():

            self.frame.destroy()
            root.destroy()
            self.label.destroy()

        
        botaoOK = Button(self.frame, text='   Ok   ', bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',width=8, command = do)
        botaoX = Button(self.frame, text='Cancelar', bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',width=8, command = cancelar)
        botaoOK.grid(row=5, column=0, sticky="w",pady=20,padx=110)
        botaoX.grid(row=5, column=0, sticky="w",padx=260,pady=20)
        entrydx.focus()
        root.bind('<Return>', lambda x: do())
        root.resizable(0,0)
        root.mainloop()
   

class Siscon(Tk):
    
    def __init__(self):

        Tk.__init__(self)           
        self.geometry('260x320+600+200')
        self.title('Geosis - Siscon')
        self.formatos = ['SEGY','MSEED']
        self.frame = Frame(self)
        self.nome_formato = StringVar()
        strEntrada = StringVar()
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.labelEntrada = Label(self.frame, text='Arquivos de entrada:',fg='black',font=("Helvetica", 12))
        self.labelSaida = Label(self.frame, text='Diretório de saída:',fg='black',font=("Helvetica", 12))
        self.botaoEntrada = Button(self.frame, text=' ... ', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black', command = self.entrada,width = 4)
        self.botaoSaida = Button(self.frame, text=' ... ', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black', command = self.saida,width = 4)
        self.label1 = Label(self.frame, text='Converter para:',fg='black',font=("Helvetica", 12))
        self.labelEntrada.grid(row=0, column=0, sticky="w",pady=15,padx=20)
        self.botaoEntrada.grid(row=0,column=0,padx=180)
        self.botaoSaida.grid(row=4,column=0,padx=180)
        self.label1.grid(row=1, column=0, sticky="w",pady=15,padx=20)
        self.labelSaida.grid(row=4, column=0, sticky="w",pady=15,padx=20)
        self.rb1 = Radiobutton(self.frame, text=self.formatos[0], variable =  self.nome_formato, value = self.formatos[0],
                          command = self.select1)
        self.rb2 = Radiobutton(self.frame, text=self.formatos[1], variable =  self.nome_formato, value = self.formatos[1],
                          command = self.select2)
        self.rb1.grid(row=2, column=0, sticky="w",padx=20)
        self.rb2.grid(row=3, column=0, sticky="w",padx=20)
        self.botaoOK = Button(self.frame, text=' Converter ', bg = 'gray90',fg='black',width=8,font=("Helvetica", 11),
                              activebackground = 'gray93', activeforeground = 'black', command = self.formatar)
        self.botaoX = Button(self.frame, text='Cancelar', bg = 'gray90',fg='black',width=8,font=("Helvetica", 11),
                             activebackground = 'gray93',activeforeground = 'black', command = self.cancelar)
        self.botaoOK.grid(row=5, column=0,sticky='w',padx=20,pady=20)
        self.botaoX.grid(row=5, column=0)
        self.warning = Label(self.frame, text='',fg = 'red',font=("Helvetica", 11))
        self.warning.grid(row = 6, column = 0, sticky='w',padx=20)
        self.resizable(0,0)
        self.select = False
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.mainloop()

    def fechar(self):

        global sisconOn

        if messagebox.askyesno("Geosis - Siscon", "Sair do programa?"):

            sisconOn = False
            self.destroy()

        else:

            pass
        
    def entrada(self):

        global liststreams
         
        self.Arquivos = filedialog.askopenfilenames(title='Abrir',filetypes=(('seg2','*.dat'),
                                                ('segy','*.sgy'),('mseed','*.mseed'),('Todos os arquivos','*.*')))

        try:
            
            for i in self.Arquivos:
                liststreams.append(read(i))

            entradaOK = Label(self.frame, text='OK',fg = 'blue',font=("Helvetica", 11))
            entradaOK.grid(row=0,column=0,sticky='e',padx=150)

        except:

            messagebox.showerror('Geosis - Siscon','Arquivo inválido')

    def saida(self):

        self.arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('segy','*.sgy'),('mseed','*.mseed')])
                                                        
        if len(self.arquivoSaida)>0:
            
            saidaOK = Label(self.frame, text='OK',fg = 'blue',font=("Helvetica", 11))
            saidaOK.grid(row=4,column=0,sticky='e',padx=150)
            
        else:
            
            pass
                
    def formatar(self):

        global liststreams

        if len(self.Arquivos) == 0:

            self.warning.configure(text='Nenhum arquivo selecionado')

        elif self.select == False:

            self.warning.configure(text='Marque uma opção')

        elif len(self.arquivoSaida) == 0:

            self.warning.configure(text='Escolha o diretório de saída')
        
        elif self.select == True and len(self.Arquivos) > 0 and len(self.arquivoSaida) > 0:
            
            if self.nome_formato.get() == 'SEGY':

                try:
                    
                    for i in liststreams:
                        
                        i.write(self.arquivoSaida+'.sgy',format=self.nome_formato.get())

                    messagebox.showinfo('Geosis - Siscon','Conversão concluida')
                    
                except:

                    messagebox.showerror('Geosis - Siscon','Formato inválido')

            elif self.nome_formato.get() == 'MSEED':

                try:
                     
                    for i in liststreams:
                        
                        i.write(self.arquivoSaida+'.mseed',format=self.nome_formato.get())
                        
                    messagebox.showinfo('Geosis - Siscon','Conversão concluida')

                except:

                    messagebox.showerror('Geosis - Siscon','Formato inválido')

            else:

                pass
            
            for i in liststreams:
                
                del liststreams[:]
                
            self.frame.destroy()
            self.destroy()

        else:

            pass
        
    def cancelar(self):

        global liststreams

        for i in liststreams:
                
            del liststreams[:]

        self.frame.destroy()
        self.destroy()

    def select1(self):

        self.select = True
        self.nome_formato.set(self.formatos[0])
        
    def select2(self):

        self.select = True
        self.nome_formato.set(self.formatos[1])
                
run = Launcher()
run.mainloop()