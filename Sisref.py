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
from scipy import stats,arange
import sys
import ast
import warnings
import platform
from scipy.interpolate import spline

warnings.filterwarnings('ignore') 

class Sisref(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)
        self.grid(row = 0, column = 0, sticky = NSEW)
        self.winConfig()
        self.menus()
        self.icons()
        self.buttons()
        self.statusBar()
        self.memory()
        self.mplConfig()

    def winConfig(self):
        
        self.configure(background='#F3F3F3')
        root.title('Geosis - Sisref')
        
        if platform.system() == 'Windows':

            root.wm_state('zoomed')

            try:

                root.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

            except:

                pass

        else:
            
            root.attributes('-zoomed',True)

        if platform.system() == 'Windows':
        
            self.valorFigx = root.winfo_screenwidth()/160

            if root.winfo_screenheight() == 1080:
                
                self.valorFigy = root.winfo_screenheight()/93.1

            elif root.winfo_screenheight() == 768:

                self.valorFigy = root.winfo_screenheight()/100.5

            elif root.winfo_screenheight() == 1024:

                self.valorFigy = root.winfo_screenheight()/94.1

            elif root.winfo_screenheight() == 900:

                self.valorFigy = root.winfo_screenheight()/96.5

            elif root.winfo_screenheight() == 720:

                self.valorFigy = root.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = root.winfo_screenheight()/99

        elif platform.system() == 'Linux':

            self.valorFigx = root.winfo_screenwidth()/168

            if root.winfo_screenheight() == 1080:
                
                self.valorFigy = root.winfo_screenheight()/93.1

            elif root.winfo_screenheight() == 768:

                self.valorFigy = root.winfo_screenheight()/96

            elif root.winfo_screenheight() == 1024:

                self.valorFigy = root.winfo_screenheight()/94.1

            elif root.winfo_screenheight() == 900:

                self.valorFigy = root.winfo_screenheight()/96.5

            elif root.winfo_screenheight() == 720:

                self.valorFigy = root.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = root.winfo_screenheight()/99

        root.bind('<Control-a>', lambda x: self.abrirgp())
        root.bind('<Control-A>', lambda x: self.abrirgp())
        root.protocol("WM_DELETE_WINDOW", self.fechar)
        self.slave_frame = Frame(root)
        self.slave_frame.grid(row=1, column=0, sticky = NSEW)
        self.slave_frame2 = Frame(root)
        self.slave_frame2.grid(row = 1, column = 1)
        #self.navFrame = Frame(self,bg='#F3F3F3')
        #self.navFrame.pack(fill = BOTH, expand = True)

    def menus(self):
        
        menuBar = Menu(root)
        fileMenu=Menu(menuBar)
        menuBar.add_cascade(label='Arquivo',menu=fileMenu)
        fileMenu.add_command(label='Abrir arquivo tempo de percurso (.gp)                    Ctrl+A',
                                      command=self.abrirgp)
        curveMenu=Menu(menuBar)
        menuBar.add_cascade(label='Curvas',menu=curveMenu)
        curveMenu.add_command(label='Editar curvas                    Ctrl+E',
                                      command=self.editarCurva)
        inversionMenu=Menu(menuBar)
        menuBar.add_cascade(label='Inversão',menu=inversionMenu)
        inversionMenu.add_command(label='Atribuir camada 2                    Ctrl+E',
                                      command=self.camadas)
        inversionMenu.add_command(label='Atribuir camada 3                    Ctrl+E',
                                      command=self.camadas)
        inversionMenu.add_command(label='Calcular velocidades                    Ctrl+E',
                                      command=self.velocidades)
        root.config(menu=menuBar)

    def icons(self):

        self.openIcon = PhotoImage(file="%s/imagens/abrir.gif"%os.getcwd())
        self.saveIcon = PhotoImage(file="%s/imagens/salvar.gif"%os.getcwd())
        self.editIcon = PhotoImage(file="%s/imagens/edit.gif"%os.getcwd())
        self.layersIcon = PhotoImage(file="%s/imagens/camadas.gif"%os.getcwd())
        self.velocityIcon = PhotoImage(file="%s/imagens/vel.gif"%os.getcwd())
        self.inversionIcon = PhotoImage(file="%s/imagens/inv.gif"%os.getcwd())

    def buttons(self):

        openButton = Button(self, command = self.abrirgp)
        openButton.config(image=self.openIcon)
        openButton.grid(row=0,column=0,sticky=W)
        saveButton = Button(self, command = self.abrirgp)
        saveButton.config(image=self.saveIcon)
        saveButton.grid(row=0,column=1,sticky=W)
        editButton = Button(self, command = self.editarCurva)
        editButton.config(image=self.editIcon)
        editButton.grid(row=0,column=2,sticky=W)
        layersButton = Button(self, command = self.camadas)
        layersButton.config(image=self.layersIcon)
        layersButton.grid(row=0,column=3,sticky=W)
        VA = Button(self, command = self.pickVA)
        VA.config(image=self.velocityIcon)
        VA.grid(row=0,column=4,sticky=W)
        inv = Button(self, command = self.velocidades)
        inv.config(image=self.inversionIcon)
        inv.grid(row=0,column=5,sticky=W)

    def statusBar(self):
        
        self.status = Label(self,text = '', fg='green',font=("Helvetica", 12))
        self.status.grid(row=0,column=6,sticky=E)
        #self.frame = Frame(root,bg='#F3F3F3')
        #self.frame.pack()
        #self.frame.grid(row=1, column=0,sticky='nsew')

    def memory(self):

        self.xData, self.yData, self.fontes, self.bolas, self.camadas, self.xDataCamada1, self.yDataCamada1, \
        self.xDataCamada2,self.yDataCamada2,self.sublinhas, self.especiais, self.cores = {},{},{},{},{},{},{}, \
        {},{},{},{},{}
        self.linhas, self.temp, self.coordx, self.coordy, self.linhasVel, self.textosVel, self.conexoes = [],[],\
        [],[],[],[],[]                                                                                               
        self.dCamada1, self.curvaExiste, self.GCamada1,self.dCamada2,self.GCamada2, self.linha, self.cor, self.artista, self.linhaVel, \
        self.clickOn, self.pickVelOn = None, False, None, None, None, None, None, None, None, False, False
        self.nlinhas = 0
        self.count = 1
        self.count2 = 0
        self.sublinha = 0

    def mplConfig(self):
        
        plt.rcParams['keymap.zoom'] = 'z,Z'
        plt.rcParams['keymap.back'] = 'v,V'
        plt.rcParams['keymap.home'] = 'ctrl+z,ctrl+Z'
        plt.rcParams['keymap.save'] = 'ctrl+i,ctrl+I'
        plt.rcParams['keymap.pan'] = 'm,M'

    def fechar(self):

        if messagebox.askyesno("Geosis - sisref", "Sair do programa?"):

            self.destroy()
            root.destroy()
            sys.exit()

    def abrirgp(self):

        if self.curvaExiste == True:

            messagebox.showinfo('','Feche a curva atual antes de abrir uma nova')

        else:

            try:

                arquivo = filedialog.askopenfilename(title='Abrir',filetypes=[('Geosis pick','*.gp'),
                                                                    ('Todos os arquivos','*.*')])
            except:

                pass

            if len(arquivo) > 0:
            
                dados = open(arquivo).readlines()
                
                linhas = [i.strip('\n') for i in dados]

                for i in linhas:

                    if i.split()[0] != '/':

                        self.temp.append(float(i.split()[0]))

                    else:
                        
                        self.nlinhas += 1
                        self.fontes.update({self.nlinhas:float(i.split()[1])})
                        
                        if self.temp[0] < float(i.split()[1]) and self.temp[-1] > float(i.split()[1]):

                            self.especiais[self.nlinhas] = float(i.split()[1])
                            del self.temp[:]

                        else:

                            del self.temp[:]
                            
                for i in range(self.nlinhas):

                    if i+1 in self.especiais:

                        self.xData[i+1] = []
                        self.yData[i+1] = []
                        self.xDataCamada1[i+1] = {}
                        self.yDataCamada1[i+1] = {}
                        self.xDataCamada2[i+1] = {}
                        self.yDataCamada2[i+1] = {}

                        for j in range(2):

                            self.xDataCamada1[i+1][j+1] = []
                            self.yDataCamada1[i+1][j+1] = []
                            self.xDataCamada2[i+1][j+1] = []
                            self.yDataCamada2[i+1][j+1] = []
                            
                    else:
                        
                        self.xData[i+1] = []
                        self.yData[i+1] = []
                        self.xDataCamada1[i+1] = []
                        self.yDataCamada1[i+1] = []
                        self.xDataCamada2[i+1] = []
                        self.yDataCamada2[i+1] = []

                for i in linhas:

                    if i.split()[0] != '/':                       

                        self.xData[self.count].append(float(i.split()[0]))
                        self.yData[self.count].append(float(i.split()[1]))

                    else:

                        self.count += 1

                self.fig = plt.figure(figsize=(self.valorFigx,self.valorFigy),facecolor='#F3F3F3')
                self.ax = self.fig.add_subplot(111)
                
                for i in range(self.nlinhas):

                    linha, = self.ax.plot(self.xData[i+1],self.yData[i+1], picker = 0, color='black')
                    self.linhas.append(linha,)
                    self.ax.scatter(float(self.fontes[i+1]),0,s=80,alpha=1,marker=(5,1),color='#E5C100')
                    self.bolas[i+1] = []
                       
                    if i+1 in self.especiais:
                        
                        for j in self.xData[i+1]:

                            if float(j) < self.fontes[i+1]:

                                bola = self.ax.scatter(j, self.yData[i+1][self.xData[i+1].index(j)], s=30,c = 'white', alpha=1, picker = 5)
                                self.bolas[i+1].append(bola)
                                self.camadas[bola] = 1
                                self.sublinhas[bola] = 1
                                self.cores[bola] = 'white'

                            else:

                                bola = self.ax.scatter(j, self.yData[i+1][self.xData[i+1].index(j)], s=30,c = 'white', alpha=1, picker = 5)
                                self.bolas[i+1].append(bola)
                                self.camadas[bola] = 1
                                self.sublinhas[bola] = 2
                                self.cores[bola] = 'white'
                        #
                    else:
                        
                        for j,k in zip(self.xData[i+1],self.yData[i+1]):
                            
                            bola = self.ax.scatter(j, k, s=30,c = 'white', alpha=1, picker = 5)
                            self.bolas[i+1].append(bola)
                            self.camadas[bola] = 1
                            self.cores[bola] = 'white'

                plt.title('Curva de tempo de percurso')     
                plt.xlabel('Distância (m)')
                plt.ylabel('Tempo (ms)')
                plt.grid()
                self.ax.xaxis.grid(linestyle='-', linewidth=.4)
                self.ax.yaxis.grid(linestyle='-', linewidth=.4)
                self.tela = FigureCanvasTkAgg(self.fig, self.slave_frame)
                self.tela.show()
                self.tela.get_tk_widget().pack(fill='both', expand=True)
                toolbar = NavigationToolbar2TkAgg(self.tela, self.slave_frame)
                toolbar.update()
                self.tela._tkcanvas.pack(fill='both', expand=True)

                def do(event):
                        
                    key_press_handler(event, self.tela, toolbar)
                    
                self.fig.canvas.mpl_connect('key_press_event', do)
                self.curvaExiste = True
                self.apertado = False
                self.editorOn = False
                self.layerPick = False
                self.status.configure(text = ' Editor de traços: Off   Editor de camadas: Off')
                    
    def pickVA(self):

        def clicar(event):

            #try:

            self.coordx.append(event.xdata)
            self.coordy.append(event.ydata)
            self.linhaVel, = self.ax.plot(self.coordx,self.coordy,color='blue')
            self.linhasVel.append(self.linhaVel,)
            self.clickOn = True

            #except:

             #   pass

        def movimento(event):

            if self.clickOn == True:
                #try:

                self.coordx.append(event.xdata)
                self.coordy.append(event.ydata)
                self.linhaVel.set_data(self.coordx,self.coordy)
                self.fig.canvas.draw()
                del self.coordx[1:-1]
                del self.coordy[1:-1]

               # except:

                 #   pass

        def soltar(event):

            #try:

            self.coordx.append(event.xdata)
            self.coordy.append(event.ydata)
            self.linhaVel.set_data(self.coordx,self.coordy)
            #slope, intercept, r_value, p_value, std_err = stats.linregress(self.coordx,self.coordy)
            m, b, r_value, p_value, std_err = stats.linregress([int(i) for i in self.coordx],
                                                            self.coordy)
            #m,b = np.polyfit(self.coordx, self.coordy, 1)
            ltex = self.ax.text(self.coordx[0],self.coordy[0], '%.2f m/s'%(abs(1/m)*1000),
                        size=12, rotation=0, color = 'blue', ha="center", va="center",bbox = dict(ec='1',fc='1'))
            self.textosVel.append(ltex)
            self.fig.canvas.draw()
            del self.coordx[:]
            del self.coordy[:]
            self.clickOn = False

           # except:

              #  pass

        if self.pickVelOn == False:

            con1 = self.fig.canvas.mpl_connect('motion_notify_event', movimento)
            con2 = self.fig.canvas.mpl_connect('button_release_event', soltar)
            con3 = self.fig.canvas.mpl_connect('button_press_event', clicar)
            self.conexoes.append(con1)
            self.conexoes.append(con2)
            self.conexoes.append(con3)
            self.pickVelOn = True

        else:

            self.pickVelOn = False

            for i in self.conexoes:
                
                self.fig.canvas.mpl_disconnect(i)

            del self.conexoes[:]

            for j,k in zip(self.linhasVel,self.textosVel):
                
                j.remove()
                k.remove()
                    
            self.fig.canvas.draw()
            del self.linhasVel[:]
            del self.textosVel[:]
    
    def onoffcheck(self):

        if self.editorOn == True and self.layerPick == True:
                    
            self.status.configure(text = ' Editor de traços: On   Editor de camadas: On')
                    
        elif self.editorOn == True and self.layerPick == False:
            
            self.status.configure(text = ' Editor de traços: On   Editor de camadas: Off')

        elif self.editorOn == False and self.layerPick == True:
            
            self.status.configure(text = ' Editor de traços: Off   Editor de camadas: On')

        else:

            self.status.configure(text = ' Editor de traços: Off   Editor de camadas: Off')

    def editarCurva(self):

        if self.curvaExiste == True:

            if self.editorOn == True:

                self.fig.canvas.mpl_disconnect(self.conexao1)
                self.fig.canvas.mpl_disconnect(self.conexao2)
                self.editorOn = False
                self.onoffcheck()
                
            else:
                    
                def click(event):

                    for i in range(self.nlinhas):

                        if event.artist in self.bolas[i+1]:

                            self.coordy = float(event.artist.get_offsets()[0][1])
                            self.coordx = float(event.artist.get_offsets()[0][0])
                            self.apertado = True
                            self.linha = i+1
                            self.artista = event.artist
                            break

                def soltar(event):

                    if self.apertado == True:

                        for j in self.xData[self.linha]:

                            if float(j) == self.coordx:
  
                                self.yData[self.linha][self.xData[self.linha].index(self.coordx)] = float(event.ydata)
                                self.bolas[self.linha][self.bolas[self.linha].index(self.artista)].remove()
                                bola = self.ax.scatter(self.coordx,float(event.ydata),
                                                       s=30,c = self.cores[self.artista], alpha=1, picker = 5)
                                self.bolas[self.linha][self.bolas[self.linha].index(self.artista)] = bola

                                for i in self.cores:

                                    if i == self.artista:
                                        
                                        self.cores[bola] = self.cores[i]
                                        del self.cores[i]
                                        break

                                self.linhas[self.linha-1].set_ydata(self.yData[self.linha])
                                self.tela.show()
                                self.apertado = False
                                break

                self.conexao1 = self.fig.canvas.mpl_connect('pick_event', click)
                self.conexao2 = self.fig.canvas.mpl_connect('button_release_event', soltar)
                self.editorOn = True
                self.onoffcheck()

    def camadas(self):

        if self.curvaExiste == True:
        
            if self.layerPick == True:

                self.fig.canvas.mpl_disconnect(self.conexao3)
                self.layerPick = False
                self.onoffcheck()

            else:

                for i in range(self.nlinhas):
                    
                    for j in self.bolas[i+1]:

                        if self.cores[j] == 'white':

                            j.set_color('red')

                        if i+1 in self.especiais:

                            if float(j.get_offsets()[0][0]) < float(self.especiais[i+1]):

                                self.xDataCamada1[i+1][1].append(float(j.get_offsets()[0][0]))
                                self.yDataCamada1[i+1][1].append(float(j.get_offsets()[0][1]))

                            else:

                                self.xDataCamada1[i+1][2].append(float(j.get_offsets()[0][0]))
                                self.yDataCamada1[i+1][2].append(float(j.get_offsets()[0][1]))

                        else:

                            self.xDataCamada1[i+1].append(float(j.get_offsets()[0][0]))
                            self.yDataCamada1[i+1].append(float(j.get_offsets()[0][1]))

                self.tela.show()

                def click2(event):

                    for i in range(self.nlinhas):

                        if event.artist in self.bolas[i+1]:

                            linha = i+1
                    
                    if linha in self.especiais:

                        if event.artist in self.sublinhas:

                            self.sublinha = self.sublinhas[event.artist]

                        if self.sublinha == 1:

                            del self.xDataCamada1[linha][1][:]
                            del self.yDataCamada1[linha][1][:]
                            del self.xDataCamada2[linha][1][:]
                            del self.yDataCamada2[linha][1][:]

                        elif self.sublinha == 2:

                            del self.xDataCamada1[linha][2][:]
                            del self.yDataCamada1[linha][2][:]
                            del self.xDataCamada2[linha][2][:]
                            del self.yDataCamada2[linha][2][:]

                    else:

                        if len(self.xDataCamada1[linha]) > 0:
                            
                            del self.xDataCamada1[linha][:]
                            del self.yDataCamada1[linha][:]
                            del self.xDataCamada2[linha][:]
                            del self.yDataCamada2[linha][:]

                    if event.artist in self.bolas[linha]:

                        if linha in self.especiais:

                            if float(event.artist.get_offsets()[0][0]) < float(self.especiais[linha]):

                                for bola in self.bolas[linha]:

                                    if float(bola.get_offsets()[0][1]) >= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) < float(self.especiais[linha]):
                
                                        bola.set_color('#1BB270')
                                        self.camadas[event.artist] = 2
                                        self.xDataCamada2[linha][1].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada2[linha][1].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = '#1BB270'
                                                break

                                    elif float(bola.get_offsets()[0][1]) <= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) < float(self.especiais[linha]):

                                        bola.set_color('red')
                                        self.camadas[event.artist] = 1
                                        self.xDataCamada1[linha][1].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada1[linha][1].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = 'red'
                                                break
                                
                            elif float(event.artist.get_offsets()[0][0]) > float(self.especiais[linha]):
                                       
                                for bola in self.bolas[linha]:

                                    if float(bola.get_offsets()[0][1]) >= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) > float(self.especiais[linha]):

                                        bola.set_color('#1BB270')
                                        self.camadas[event.artist] = 2                                              
                                        self.xDataCamada2[linha][2].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada2[linha][2].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = '#1BB270'
                                                break
                                        
                                    elif float(bola.get_offsets()[0][1]) <= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) > float(self.especiais[linha]):

                                        bola.set_color('red')
                                        self.camadas[event.artist] = 1
                                        self.xDataCamada1[linha][2].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada1[linha][2].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = 'red'
                                                break
                                    
                        else:
                                   
                            for bola in self.bolas[linha]:

                                if self.fontes[linha] > float(event.artist.get_offsets()[0][0]):
                            
                                    if float(bola.get_offsets()[0][0]) <= float(event.artist.get_offsets()[0][0]):

                                        bola.set_color('#1BB270')
                                        self.camadas[event.artist] = 2
                                        self.xDataCamada2[linha].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada2[linha].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                                if i == bola:

                                                    self.cores[i] = '#1BB270'
                                                    break

                                    elif float(bola.get_offsets()[0][0]) > float(event.artist.get_offsets()[0][0]):

                                        bola.set_color('red')
                                        self.camadas[event.artist] = 1
                                        self.xDataCamada1[linha].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada1[linha].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                                if i == bola:

                                                    self.cores[i] = 'red'
                                                    break

                                else:

                                    if float(bola.get_offsets()[0][0]) >= float(event.artist.get_offsets()[0][0]):

                                        bola.set_color('#1BB270')
                                        self.camadas[event.artist] = 2
                                        self.xDataCamada2[linha].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada2[linha].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                                if i == bola:

                                                    self.cores[i] = '#1BB270'
                                                    break

                                    elif float(bola.get_offsets()[0][0]) < float(event.artist.get_offsets()[0][0]):

                                        bola.set_color('red')
                                        self.camadas[event.artist] = 1
                                        self.xDataCamada1[linha].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada1[linha].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                                if i == bola:

                                                    self.cores[i] = 'red'
                                                    break
                                                
                        self.tela.show()
                        
                self.conexao3 = self.fig.canvas.mpl_connect('pick_event', click2)
                self.layerPick = True
                self.onoffcheck()

    def velocidades(self):

        if self.curvaExiste == True:

            soma = 0
            soma2 = 0
            dadosd = []
            dadosG = []
            dadosd2 = []
            dadosG2 = []
            temp = []

            if type(self.xDataCamada1[1]) == dict:
                
                for i in self.xDataCamada1[1][1]:

                    temp.append(i)

                for i in self.xDataCamada1[1][2]:

                    temp.append(i)

                for i in self.xDataCamada2[1][1]:
                     
                    temp.append(i)

                for i in self.xDataCamada2[1][2]:
                     
                    temp.append(i)

            else:

                for i in self.xDataCamada1[1]:

                    temp.append(i)

                for i in self.xDataCamada2[1]:
                     
                    temp.append(i)
                

            for i in range(self.nlinhas):

                if type(self.yDataCamada1[i+1]) == dict:

                    soma += len(self.yDataCamada1[i+1][1])
                    soma += len(self.yDataCamada1[i+1][2])
                    soma2 += len(self.yDataCamada2[i+1][1])
                    soma2 += len(self.yDataCamada2[i+1][2])

                    for j in self.xDataCamada1[i+1][1]:

                        dadosG.append(abs(self.fontes[i+1]-j))

                    for j in self.xDataCamada1[i+1][2]:

                        dadosG.append(abs(self.fontes[i+1]-j))

                    for j in self.xDataCamada2[i+1][1]:

                        dadosG2.append(abs(self.fontes[i+1]-j))

                    for j in self.xDataCamada2[i+1][2]:

                        dadosG2.append(abs(self.fontes[i+1]-j))

                    for j in self.yDataCamada1[i+1][1]:

                        dadosd.append(j)

                    for j in self.yDataCamada1[i+1][2]:
                        
                        dadosd.append(j)

                    for j in self.yDataCamada2[i+1][1]:
                        
                        dadosd2.append(j)

                    for j in self.yDataCamada2[i+1][2]:
                        
                        dadosd2.append(j)
                    
                else:
                    
                    soma += len(self.yDataCamada1[i+1])
                    soma2 += len(self.yDataCamada2[i+1])
                
                    for j in self.xDataCamada1[i+1]:

                        dadosG.append(abs(self.fontes[i+1]-j))

                    for j in self.xDataCamada2[i+1]:

                        dadosG2.append(abs(self.fontes[i+1]-j))

                    for j in self.yDataCamada1[i+1]:
                        
                        dadosd.append(j)

                    for j in self.yDataCamada2[i+1]:
                        
                        dadosd2.append(j)

            self.dCamada1 = np.array(dadosd)
            self.GCamada1 = np.zeros((soma,1))

            for i in range(soma):

                self.GCamada1[i] = dadosG[i]

            self.dCamada2 = np.array(dadosd2)
            self.GCamada2 = np.zeros((soma2, len(self.fontes)+len(self.xData[1])+1))
            count = -1

            for i in range(self.nlinhas):

                if type(self.xDataCamada2[i+1]) != dict:
                
                    for j in range(len(self.xDataCamada2[i+1])):

                        count += 1
                        self.GCamada2[count][i] = 1
                        self.GCamada2[count][-1] = dadosG2[count]
                        self.GCamada2[count][temp.index(abs(dadosG2[count]-abs(self.fontes[i+1])))+len(self.fontes)] = 1

                else:

                    for j in range(len(self.xDataCamada2[i+1][1])):

                        count += 1
                        self.GCamada2[count][i] = 1
                        self.GCamada2[count][-1] = dadosG2[count]
                        self.GCamada2[count][temp.index(abs(dadosG2[count]-abs(self.fontes[i+1])))+len(self.fontes)] = 1

                    for j in range(len(self.xDataCamada2[i+1][2])):

                        count += 1
                        self.GCamada2[count][i] = 1
                        self.GCamada2[count][-1] = dadosG2[count]
                        self.GCamada2[count][temp.index(abs(dadosG2[count]+abs(self.fontes[i+1])))+len(self.fontes)] = 1

            count = 0
            smooth = np.zeros((len(self.fontes)+len(self.xData[1]),len(self.fontes)+len(self.xData[1])+1))

            for i in range(np.shape(smooth)[0]):

                smooth[i][i] = 0.01
                smooth[i][i+1] = -0.01
                    
            
            '''for i in range(len(self.fontes)+len(self.xData[1])):
                    
                smooth[count][count] = 0.01
                smooth[count][count+1] = -0.01
                count+=1'''
            
            smooth_G2 = np.concatenate((self.GCamada2,smooth))
            smooth_d2 =  np.hstack((self.dCamada2,[i*0 for i in range(len(self.fontes)+len(self.xData[1]))]))
                    
            m1 = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(self.GCamada1),self.GCamada1)),np.transpose(self.GCamada1)),self.dCamada1)
            m1 = np.linalg.lstsq(self.GCamada1, self.dCamada1)[0]
            #m2 = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(self.GCamada2),self.GCamada2)),np.transpose(self.GCamada2)),self.dCamada2)
            #m2 = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(smooth_G2),smooth_G2)),np.transpose(smooth_G2)),smooth_d2)
            m2 = np.linalg.lstsq(smooth_G2, smooth_d2)[0]
            
            #messagebox.showinfo('','Velocidades médias: camada 1 = %.2f km/s, camada 2 = %.2f km/s'%(1/m1[-1],1/m2[-1]))
            #xnew = np.linspace(0, 10, num=41, endpoint=True)

            fig2 = plt.figure(figsize=(self.valorFigx,self.valorFigy),facecolor='#F3F3F3')

            ax2 = fig2.add_subplot(111)

            x_smooth = np.linspace(np.array(temp).min(),np.array(temp).max(), 300)
            y_smooth = spline(np.array(temp),-1*(m2[len(self.fontes):-1]*(1/m1[-1])*(1/m2[-1]))/np.sqrt(((1/m2[-1])**2)-(1/m1[-1])**2), x_smooth)
            
            ax2.plot(x_smooth[0],x_smooth[-1], color = '#A85418', label = str(int(round(1/m1[-1]*1000)))+' m/s',linewidth = 3)
            l, = ax2.plot(x_smooth,y_smooth, label = str(int(round(1/m2[-1]*1000)))+' m/s', color = '#69340F', linewidth = 3)
            ax2.set_ylabel('Elevação (m)')
            ax2.set_xlabel('Distância (m)')
            ax2.set_xlim(temp[0],temp[-1])
            ax2.set_ylim(min(l.get_ydata())*3,10)
            ax2.fill_between(x_smooth, y_smooth, 0, color = '#A85418')
            ax2.fill_between(x_smooth, y_smooth, min(l.get_ydata())*2, color = '#69340F')
            #ax2.text(temp[int(len(temp)/2)], -1, '%.1f km/s'%(round(1/m1[-1],1)), fontsize=18)
            #ax2.text(temp[int(len(temp)/2)], min(l.get_ydata())-1, '%.1f km/s'%(round(1/m2[-1],1)), fontsize=18)
            ax2.grid()
            ax2.set_title(label='Modelo de velocidade')
            ax2.legend(loc='best')
            plt.gca().set_aspect('equal', adjustable='box')
            plt.draw()
            
            np.savetxt('time-terms.txt',m2,delimiter =' ', fmt='%.5f')

            with open('vels.txt', 'w') as arq:

                arq.write(str(round(1/m1[-1],5))+' ')
                arq.write(str(round(1/m2[-1],5)))
                arq.close()
            
            print(m2)
            print(1/m1[-1],1/m2[-1])
            np.savetxt('G2.txt',smooth_G2,delimiter =' ', fmt='%.1f')
            np.savetxt('d2.txt',smooth_d2,delimiter =' ', fmt='%.1f')
            np.savetxt('G1.txt',self.GCamada1,delimiter =' ', fmt='%.1f')
            np.savetxt('d1.txt',self.dCamada1,delimiter =' ', fmt='%.1f')

            tela2 = FigureCanvasTkAgg(fig2, self.slave_frame2)
            tela2.show()
            tela2.get_tk_widget().pack(fill='both', expand=True)
            toolbar2 = NavigationToolbar2TkAgg(tela2, self.slave_frame2)
            toolbar2.update()
            tela2._tkcanvas.pack(fill='both', expand=True)


root = Tk()
Sisref(root)
root.mainloop()
