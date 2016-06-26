from tkinter import *
from tkinter import filedialog, messagebox
import matplotlib
matplotlib.use('TkAgg')                                                                  
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.mlab as mlab
import scipy.stats as stats
import os                                                                              
import numpy as np
from scipy import stats,arange
import sys
import ast
import warnings
import platform
from scipy.interpolate import spline
import statistics as stat

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
        self.frame_curva = Frame(root)
        self.frame_curva.grid(row=1, column=0, sticky = NSEW)
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
        inversionMenu.add_separator()
        inversionMenu.add_command(label='Fazer inversão time-term automática                    Ctrl+E',
                                      command=self.invAuto)
        inversionMenu.add_command(label='Fazer inversão time-term manual                    Ctrl+E',
                                      command=self.invManual)
        viewMenu=Menu(menuBar)
        menuBar.add_cascade(label='Visualização',menu=viewMenu)
        viewMenu.add_command(label='Configurar eixos do modelo                    Ctrl+E',
                                      command=self.axisConfig)
        viewMenu.add_separator()
        viewMenu.add_command(label='Visualizar tiros no modelo                   Ctrl+E',
                                      command=self.showShots)
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
        inv = Button(self, command = self.invAuto)
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
        self.clickOn, self.pickVelOn, self.modeloExiste, self.showShots = None, False, None, None, None, None, None, None, None, False, False, False, False
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

                self.fig = plt.figure(figsize=(self.valorFigx-0.2,self.valorFigy),facecolor='#F3F3F3')
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
                self.tela = FigureCanvasTkAgg(self.fig, self.frame_curva)
                self.tela.show()
                self.tela.get_tk_widget().pack(fill='both', expand=True)
                toolbar = NavigationToolbar2TkAgg(self.tela, self.frame_curva)
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

    def showShots(self):

        if self.modeloExiste == True:

            if self.showShots == False:

                self.estrelas = []

                for fonte in self.fontes.values():

                    shot = self.ax_model.scatter(fonte,0,s=100,alpha=1,marker=(5,1),color='#E5C100')
                    self.estrelas.append(shot)

                self.fig_model.canvas.draw()
                self.showShots = True

            else:

                for i in self.estrelas:

                    i.remove()

                self.fig_model.canvas.draw()
                self.showShots = False
                

        else:

            messagebox.showinfo('Geosis - Sisref', 'Nennhum modelo plotado!')
            

    def axisConfig(self):

        if self.modeloExiste == True:

            axisWind = Tk()
            axisWind.title('Sisref - Configuração dos eixos do modelo')
            axisWind.geometry('200x240')
            axisWind.resizable(0,0)
            ymin_entry = StringVar()
            ymax_entry = StringVar()
            xmin_entry = StringVar()
            xmax_entry = StringVar()
            
            label_ymin = Label(axisWind, text = 'Y mínimo (m):',font=("Helvetica", 11),
                     fg='black').grid(row = 0, column = 0, sticky='w', padx = 10, pady = 10)
            entry_ymin = Entry(axisWind, textvariable = ymin_entry, width=10)
            entry_ymin.grid(row = 0, column = 0, sticky = 'w', padx = 115)
            label_ymax = Label(axisWind, text = 'Y máximo (m):',font=("Helvetica", 11),
                     fg='black').grid(row = 1, column = 0, sticky='w', padx = 10, pady = 10)
            entry_ymax = Entry(axisWind, textvariable = ymax_entry, width=10)
            entry_ymax.grid(row = 1, column = 0, sticky = 'w', padx = 115)
            label_xmin = Label(axisWind, text = 'X mínimo (m):',font=("Helvetica", 11),
                     fg='black').grid(row = 2, column = 0, sticky='w', padx = 10, pady = 10)
            entry_xmin = Entry(axisWind, textvariable = xmin_entry, width=10)
            entry_xmin.grid(row = 2, column = 0, sticky = 'w', padx = 115)
            label_xmax = Label(axisWind, text = 'X máximo (m):',font=("Helvetica", 11),
                     fg='black').grid(row = 3, column = 0, sticky='w', padx = 10, pady = 10)
            entry_xmax = Entry(axisWind, textvariable = xmax_entry, width=10)
            entry_xmax.grid(row = 3, column = 0, sticky = 'w', padx = 115)


            def definir ():

                if len(entry_ymax.get()) > 0:

                    if float(entry_ymax.get()) > self.ax_model.get_ylim()[0]:

                        self.ax_model.set_ylim(self.ax_model.get_ylim()[0],float(entry_ymax.get()))

                    else:

                        messagebox.showinfo('Geosis - Sisref', 'Verifique os valores de y!')

                if len(entry_ymin.get()) > 0:

                    if float(entry_ymin.get()) < self.ax_model.get_ylim()[1]:

                        self.ax_model.set_ylim(float(entry_ymin.get()),self.ax_model.get_ylim()[1])

                    else:

                        messagebox.showinfo('Geosis - Sisref', 'Verifique os valores de y!')

                if len(entry_xmin.get()) > 0:

                    if float(entry_xmin.get()) < self.ax_model.get_xlim()[1]:

                        self.ax_model.set_xlim(float(entry_xmin.get()),self.ax_model.get_xlim()[1])

                    else:

                        messagebox.showinfo('Geosis - Sisref', 'Verifique os valores de x!')

                if len(entry_xmax.get()) > 0:

                    if float(entry_xmax.get()) > self.ax_model.get_xlim()[0]:

                        self.ax_model.set_xlim(self.ax_model.get_xlim()[0],float(entry_xmax.get()))

                    else:

                        messagebox.showinfo('Geosis - Sisref', 'Verifique os valores de x!')
                
                self.fig_model.canvas.draw()
                

            def cancelar():

                axisWind.destroy()

            botaoDef = Button(axisWind, text = 'Ok',font=("Helvetica", 11), width = 6,
                        command = definir).grid(row = 4, column = 0, sticky = 'w', padx = 20, pady = 10)
            botaoFechar = Button(axisWind, text = 'Fechar',font=("Helvetica", 11), width = 6,
                command = cancelar).grid(row = 4, column = 0, sticky = 'w', padx = 100, pady = 10)

        else:

            messagebox.showinfo('Geosis - Sisref', 'Nennhum modelo plotado!')
        
                    
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

    def invManual(self):

        if self.curvaExiste == True:

            if self.modeloExiste == False:

                self.frame_model = Frame(root)
                self.frame_model.grid(row = 1, column = 1)

            else:

                self.frame_model.destroy()

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

                        try:
                            
                            count += 1
                            self.GCamada2[count][i] = 1
                            self.GCamada2[count][-1] = dadosG2[count]
                            self.GCamada2[count][temp.index(abs(dadosG2[count]-abs(self.fontes[i+1])))+len(self.fontes)] = 1

                        except:

                            pass

                else:

                    for j in range(len(self.xDataCamada2[i+1][1])):

                        try:

                            count += 1
                            self.GCamada2[count][i] = 1
                            self.GCamada2[count][-1] = dadosG2[count]
                            self.GCamada2[count][temp.index(abs(dadosG2[count]-abs(self.fontes[i+1])))+len(self.fontes)] = 1

                        except:

                            pass

                    for j in range(len(self.xDataCamada2[i+1][2])):

                        try:

                            count += 1
                            self.GCamada2[count][i] = 1
                            self.GCamada2[count][-1] = dadosG2[count]
                            self.GCamada2[count][temp.index(abs(dadosG2[count]+abs(self.fontes[i+1])))+len(self.fontes)] = 1

                        except:
                            pass

            residuals = {}
            mls = {}
            inversao = True
            solucoes = []
            solucoesid = {}
            fator = 0.1
            count = 1
            casas = 2
            
            while inversao == True:

                teste = False

                smooth = np.zeros((len(self.fontes)+len(self.xData[1]),len(self.fontes)+len(self.xData[1])+1))

                for i in range(np.shape(smooth)[0]):

                    smooth[i][i] = round(fator/count,casas)
                    smooth[i][i+1] = -1*round(fator/count,casas)
                    
                smooth_G2 = np.concatenate((self.GCamada2,smooth))
                smooth_d2 = np.hstack((self.dCamada2,[i*0 for i in range(len(self.fontes)+len(self.xData[1]))]))
                m = np.linalg.lstsq(smooth_G2, smooth_d2)
                solucoes.append(m[0])

                for i in m[0]: #teste de positividade

                    if i < 0:

                        teste = True

                if teste == False and len(m[1]) > 0: #se a solução for positiva e resíduo existir
                
                    residuals.update({float(m[1]):m[0]}) # residuo, solução
                    mls.update({float(m[1]):fator/count}) #resíduo, lagrange
                    solucoesid.update({fator/count:m[0]}) #lagrange, solução
                
                if round(fator/count,casas) == 9.9*10**-8:

                    inversao = False
                    break
                
                if round(fator/count,casas) == round(fator*10**-7,8) or casas == 9:

                    fator += 0.01
                    count = 1
                    casas = 2
                    
                else:
                 
                    count = count*10
                    casas += 1
            
            best_fits = {}
            
            selectWind = Tk()
            selectWind.title('Sisref - Seletor de solução')
            
            fig_gauss = plt.figure(figsize=(self.valorFigx-0.2,self.valorFigy+0.5),facecolor='#F3F3F3')
            ax_gauss = fig_gauss.add_subplot(111)
            R = []
            bolas_gauss = []

            for i in sorted(zip(mls.values(),mls.keys())):

                R.append(i[1])

            norm_dist = stats.norm.pdf(R, stat.mean(R), stat.stdev(R))
            l_gauss, = ax_gauss.plot(np.array(R), norm_dist, linewidth = 1.2, color = 'black', linestyle = '--')
            ax_gauss.fill_between(np.array(R), norm_dist, 0, facecolor = 'blue', alpha = .3)
            intervalo = stats.norm.interval(0.25, loc= stat.mean(R), scale= stat.stdev(R))

            for i in range(len(R)):
                
                b = ax_gauss.scatter(R[i], norm_dist[i], s = 15,edgecolor ='black',
                                     facecolor = 'blue', alpha = 0.4, picker = 5)
                bolas_gauss.append(b)
                best_fits.update({R[i]:residuals[R[i]]})
                
            ax_gauss.grid(True)
            ax_gauss.set_ylabel('Probabilidade (%)')
            ax_gauss.set_xlabel('Resíduos')
            ax_gauss.set_title(label='Distribuição gaussiana (%d/%d resíduos selecionados)'%(len(residuals),len(R)))
            p1 = plt.Rectangle((0, 0), 1, 1, fc="red", alpha = 0.3)
            p2 = plt.Rectangle((0, 0), 1, 1, fc="blue", alpha = 0.3)
            ax_gauss.legend([p1, p2], ['Não selecionados', 'Selecionados'])

            def click_gauss(event):

                if event.artist in bolas_gauss:

                    m = residuals[event.artist.get_offsets()[0][0]]
                    z = -1*(m[len(self.fontes):-1]*(1/m1[-1])*(1/m[-1]))/np.sqrt(((1/m[-1])**2)-(1/m1[-1])**2)

                    if event.artist.get_offsets()[0][0] in best_fits:

                        for linha in linhas_solus:

                            if sum(linha.get_ydata()) == sum(z):

                                linha.set_linestyle('--')
                                event.artist.set_color('blue')
                                del best_fits[event.artist.get_offsets()[0][0]]

                    else:

                        for linha in linhas_solus:

                            if sum(linha.get_ydata()) == sum(z):
                                        
                                linha.set_linestyle(':')
                                linha.set_linewidth(1)
                                event.artist.set_color('red')
                                best_fits.update({event.artist.get_offsets()[0][0]:m})

                    fig_solus.canvas.draw()
                    fig_gauss.canvas.draw()
                                
            def click_solus(event):

                if event.artist in linhas_solus:

                    z = event.artist.get_ydata()
                    residuo = None

                    for m in residuals.values():

                        if sum(-1*(m[len(self.fontes):-1]*(1/m1[-1])*(1/m[-1]))/np.sqrt(((1/m[-1])**2)-(1/m1[-1])**2)) == sum(z):

                            for r in residuals.keys():

                                if sum(residuals[r]) == sum(m):

                                    residuo = r

                    if residuo in best_fits.keys():

                        del best_fits[residuo]
                        event.artist.set_linestyle('--')
                        event.artist.set_linewidth(1)
                        
                        for bola in bolas_gauss:

                            if bola.get_offsets()[0][0] == residuo:

                                bola.set_color('blue')

                    else:

                        best_fits.update({residuo:residuals[residuo]})
                        
                        for bola in bolas_gauss:

                            if bola.get_offsets()[0][0] == residuo:

                                bola.set_color('red')

                        event.artist.set_linestyle(':')
        

                    fig_solus.canvas.draw()
                    fig_gauss.canvas.draw()


            def conIntervaloConf():

                IntervalWind = Tk()
                intervalo_entry = StringVar()
                IntervalWind.title('Sisref - Intervalo de confiança')
                IntervalWind.geometry('300x100')
                IntervalWind.resizable(0,0)
                labelIntervalo = Label(IntervalWind, text = 'Intervalo de confiança (%):',font=("Helvetica", 11),
                         fg='black').grid(row = 0, column = 0, sticky='w', padx = 10, pady = 10)
                entryIntervalo = Entry(IntervalWind, textvariable = intervalo_entry, width=10)
                entryIntervalo.grid(row = 0, column = 0, sticky = 'w', pady = 10, padx = 200)

                def cancelar():

                    IntervalWind.destroy()

                def definir():

                    if len(entryIntervalo.get()) > 0:

                        try:

                            intervalo = stats.norm.interval(1-(float(entryIntervalo.get())/100), loc= stat.mean(R), scale= stat.stdev(R))
                            ax_gauss.cla()
                            l_gauss, = ax_gauss.plot(np.array(R), norm_dist, linewidth = .5, color = 'black', linestyle = '--')
                            ax_gauss.fill_between(np.array(R), norm_dist, 0, facecolor = 'red', alpha = .3)
                            ax_gauss.fill_between(np.array(R), norm_dist, where = ((np.array(R)>= intervalo[0]) & (np.array(R) <= intervalo[1])),
                                                       facecolor = 'blue', alpha = .3)
                            p1 = plt.Rectangle((0, 0), 1, 1, fc="red", alpha = 0.3)
                            p2 = plt.Rectangle((0, 0), 1, 1, fc="blue", alpha = 0.3)
                            ax_gauss.legend([p1, p2], ['Não selecionados', 'Selecionados'])
                            best_fits.clear()
                            sum_best_fits = 0
                            ax_solus.cla()
                            espessuras = []
                            
                            for i in range(len(R)):
                                
                                b = ax_gauss.scatter(R[i], norm_dist[i], s = 15, edgecolor ='black',
                                                     facecolor = 'red', alpha = 0.4, picker = 5)

                                if b.get_offsets()[0][0] >= intervalo[0] and b.get_offsets()[0][0] <= intervalo[1]:

                                    b.set_color('blue')
                                    best_fits.update({b.get_offsets()[0][0]:residuals[b.get_offsets()[0][0]]})
                                    esp, = ax_solus.plot(np.array(temp),
                                         -1*(residuals[b.get_offsets()[0][0]][len(self.fontes):-1]*(1/m1[-1])*(1/residuals[b.get_offsets()[0][0]][-1]))/np.sqrt(((1/residuals[b.get_offsets()[0][0]][-1])**2)-(1/m1[-1])**2),
                                                   linewidth = 0.8, linestyle = '--')
                                    espessuras.append(min(esp.get_ydata()))
                                    sum_best_fits += residuals[b.get_offsets()[0][0]]
                                    
                            
                            ax_gauss.grid(True)
                            ax_gauss.set_ylabel('Probabilidade (%)')
                            ax_gauss.set_xlabel('Resíduos')
                            ax_gauss.set_title(label='Distribuição gaussiana (%d/%d resíduos selecionados)'%(len(best_fits.keys()),len(R)))
                            fig_gauss.canvas.draw()
                            
                            best_fit = sum_best_fits/len(best_fits.values())

                            ax_solus.plot(np.array(temp),
                                          -1*(best_fit[len(self.fontes):-1]*(1/m1[-1])*(1/best_fit[-1]))/np.sqrt(((1/best_fit[-1])**2)-(1/m1[-1])**2),
                                          color = '#94ff2e', linewidth = 2.5, linestyle ='-', label = 'Espessura média (seu modelo)')
                            ax_solus.legend(loc='best')

                            plt.gca().set_aspect('equal', adjustable='box')
                            plt.draw()
                            ax_solus.set_ylabel('Profundidade (m)')
                            ax_solus.set_xlabel('Distância (m)')
                            ax_solus.set_title(label='Espessuras de %d soluções'%len(best_fits))      
                            ax_solus.set_ylim(min(espessuras)-5,5)
                            fig_solus.canvas.draw()
                            IntervalWind.destroy()
                                
                            
                        except:

                            messagebox.showinfo('Geosis - Sisref', 'Intervalo inválido. Entre com um valor entre 0 e 100!')
                            
                botaoDef = Button(IntervalWind, text = 'Definir',font=("Helvetica", 11), width = 6,
                    command = definir).grid(row = 1, column = 0, sticky = 'w', padx = 10, pady = 10)
                botaoFechar = Button(IntervalWind, text = 'Cancelar',font=("Helvetica", 11), width = 6,
                    command = cancelar).grid(row = 1, column = 0, sticky = 'w', padx = 150, pady = 10)
            
            def velModel():

                if self.modeloExiste == False:

                    self.frame_model = Frame(root)
                    self.frame_model.grid(row = 1, column = 1)

                else:

                    self.frame_model.destroy()
                    self.frame_model = Frame(root)
                    self.frame_model.grid(row = 1, column = 1)
                    self.showShots = False

                sum_solus = 0
                len_solus = 0

                self.fig_model = plt.figure(figsize=(self.valorFigx-0.2,self.valorFigy+0.5),facecolor='#F3F3F3')
                self.ax_model = self.fig_model.add_subplot(111)

                for r in residuals.keys():

                    if r in best_fits.keys():

                        sum_solus += residuals[r]
                        len_solus += 1

                media_solus = sum_solus/len_solus
                self.ax_model.plot(np.array(temp)[0],np.array(temp)[-1], color = '#5bdaff', label = str(int(round(1/m1[-1]*1000)))+' m/s',linewidth = 3)
                l_model,= self.ax_model.plot(np.array(temp),-1*(media_solus[len(self.fontes):-1]*(1/m1[-1])*(1/media_solus[-1]))/np.sqrt(((1/media_solus[-1])**2)-(1/m1[-1])**2),
                                          color = '#94ff2e',label = str(int(round(1/media_solus[-1]*1000)))+' m/s',linewidth = 3)
                self.ax_model.set_ylabel('Elevação (m)')
                self.ax_model.set_xlabel('Distância (m)')
                self.ax_model.set_xlim(np.array(temp)[0],np.array(temp)[-1])
                self.ax_model.set_ylim(min(l_model.get_ydata())-5,5)
                plt.gca().set_aspect('equal', adjustable='box')
                plt.draw()
                self.ax_model.fill_between(np.array(temp),-1*(media_solus[len(self.fontes):-1]*(1/m1[-1])*(1/media_solus[-1]))/np.sqrt(((1/media_solus[-1])**2)-(1/m1[-1])**2),
                                      0, color = '#5bdaff')
                self.ax_model.fill_between(np.array(temp),-1*(media_solus[len(self.fontes):-1]*(1/m1[-1])*(1/media_solus[-1]))/np.sqrt(((1/media_solus[-1])**2)-(1/m1[-1])**2),
                                      min(l_model.get_ydata())*2, color = '#94ff2e')
                self.ax_model.grid()
                self.ax_model.set_title(label='Modelo de velocidade')
                self.ax_model.legend(loc='best')

                tela_model = FigureCanvasTkAgg(self.fig_model, self.frame_model)
                tela_model.show()
                tela_model.get_tk_widget().pack(fill='both', expand=True)
                toolbar2 = NavigationToolbar2TkAgg(tela_model, self.frame_model)
                toolbar2.update()
                tela_model._tkcanvas.pack(fill='both', expand=True)
                self.modeloExiste = True
                selectWind.destroy()

            invSelected = Button(selectWind, command = velModel, text = 'Modelo de velocidade')
            invSelected.grid(row=0,column=0,sticky=W)
            defInter = Button(selectWind, command = conIntervaloConf, text = 'Intervalo de confiança')
            defInter.grid(row=0,column=0,sticky=W, padx = 130)
            frame_gauss = Frame(selectWind)
            frame_gauss.grid(row=1, column=0, sticky = NSEW)
            frame_solus = Frame(selectWind)
            frame_solus.grid(row = 1, column = 1)

            tela_gauss = FigureCanvasTkAgg(fig_gauss, frame_gauss)
            tela_gauss.show()
            tela_gauss.get_tk_widget().pack(fill='both', expand=True)
            toolbar = NavigationToolbar2TkAgg(tela_gauss, frame_gauss)
            toolbar.update()
            tela_gauss._tkcanvas.pack(fill='both', expand=True)

            fig_solus = plt.figure(figsize=(self.valorFigx-0.2,self.valorFigy),facecolor='#F3F3F3')
            ax_solus = fig_solus.add_subplot(111)

            m1 = np.linalg.lstsq(self.GCamada1, self.dCamada1)[0]

            linhas_solus = []
            espessuras = []

            for sol in residuals.values():

                l_solu, = ax_solus.plot(np.array(temp),-1*(sol[len(self.fontes):-1]*(1/m1[-1])*(1/sol[-1]))/np.sqrt(((1/sol[-1])**2)-(1/m1[-1])**2),
                          linestyle = '--', linewidth = .8, picker = 5)
                linhas_solus.append(l_solu)
                espessuras.append(min(l_solu.get_ydata()))

            ax_solus.set_ylabel('Profundidade (m)')
            ax_solus.set_xlabel('Distância (m)')
            ax_solus.set_title(label = 'Espessuras referentes a %d soluções'%len(residuals))
            ax_solus.set_ylim(min(espessuras)-5,5)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.draw()

            tela_solus = FigureCanvasTkAgg(fig_solus, frame_solus)
            tela_solus.show()
            tela_solus.get_tk_widget().pack(fill='both', expand=True)
            toolbar22 = NavigationToolbar2TkAgg(tela_solus, frame_solus)
            toolbar.update()
            tela_solus._tkcanvas.pack(fill='both', expand=True)
            con_gauss = fig_gauss.canvas.mpl_connect('pick_event', click_gauss)
            con_solus = fig_solus.canvas.mpl_connect('pick_event', click_solus)
                            

    def invAuto(self):

        if self.curvaExiste == True:

            if self.modeloExiste == False:

                self.frame_model = Frame(root)
                self.frame_model.grid(row = 1, column = 1)

            else:

                self.frame_model.destroy()
                self.frame_model = Frame(root)
                self.frame_model.grid(row = 1, column = 1)
                self.showShots = False

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

                        try:

                            count += 1
                            self.GCamada2[count][i] = 1
                            self.GCamada2[count][-1] = dadosG2[count]
                            self.GCamada2[count][temp.index(abs(dadosG2[count]-abs(self.fontes[i+1])))+len(self.fontes)] = 1

                        except:

                            pass

                else:

                    for j in range(len(self.xDataCamada2[i+1][1])):

                        try:

                            count += 1
                            self.GCamada2[count][i] = 1
                            self.GCamada2[count][-1] = dadosG2[count]
                            self.GCamada2[count][temp.index(abs(dadosG2[count]-abs(self.fontes[i+1])))+len(self.fontes)] = 1

                        except:

                            pass

                    for j in range(len(self.xDataCamada2[i+1][2])):

                        try:

                            count += 1
                            self.GCamada2[count][i] = 1
                            self.GCamada2[count][-1] = dadosG2[count]
                            self.GCamada2[count][temp.index(abs(dadosG2[count]+abs(self.fontes[i+1])))+len(self.fontes)] = 1

                        except:

                            pass

            residuals = {}
            mls = {}
            inversao = True
            solucoes = []
            solucoesid = {}
            fator = 0.1
            count = 1
            casas = 2
            
            while inversao == True:

                teste = False

                smooth = np.zeros((len(self.fontes)+len(self.xData[1]),len(self.fontes)+len(self.xData[1])+1))

                for i in range(np.shape(smooth)[0]):

                    smooth[i][i] = round(fator/count,casas)
                    smooth[i][i+1] = -1*round(fator/count,casas)
                    
                smooth_G2 = np.concatenate((self.GCamada2,smooth))
                smooth_d2 = np.hstack((self.dCamada2,[i*0 for i in range(len(self.fontes)+len(self.xData[1]))]))
                m = np.linalg.lstsq(smooth_G2, smooth_d2)
                solucoes.append(m[0])

                for i in m[0]: #teste de positividade

                    if i < 0:

                        teste = True

                if teste == False and len(m[1]) > 0: #se a solução for positiva e resíduo existir
                
                    residuals.update({float(m[1]):m[0]}) # residuo, solução
                    mls.update({float(m[1]):fator/count}) #resíduo, lagrange
                    solucoesid.update({fator/count:m[0]}) #lagrange, solução
                
                if round(fator/count,casas) == 9.9*10**-8:

                    inversao = False
                    break
                
                if round(fator/count,casas) == round(fator*10**-7,8) or casas == 9:

                    fator += 0.01
                    count = 1
                    casas = 2
                    
                else:
                 
                    count = count*10
                    casas += 1
                    
            R = []

            for i in sorted(zip(mls.values(),mls.keys())):

                R.append(i[1])

            norm_dist = stats.norm.pdf(R, stat.mean(R), stat.stdev(R))
            intervalo = stats.norm.interval(0.25, loc= stat.mean(R), scale= stat.stdev(R))
            best_fits = []

            for i in R:

                if i >= intervalo[0] and i <= intervalo[1]:
                    
                    best_fits.append(residuals[i])
                                
            m1 = np.linalg.lstsq(self.GCamada1, self.dCamada1)[0]
            sum_best_fits = 0

            for i in best_fits:
                
                sum_best_fits += i
            
            best_fit = sum_best_fits/len(best_fits)

            #solução escolhida
            self.fig_model = plt.figure(figsize=(self.valorFigx-0.2,self.valorFigy),facecolor='#F3F3F3')
            self.ax_model = self.fig_model.add_subplot(111)   
            self.ax_model.plot(np.array(temp)[0],np.array(temp)[-1], color = '#5bdaff', label = str(int(round(1/m1[-1]*1000)))+' m/s',linewidth = 3)
            l_model, = self.ax_model.plot(np.array(temp),-1*(best_fit[len(self.fontes):-1]*(1/m1[-1])*(1/best_fit[-1]))/np.sqrt(((1/best_fit[-1])**2)-(1/m1[-1])**2),
                          label = str(int(round(1/best_fit[-1]*1000)))+' m/s', color = '#94ff2e', linewidth = 3)
            self.ax_model.set_ylabel('Elevação (m)')
            self.ax_model.set_xlabel('Distância (m)')
            self.ax_model.set_xlim(np.array(temp)[0],np.array(temp)[-1])
            self.ax_model.set_ylim(min(l_model.get_ydata())-5,5)
            self.ax_model.fill_between(np.array(temp),-1*(best_fit[len(self.fontes):-1]*(1/m1[-1])*(1/best_fit[-1]))/np.sqrt(((1/best_fit[-1])**2)-(1/m1[-1])**2),
                                  0, color = '#5bdaff')
            self.ax_model.fill_between(np.array(temp),-1*(best_fit[len(self.fontes):-1]*(1/m1[-1])*(1/best_fit[-1]))/np.sqrt(((1/best_fit[-1])**2)-(1/m1[-1])**2),
                                  min(l_model.get_ydata())*2, color = '#94ff2e')
            self.ax_model.grid()
            self.ax_model.set_title(label='Modelo de velocidade')
            self.ax_model.legend(loc='best')
            plt.gca().set_aspect('equal', adjustable='box')
            plt.draw()

            tela2 = FigureCanvasTkAgg(self.fig_model, self.frame_model)
            tela2.show()
            tela2.get_tk_widget().pack(fill='both', expand=True)
            toolbar2 = NavigationToolbar2TkAgg(tela2, self.frame_model)
            toolbar2.update()
            tela2._tkcanvas.pack(fill='both', expand=True)
            self.modeloExiste = True
        ###
            if messagebox.askyesno("Geosis - Sisref", "Visualizar a seleção de soluções?"):

                selectWind_auto = Tk()
                selectWind_auto.title('Sisref - Seleção de soluções')
                frame_gauss_auto = Frame(selectWind_auto)
                frame_gauss_auto.grid(row=1, column=0, sticky = NSEW)
                frame_solus_auto = Frame(selectWind_auto)
                frame_solus_auto.grid(row = 1, column = 1)
                
                fig_solus_auto = plt.figure(figsize=(self.valorFigx-0.2,self.valorFigy+0.5),facecolor='#F3F3F3')
                ax_solus_auto = fig_solus_auto.add_subplot(111)

                espessuras = []
                
                for m in best_fits:

                    esp, = ax_solus_auto.plot(np.array(temp),
                             -1*(m[len(self.fontes):-1]*(1/m1[-1])*(1/m[-1]))/np.sqrt(((1/m[-1])**2)-(1/m1[-1])**2),
                                       linewidth = 0.8, linestyle = '--')
                    espessuras.append(min(esp.get_ydata()))

                ax_solus_auto.plot(np.array(temp),
                              -1*(best_fit[len(self.fontes):-1]*(1/m1[-1])*(1/best_fit[-1]))/np.sqrt(((1/best_fit[-1])**2)-(1/m1[-1])**2),
                              color = '#94ff2e', linewidth = 2.5, linestyle ='-', label = 'Espessura média (seu modelo)')
                ax_solus_auto.legend(loc='best')

                plt.gca().set_aspect('equal', adjustable='box')
                plt.draw()
                ax_solus_auto.set_ylabel('Profundidade (m)')
                ax_solus_auto.set_xlabel('Distância (m)')
                ax_solus_auto.set_title(label='Espessuras de %d soluções'%len(best_fits))      
                ax_solus_auto.set_ylim(min(espessuras)-5,5)
                
                tela_solus_auto = FigureCanvasTkAgg(fig_solus_auto, frame_solus_auto)
                tela_solus_auto.show()
                tela_solus_auto.get_tk_widget().pack(fill='both', expand=True)
                toolbar_solus_auto = NavigationToolbar2TkAgg(tela_solus_auto, frame_solus_auto)
                toolbar_solus_auto.update()
                tela_solus_auto._tkcanvas.pack(fill='both', expand=True)

                fig_gauss_auto = plt.figure(figsize=(self.valorFigx-0.2,self.valorFigy+0.5),facecolor='#F3F3F3')
                ax_gauss_auto = fig_gauss_auto.add_subplot(111)

                l_gauss, = ax_gauss_auto.plot(np.array(R), norm_dist, linewidth = .5, color = 'black', linestyle = '--')
                ax_gauss_auto.fill_between(np.array(R), norm_dist, 0, facecolor = 'red', alpha = .3)
                ax_gauss_auto.fill_between(np.array(R), norm_dist, where = ((np.array(R)>= intervalo[0]) & (np.array(R) <= intervalo[1])),
                                           facecolor = 'blue', alpha = .3)
                p1 = plt.Rectangle((0, 0), 1, 1, fc="red", alpha = 0.3)
                p2 = plt.Rectangle((0, 0), 1, 1, fc="blue", alpha = 0.3)
                ax_gauss_auto.legend([p1, p2], ['Não selecionados', 'Selecionados'])

                for i in range(len(R)):
                    
                    b = ax_gauss_auto.scatter(R[i], norm_dist[i], s = 15, edgecolor ='black',
                                         facecolor = 'red', alpha = 0.4, picker = 5)

                    if b.get_offsets()[0][0] >= intervalo[0] and b.get_offsets()[0][0] <= intervalo[1]:

                        b.set_color('blue')
                
                ax_gauss_auto.grid(True)
                ax_gauss_auto.set_ylabel('Probabilidade (%)')
                ax_gauss_auto.set_xlabel('Resíduos')
                ax_gauss_auto.set_title(label='Distribuição gaussiana (%d/%d resíduos selecionados)'%(len(best_fits),len(R)))

                tela_gauss_auto = FigureCanvasTkAgg(fig_gauss_auto, frame_gauss_auto)
                tela_gauss_auto.show()
                tela_gauss_auto.get_tk_widget().pack(fill='both', expand=True)
                toolbar_gauss_auto = NavigationToolbar2TkAgg(tela_gauss_auto, frame_gauss_auto)
                toolbar_gauss_auto.update()
                tela_gauss_auto._tkcanvas.pack(fill='both', expand=True)
        ###


root = Tk()
Sisref(root)
root.mainloop()
