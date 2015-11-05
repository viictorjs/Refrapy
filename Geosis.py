
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


class Launcher(Tk):
    
    def __init__(self):

        print('''

    GEOSIS v1.0
    
    AUTOR: VICTOR JOSÉ C. B. GUEDES
    E-MAIL: vjs279@hotmail.com
    
    GEOFÍSICA - UNIVERSIDADE DE BRASILIA

    *fechar esta janela encerrará o programa*

                                        ''')
        Tk.__init__(self)
        self.geometry('640x400')
        self.title('Geosis v1.0')
        parentLauncher = Frame(self)
        parentLauncher.grid(row=0,column=0,sticky='nsew')
        barraDEmenu = Menu(self)
        self.configure(menu=barraDEmenu)
        menu_modulos=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Módulos',menu=menu_modulos)
        menu_modulos.add_command(label='Sispick',
                                      command= self.chamarSispick)
        menu_modulos.add_command(label='Siscon',
                                      command= self.chamarSiscon)
        menu_ajuda = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Ajuda',menu=menu_ajuda)
        menu_ajuda.add_command(label='Sobre o software',command = self.Sobre)

        try:
            
            photo = PhotoImage(file="%s/imagens/unb_geof.gif"%os.getcwd())

            if platform.system() == 'Windows':
                
                self.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

        except:

            messagebox.showerror('',"Arquivos faltando na pasta 'imagens'")
            
        label = Label(parentLauncher,image=photo)
        label.image = photo
        label.grid(row=0,column=0,sticky='nsew')
        botaoSispick = Button(parentLauncher, text='sispick',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSispick).grid(row=0,column=0,sticky='w')   
        botaosiscon = Button(parentLauncher, text='siscon',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSiscon).grid(row=0,column=0,sticky='e')
        botaosisref = Button(parentLauncher, text='sisref',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarsisref).grid(row=0,column=0,padx=50)
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

    def fechar(self):

        if messagebox.askyesno("Geosis", "Fechar o launcher?"):
            
            self.destroy()

    def chamarsisref(self):

        self.destroy()
        run_sisref = sisref()

    def chamarSispick(self):

        self.destroy()
        run_sispick = Sispick()

    def chamarSiscon(self):

        self.destroy()
        run_siscon = Siscon()

    def Sobre(self):

        root = Tk()
        root.geometry('630x300')
        root.title('Info')
        titulo = Label(root, text='Sobre o software',fg='green',font=("Helvetica", 14))
        root.resizable(0,0)
        root.mainloop()
        

class Sispick(Tk):

    frames, figs, axes, telas, listSource, sts, ticksLabel, toolbars, dadosNorms, dadosCrus, \
    ganho, filtros,filtrosHP, filtrosLP, copiasCruas, copiasNorms, okpicks, clips, \
    sombreamentos, picks, picksArts, coordx, coordy, conPickClick, conPickMov, conPickSoltar, \
    conVelClick, conVelMov, conVelSoltar, conAmostra, ndados, linhasPick, freqLP, \
    freqHP = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[], \
    [],[],[],[],[],[],[],[]
    sublinhas, bolas, indicadores, plotArts, sombArts, coordsx, coordsy, linhasVel, \
    textoVel, tracosMax = {},{},{},{},{},{}, {}, {}, {}, {}
    plotExiste, pickMode, yinvertido, normalizado, optAberto, pickAmostraAtivado, clickOn, \
    pickVelOn = False,False,False,False,False,False,False,False
    arquivos, formato, posicaoGeof1, eventCon, pagina, recordlen, valordx, linhaVel, linhaPick, \
    valorFigx, valorFigy = None,None,None,None,None,None,None,None,None,None,None
    fatorY, valorGanho, fatorLP, fatorHP = 0.8, 2, 0.8, 1.5

    def __init__(self):                         

        Tk.__init__(self)                       
        self.configure(background='#F3F3F3')
        self.title('Geosis - Sispick')
        
        if platform.system() == 'Windows':

            self.wm_state('zoomed')

            try:

                self.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

            except:

                pass

        else:
            
            self.attributes('-zoomed',True)

        if platform.system() == 'Windows':
        
            self.valorFigx = self.winfo_screenwidth()/80

            if self.winfo_screenheight() == 1080:
                
                self.valorFigy = self.winfo_screenheight()/93.1

            elif self.winfo_screenheight() == 768:

                self.valorFigy = self.winfo_screenheight()/100.5

            elif self.winfo_screenheight() == 1024:

                self.valorFigy = self.winfo_screenheight()/94.1

            elif self.winfo_screenheight() == 900:

                self.valorFigy = self.winfo_screenheight()/96.5

            elif self.winfo_screenheight() == 720:

                self.valorFigy = self.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = self.winfo_screenheight()/99

        elif platform.system() == 'Linux':

            self.valorFigx = self.winfo_screenwidth()/83

            if self.winfo_screenheight() == 1080:
                
                self.valorFigy = self.winfo_screenheight()/93.1

            elif self.winfo_screenheight() == 768:

                self.valorFigy = self.winfo_screenheight()/96

            elif self.winfo_screenheight() == 1024:

                self.valorFigy = self.winfo_screenheight()/94.1

            elif self.winfo_screenheight() == 900:

                self.valorFigy = self.winfo_screenheight()/96.5

            elif self.winfo_screenheight() == 720:

                self.valorFigy = self.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = self.winfo_screenheight()/99
        
        self.parent = Frame(self,bg='#F3F3F3')
        self.parent.grid(row=0,column=0,sticky='nsew')
        barraDEmenu = Menu(self)
        self.configure(menu=barraDEmenu)
        menu_arquivo=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Arquivo',menu=menu_arquivo)
        menu_arquivo.add_command(label='Abrir                    Ctrl+A',
                                      command=self.abrir_pt1)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label='Salvar pick Seisimager (.vs)           Ctrl+S',
                                      command=self.salvarpick)
        menu_arquivo.add_command(label='Salvar pick Geosis (.gp)           Ctrl+S',
                                      command=self.salvargp)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label='Sair                         Alt+S',
                                      command=self.destroy)
        menu_visualizar = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Visualizaçao',menu=menu_visualizar)
        menu_visualizar.add_command(label='Proximo                Direita',
                                         command=self.nextpage)
        menu_visualizar.add_command(label='Anterior                Esquerda',
                                         command=self.backpage)
        menu_visualizar.add_separator()
        menu_visualizar.add_command(label='Inverter eixo y       I',
                                         command=self.backpage)
        menu_visualizar.add_separator()
        menu_visualizar.add_command(label='Diminuir eixo y      Baixo',
                                         command=self.menosy)
        menu_visualizar.add_command(label='Aumentar eixo y    Cima',
                                         command=self.maisy)
        menu_tracos = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Traços',menu=menu_tracos)
        menu_tracos.add_command(label='Dar ganho                                 Shift + Direita',
                                     command=self.ampup)
        menu_tracos.add_command(label='Retirar ganho                            Shift + Esquerda',
                                     command=self.ampdown)
        menu_tracos.add_separator()
        menu_tracos.add_command(label='Aplicar/Retirar normalizaçao       N',
                                     command=self.normalizar)
        menu_tracos.add_separator()
        menu_tracos.add_command(label='Sombrear amplitudes negativas    Alt + Direita',
                                     command=self.sombNeg)
        menu_tracos.add_command(label='Sombrear amplitudes positivas    Alt + Esquerda',
                                     command=self.sombPos)
        menu_tracos.add_command(label='Retirar sombreamento    Alt + Baixo',
                                     command=self.sombNull)
        menu_tracos.add_separator()
        menu_tracos.add_command(label='Clipar         C',
                                     command=self.clip)
        menu_editar = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Editar',menu=menu_editar)
        menu_editar.add_command(label='Ativar/Desativar pick                  P',
                                     command=self.ativarPick)
        menu_editar.add_command(label='Limpar plot                                Ctrl + L',
                                     command=self.limparplot)
        menu_editar.add_separator()
        menu_editar.add_command(label='Cortar amostras      A',
                                 command=self.pickAmostra)
        menu_editar.add_command(label='Restaurar amostras originais      Alt + A',
                                         command=self.amostrasDefault)
        menu_editar.add_separator()
        menu_editar.add_command(label='Criar/Remover ligaçao entre picks      L',
                                         command=self.removerLinhaPicks)
        menu_editar.add_separator()
        menu_editar.add_command(label='Visualizar curva de tempo de percurso      Ctrl + G',
                                         command=self.verCurva)
        menu_editar.add_separator()
        menu_editar.add_command(label='Fechar seçao atual                     Ctrl+X',
                                     command=self.fecharPlot)
        menu_filtros = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Filtros',menu=menu_filtros)
        menu_filtros.add_command(label='Passa baixa          Ctrl+O',command=self.filtroLP)
        menu_filtros.add_command(label='Passa alta          Ctrl+O',command=self.filtroHP)
        menu_filtros.add_separator()
        menu_filtros.add_command(label='Remover filtros          Ctrl+O',command=self.removerFiltros)
        menu_opcoes = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Opçoes',menu=menu_opcoes)
        menu_opcoes.add_command(label='Opções de plot          Ctrl+O',command=self.configPlot)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label='Editar cabeçalho          Ctrl+H',command = self.cabecalho)
        menu_ajuda = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Ajuda',menu=menu_ajuda)
        menu_ajuda.add_command(label='Atalhos de teclado',command = lambda: print(''))
        Abrir = Button(self.parent, command = self.abrir_pt1)
        img_abrir = PhotoImage(file="%s/imagens/abrir.gif"%os.getcwd())
        Abrir.config(image=img_abrir)
        Abrir.grid(row=0,column=0,sticky=W)
        Salvar = Button(self.parent, command = self.salvargp)
        img_salvar = PhotoImage(file="%s/imagens/salvar.gif"%os.getcwd())
        Salvar.config(image=img_salvar)
        Salvar.grid(row=0,column=1,sticky=W)
        Back = Button(self.parent, command = self.backpage)
        img_voltar = PhotoImage(file="%s/imagens/voltar.gif"%os.getcwd())
        Back.config(image=img_voltar)
        Back.grid(row=0,column=2,sticky=W)
        Next = Button(self.parent, command = self.nextpage)
        img_proximo = PhotoImage(file="%s/imagens/proximo.gif"%os.getcwd())
        Next.config(image=img_proximo)
        Next.grid(row=0,column=3,sticky=W)
        menosY = Button(self.parent, command = self.menosy)
        img_baixo = PhotoImage(file="%s/imagens/baixo.gif"%os.getcwd())
        menosY.config(image=img_baixo)
        menosY.grid(row=0,column=4,sticky=W)
        maisY = Button(self.parent, command = self.maisy)
        img_cima = PhotoImage(file="%s/imagens/cima.gif"%os.getcwd())
        maisY.config(image=img_cima)
        maisY.grid(row=0,column=5,sticky=W)
        ampDown = Button(self.parent,command = self.ampdown)
        img_menos = PhotoImage(file="%s/imagens/menos.gif"%os.getcwd())
        ampDown.config(image=img_menos)
        ampDown.grid(row=0,column=6,sticky=W)
        ampUp = Button(self.parent, command = self.ampup)
        img_mais = PhotoImage(file="%s/imagens/mais.gif"%os.getcwd())
        ampUp.config(image=img_mais)
        ampUp.grid(row=0,column=7,sticky=W)
        normal = Button(self.parent, command = self.normalizar)
        img_norm = PhotoImage(file="%s/imagens/norm.gif"%os.getcwd())
        normal.config(image=img_norm)
        normal.grid(row=0,column=8,sticky=W)
        inverttime = Button(self.parent, command = self.invert)
        img_invert = PhotoImage(file="%s/imagens/invert.gif"%os.getcwd())
        inverttime.config(image=img_invert)
        inverttime.grid(row=0,column=9,sticky=W)
        pickAmostras = Button(self.parent, command = self.pickAmostra)
        img_cortar = PhotoImage(file="%s/imagens/cortar.gif"%os.getcwd())
        pickAmostras.config(image=img_cortar)
        pickAmostras.grid(row=0,column=10,sticky=W)
        somb_null = Button(self.parent, command = self.sombNull)
        img_sombnull = PhotoImage(file="%s/imagens/fill_null.gif"%os.getcwd())
        somb_null.config(image=img_sombnull)
        somb_null.grid(row=0,column=11,sticky=W)
        somb_neg = Button(self.parent, command = self.sombNeg)
        img_sombneg = PhotoImage(file="%s/imagens/fill_neg.gif"%os.getcwd())
        somb_neg.config(image=img_sombneg)
        somb_neg.grid(row=0,column=12,sticky=W)
        somb_pos = Button(self.parent, command = self.sombPos)
        img_sombpos = PhotoImage(file="%s/imagens/fill_pos.gif"%os.getcwd())
        somb_pos.config(image=img_sombpos)
        somb_pos.grid(row=0,column=13,sticky=W) 
        clipar = Button(self.parent, command = self.clip)
        img_clip = PhotoImage(file="%s/imagens/clip.gif"%os.getcwd())
        clipar.config(image=img_clip)
        clipar.grid(row=0,column=14,sticky=W)
        PA = Button(self.parent, command = self.filtroHP)
        img_PA = PhotoImage(file="%s/imagens/PA.gif"%os.getcwd())
        PA.config(image=img_PA)
        PA.grid(row=0,column=15,sticky=W)
        PB = Button(self.parent, command = self.filtroLP)
        img_PB = PhotoImage(file="%s/imagens/PB.gif"%os.getcwd())
        PB.config(image=img_PB)
        PB.grid(row=0,column=16,sticky=W)
        RF = Button(self.parent, command = self.removerFiltros)
        img_RF = PhotoImage(file="%s/imagens/RF.gif"%os.getcwd())
        RF.config(image=img_RF)
        RF.grid(row=0,column=17,sticky=W)
        Pick = Button(self.parent, command = self.ativarPick)
        img_pick = PhotoImage(file="%s/imagens/pick.gif"%os.getcwd())
        Pick.config(image=img_pick)
        Pick.grid(row=0,column=18,sticky=W)
        ligar = Button(self.parent, command = self.ligarPicks)
        img_ligar = PhotoImage(file="%s/imagens/ligar.gif"%os.getcwd())
        ligar.config(image=img_ligar)
        ligar.grid(row=0,column=19,sticky=W)
        limpar = Button(self.parent, command = self.limparplot)
        img_limpar = PhotoImage(file="%s/imagens/limpar.gif"%os.getcwd())
        limpar.config(image=img_limpar)
        limpar.grid(row=0,column=20,sticky=W)
        vel = Button(self.parent, command = self.pickVelocidade)
        img_vel = PhotoImage(file="%s/imagens/vel.gif"%os.getcwd())
        vel.config(image=img_vel)
        vel.grid(row=0,column=21,sticky=W)
        grafico = Button(self.parent, command = self.verCurva)
        img_grafico = PhotoImage(file="%s/imagens/grafico.gif"%os.getcwd())
        grafico.config(image=img_grafico)
        grafico.grid(row=0,column=22,sticky=W)
        opt = Button(self.parent, command = self.configPlot)
        img_opt = PhotoImage(file="%s/imagens/opt.gif"%os.getcwd())
        opt.config(image=img_opt)
        opt.grid(row=0,column=23,sticky=W)
        header = Button(self.parent, command = self.cabecalho)
        img_header = PhotoImage(file="%s/imagens/header.gif"%os.getcwd())
        header.config(image=img_header)
        header.grid(row=0,column=24,sticky=W)
        FecharPlot = Button(self.parent, command = self.fecharPlot)
        img_fechar = PhotoImage(file="%s/imagens/fechar.gif"%os.getcwd())
        FecharPlot.config(image=img_fechar)
        FecharPlot.grid(row=0,column=25,sticky=W)
        self.statusPick = Label(self.parent,text = ' ', fg='red',font=("Helvetica", 12), bg='#F3F3F3')
        self.statusPick.grid(row=0,column=26,sticky=E)
        self.statusVel = Label(self.parent,text = ' ', fg='red',font=("Helvetica", 12), bg='#F3F3F3')
        self.statusVel.grid(row=0,column=27,sticky=E)
        self.statusCortador = Label(self.parent,text = ' ', fg='red',font=("Helvetica", 12), bg='#F3F3F3')
        self.statusCortador.grid(row=0,column=28,sticky=E)
        self.statusPA = Label(self.parent,text = ' ', fg='green',font=("Helvetica", 12),bg='#F3F3F3')
        self.statusPA.grid(row=0,column=29,sticky=E)
        self.statusPB = Label(self.parent,text = ' ', fg='green',font=("Helvetica", 12),bg='#F3F3F3')
        self.statusPB.grid(row=0,column=30,sticky=E)
        self.status = Label(self.parent,text = ' ', fg='red',font=("Helvetica", 12),bg='#F3F3F3')
        self.status.grid(row=0,column=31,sticky=E)
        plt.rcParams['keymap.zoom'] = 'z,Z'
        plt.rcParams['keymap.back'] = 'b,B'
        plt.rcParams['keymap.home'] = 'ctrl+z,ctrl+Z'
        plt.rcParams['keymap.save'] = 'ctrl+i,ctrl+I'
        plt.rcParams['keymap.pan'] = 'm,M'
        self.bind('<Alt-s>', lambda x: self.destroy())
        self.bind('<Alt-S>', lambda x: self.destroy())
        self.bind('A', lambda x: self.pickAmostra())
        self.bind('a', lambda x: self.pickAmostra())
        self.bind('<Alt-L>', lambda x: self.ligarPicks())
        self.bind('<Alt-l>', lambda x: self.ligarPicks())
        self.bind('l', lambda x: self.ligarPicks())
        self.bind('V', lambda x: self.pickVelocidade())
        self.bind('v', lambda x: self.pickVelocidade())
        self.bind('<Control-a>', lambda x: self.abrir_pt1())
        self.bind('<Control-A>', lambda x: self.abrir_pt1())
        self.bind('<Control-l>', lambda x: self.limparplot())
        self.bind('<Control-L>', lambda x: self.limparplot())
        self.bind('<Control-s>', lambda x: self.salvarpick())
        self.bind('<Control-S>', lambda x: self.salvarpick())
        self.bind('<Control-x>', lambda x: self.fecharPlot())
        self.bind('<Control-X>', lambda x: self.fecharPlot())
        self.bind('<Control-o>', lambda x: self.configPlot())
        self.bind('<Control-O>', lambda x: self.configPlot())
        self.bind('<Control-g>', lambda x: self.verCurva())
        self.bind('<Control-G>', lambda x: self.verCurva())
        self.bind('<Control-h>', lambda x: self.cabecalho())
        self.bind('<Control-H>', lambda x: self.cabecalho())
        self.bind('<Shift-Left>', lambda x: self.ampdown())
        self.bind('<Shift-Right>', lambda x: self.ampup())
        self.bind('<Up>', lambda x: self.maisy())
        self.bind('<Down>', lambda x: self.menosy())
        self.bind('i', lambda x: self.invert())
        self.bind('n', lambda x: self.normalizar())
        self.bind('<Alt-Right>', lambda x: self.sombNeg())
        self.bind('<Alt-Left>', lambda x: self.sombPos())
        self.bind('<Alt-Down>', lambda x: self.sombNull())
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

        if self.plotExiste == True:

            self.fecharPlot()
            self.destroy()
            sys.exit()

        else:

            self.destroy()
            sys.exit()
            
    def abrir_pt1(self):
        
        if self.plotExiste == False:
                    
            self.arquivos = sorted(filedialog.askopenfilenames(title='Abrir',
                                                               filetypes=[('seg2','*.dat'),
                                                                ('seg2','*.DAT'),('segy','*.sgy')]))

            if len(self.arquivos) > 0:

                self.status.configure(text=' Abrindo %d arquivo(os). Aguarde...'%len(self.arquivos))

               # try:
                
                for i in range(len(self.arquivos)):

                    self.sts.append(read(self.arquivos[i]))
                    self.ndados.append(len(self.sts[i][0]))

                    if self.sts[i][0].stats._format == 'SEG2':

                        self.formato = 'seg2'

                    elif self.sts[i][0].stats._format == 'SEGY':

                        self.formato = 'segy'

                    else:

                        messagebox.showerror('Geosis - Sispick', 'Formato invalido. Mais informaçoes em Ajuda > Erros')
                        break

                    if self.formato == 'seg2':

                        try:
                            
                            self.listSource.append(self.sts[i][0].stats.seg2['SOURCE_LOCATION'])

                        except:

                            messagebox.showinfo('Geosis - Sispick','Posição(ões) de fonte(s) não encontrada(as) no(s) cabeçalho(s).\nPara adicionar vá em Opções > Editar cabeçalho')
                            self.listSource.append(999)

                    elif self.formato == 'segy':

                        try:
                            
                            self.listSource.append(self.sts[i][0].stats.segy['SOURCE_LOCATION'])

                        except:

                            messagebox.showinfo('Geosis - Sispick','Posição(ões) de fonte(s) não encontrada(as) no(s) cabeçalho(s).\nPara adicionar vá em Opções > Editar cabeçalho')
                            self.listSource.append(999)

                    if self.formato == 'seg2':

                        try:

                            self.posicaoGeof1 = float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])

                        except:

                            self.posicaoGeof1 = 0
                            messagebox.showinfo('Geosis - Sispick', 'Posiçao do primeiro geofone nao encontrada. Sera utilizado 0 m.\nPara alterar va em Opçoes > Editar cabeçalho')

                    elif self.formato == 'segy':

                        try:

                            self.posicaoGeof1 = float(self.sts[i][0].stats.segy['RECEIVER_LOCATION'])

                        except:

                            self.posicaoGeof1 = 0
                            messagebox.showinfo('Geosis - Sispick', 'Posiçao do primeiro geofone nao encontrada. Sera utilizado 0 m.\nPara alterar va em Opçoes > Editar cabeçalho')


                    if self.formato == 'seg2':
                        
                        try:
                            
                            self.valordx = float(self.sts[0][1].stats.seg2['RECEIVER_LOCATION'])-float(self.sts[0][0].stats.seg2['RECEIVER_LOCATION'])

                        except:
                            
                            self.configDx()

                    elif self.formato == 'segy':
                        
                        try:
                            
                            self.valordx = float(self.sts[0][1].stats.segy['RECEIVER_LOCATION'])-float(self.sts[0][0].stats.segy['RECEIVER_LOCATION'])

                        except:
                            
                            self.configDx()

                if self.ndados[0] > 10000:

                    messagebox.showinfo('Geosis - Sispick','Para acelerar o processamento utilize o cortador de amostras em Editar > Cortas amostras')

                self.abrir_pt2()

               # except:

                 #   messagebox.showerror('Geosis - Sispick','Erro na leitura do arquivo. Informações em Ajuda > Erros')
                   # self.status.configure(text='')
                  #  del self.sts[:]
                  #  del self.ndados[:]
                  #  self.arquivos = None

        else:
        
            messagebox.showinfo('','Feche a seçao sismica atual para abrir uma nova')

    def abrir_pt2(self):
        
        for i in range(len(self.arquivos)):

            frame = Frame(self,bg='#F3F3F3')
            frame.grid(row=1, column=0,sticky='nsew')
            self.frames.append(frame)
            fig = plt.figure(i,figsize=(self.valorFigx,self.valorFigy),facecolor='#F3F3F3')
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
            plt.title(' %s | %d canais'%(os.path.basename(self.arquivos[i]),int(self.canais)))     
            plt.xlabel('Distância (m)')
            plt.ylabel('Tempo (ms)')
            plt.ylim(0,1000*(self.sts[i][0].stats.delta*self.ndados[i]))
            plt.xlim(self.posicaoGeof1-self.valordx,self.posicaoGeof1+self.valordx*len(self.sts[i]))
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
        self.clickOn = False
        self.pickVelOn = False

    def nextpage(self):
        
        if self.plotExiste == True and self.pagina < len(self.arquivos)-1:
            
            frame = self.frames[self.pagina+1]
            frame.tkraise()
            self.pagina += 1
            self.telas[self.pagina].show()

            if self.filtrosHP[self.pagina] == True:
                
                self.statusPA.configure(text = 'Passa alta: %.2f Hz'%float(self.freqHP[self.pagina]/self.fatorHP))

            if self.filtrosLP[self.pagina] == True:

                self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%float(self.freqLP[self.pagina]/self.fatorLP))

            if self.filtrosHP[self.pagina] != True:

                self.statusPA.configure(text = '')

            if self.filtrosLP[self.pagina] != True:
                
                self.statusPB.configure(text = '')

    def backpage(self):

        if self.plotExiste == True and self.pagina != 0:
                
            frame = self.frames[self.pagina-1] 
            frame.tkraise()
            self.pagina -= 1
            self.telas[self.pagina].show()

            if self.filtrosHP[self.pagina] == True:
                
                self.statusPA.configure(text = 'Passa alta: %.2f Hz'%float(self.freqHP[self.pagina]/self.fatorHP))

            if self.filtrosLP[self.pagina] == True:

                self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%float(self.freqLP[self.pagina]/self.fatorLP))

            if self.filtrosHP[self.pagina] != True:

                self.statusPA.configure(text = '')

            if self.filtrosLP[self.pagina] != True:
                
                self.statusPB.configure(text = '')
                    
    def ativarPick(self):
        
        if self.plotExiste == True:

            if self.pickMode == False:

                self.pickMode = True
                self.statusPick.configure(text=' Pick ativado',fg='blue')
                
                def pick(event):

                    try:

                        self.coordx.append(event.xdata)
                        self.coordy.append(event.ydata)
                        self.linhaPick, = self.axes[self.pagina].plot(self.coordx,self.coordy,color='red')
                        self.clickOn = True
                        nearestMagnetValue = min(self.okpicks, key=lambda x: abs(event.xdata - x))
                        
                        if nearestMagnetValue in self.picks[self.pagina]:

                            self.picks[self.pagina][nearestMagnetValue] = event.ydata
                            self.picksArts[self.pagina][nearestMagnetValue].remove()
                            pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-1,
                                                                nearestMagnetValue+1,colors='r',linestyle='solid')
                            self.picksArts[self.pagina][nearestMagnetValue] = pickline
                            self.telas[self.pagina].show()
                                    
                        else:
                            
                            pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-1,
                                                                nearestMagnetValue+1,colors='r',linestyle='solid')
                            self.picksArts[self.pagina].update({nearestMagnetValue:pickline})
                            self.picks[self.pagina].update({nearestMagnetValue:event.ydata})
                            self.telas[self.pagina].show()

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
                                    self.telas[self.pagina].show()

                        if self.linhasPick[self.pagina] != None and bool(self.picks[self.pagina]) == True:

                            self.linhasPick[self.pagina].set_data([key for key in sorted(self.picks[self.pagina])],
                                    [self.picks[self.pagina][key] for key in sorted(self.picks[self.pagina])])
                            self.telas[self.pagina].show()

                    except:

                       pass

                def movimento(event):

                    if self.clickOn == True:

                        try:

                            self.coordx.append(event.xdata)
                            self.coordy.append(event.ydata)
                            self.linhaPick.set_data(self.coordx,self.coordy)
                            self.telas[self.pagina].show()
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
                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-1,
                                                                                i+1,colors='r',linestyle='solid')
                                            self.picksArts[self.pagina][i] = pickline

                                        else:

                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-1,
                                                                        i+1,colors='r',linestyle='solid')
                                            self.picksArts[self.pagina].update({i:pickline})
                                            self.picks[self.pagina].update({i:m*i+b})

                            else:

                                for i in arange(valorMaisproximo1,valorMaisproximo2-self.valordx, -self.valordx):
                                

                                    if i in self.okpicks:

                                        if i in self.picks[self.pagina]:

                                            self.picks[self.pagina][i] = m*i+b
                                            self.picksArts[self.pagina][i].remove()
                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-1,
                                                                                i+1,colors='r',linestyle='solid')
                                            self.picksArts[self.pagina][i] = pickline

                                        else:

                                            pickline = self.axes[self.pagina].hlines(m*i+b,i-1,
                                                                        i+1,colors='r',linestyle='solid')
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

                            self.telas[self.pagina].show()
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
            root.title('Geosis - Sispick') 
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
                        
                        bola = ax.scatter(key, self.picks[i][key],s=40,c = 'white',picker = 5)
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

            plt.title('Previa de curva de tempo de percurso')    
            plt.xlabel('Distância (m)')
            plt.ylabel('Tempo (ms)')
            plt.grid()
            canvas = FigureCanvasTkAgg(fig, root)
            canvas.show()
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

                if messagebox.askyesno("Geosis - Sispick", "Limpar picks do sismograma atual?"):

                    for i in self.picksArts[self.pagina].values():
                    
                        i.remove()

                    self.picks[self.pagina].clear()
                    self.picksArts[self.pagina].clear()
                    self.telas[self.pagina].show()

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
                                
                        self.telas[i].show()
                    
    def fecharPlot(self):
          
        if self.plotExiste == True:

            if messagebox.askyesno("Geosis - Sispick", "Fechar o projeto atual?"):

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

            self.telas[i].show()

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
                
                if messagebox.askyesno('Geosis - Sispick', 'Atualizar os plots para número de amostras original (%d)?'%int(len(self.sts[0][0]))):

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
                self.telas[self.pagina].show()

    def filtroLP(self):

        if self.plotExiste == True:

            if self.normalizado == True:

                if self.filtros[self.pagina] != True:

                    self.copiasNorms[self.pagina] = self.sts[self.pagina].copy().normalize()
                    self.copiasNorms[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP

                else:

                    self.copiasNorms[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)

            else:

                if self.filtros[self.pagina] != True:

                    self.copiasCruas[self.pagina] = self.sts[self.pagina].copy().normalize(1)
                    self.copiasCruas[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP

                else:

                    self.copiasCruas[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)

            self.filtrosLP[self.pagina] = True        
            self.filtros[self.pagina] = True
            self.conferidorIndividual()
            self.telas[self.pagina].show()

    def filtroHP(self):

        if self.plotExiste == True:

            if self.normalizado == True:

                if self.filtros[self.pagina] != True:

                    self.copiasNorms[self.pagina] = self.sts[self.pagina].copy().normalize()
                    self.copiasNorms[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP

                else:

                    self.copiasNorms[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)

            else:

                if self.filtros[self.pagina] != True:

                    self.copiasCruas[self.pagina] = self.sts[self.pagina].copy().normalize(1)
                    self.copiasCruas[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP

                else:

                    self.copiasCruas[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP = self.freqHP[self.pagina]*self.fatorHP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+self.posicaoGeof1+j*self.valordx)

            self.filtrosHP[self.pagina] = True
            self.filtros[self.pagina] = True
            self.conferidorIndividual()
            self.telas[self.pagina].show()

    def salvargp(self):

        if not self.picks[:]:

            messagebox.showerror('Geosis - Sispick','Nao há picks')
            
        else:
            
            try:
                
                arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('Geosis pick', '.gp')])

                if platform.system() == 'Windows':
                    
                    with open(arquivoSaida+'.gp','a') as arqpck:

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
                    
                messagebox.showinfo('Geosis - Sispick','Pick salvo')

            except:

                pass

    def salvarpick(self):

        if not self.picks[:]:

            messagebox.showerror('Geosis - Sispick','Nao há picks')
            
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
                    
                messagebox.showinfo('Geosis - Sispick','Pick salvo')

            except:

                pass

    def pickVelocidade(self):

        if self.plotExiste == True:

            if self.pickVelOn == False:

                self.statusVel.configure(text = 'Velocidade aparente ativada',fg='blue')

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
                
                    if messagebox.askyesno('Geosis - Sispick', 'Cortar o plot para %d ms?'%int(event.ydata)):

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
            root.title('Geosis - Sispick')
            root.resizable(0,0)
            fonte = StringVar()
            dx = StringVar()
            comp = StringVar()
            pos1 = StringVar()
            main = Label(root, text = 'Dados do cabeçalho (%s)'%os.path.basename(self.arquivos[self.pagina]),font=("Helvetica", 14),
                         fg='green').grid(row = 0, column = 0, sticky='w', padx = 10, pady = 10)
            fonte = Label(root, text = 'Posição da fonte (atual: %.1f m):'%float(self.listSource[self.pagina]),font=("Helvetica", 10),
                         fg='black').grid(row = 1, column = 0, sticky='w', padx = 10, pady = 10)
            espacamento = Label(root, text = 'Espaçamento entre geofones (atual: %.1f m):'%float(self.valordx),font=("Helvetica", 10),
                         fg='black').grid(row = 2, column = 0, sticky='w', padx = 10, pady = 10)
            comp = Label(root, text = 'Comprimento do perfil (atual: %.1f m):'%(self.valordx*len(self.sts[self.pagina])),
                         font=("Helvetica", 10),fg='black').grid(row = 3, column = 0, sticky='w', padx = 10, pady = 10)
            pos = Label(root, text = 'Posiçao do primeiro geofone (atual: %.1f m):'%self.posicaoGeof1,
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
                            self.telas[i].show()
                            
                    except:

                        warning.configure(text = 'Comprimento de perfil inválido', fg = 'red')

                if len(entrypos1.get()) > 0:

                    self.posicaoGeof1 = float(entrypos1.get())

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
            root.title('Geosis - Sispick')
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
            labelFigx = Label(root, text='Tamanho x do plot (atual: %.1f): '%self.valorFigx,
                              font=("Helvetica", 10)).grid(row=3, column=0, sticky="w",padx=20,pady=10)
            entryFigx = Entry(root, textvariable = varFigx,width=10)
            entryFigx.grid(row=3, column=0, sticky="w",padx=235,pady=10)
            labelFigy = Label(root, text='Tamanho y do plot (atual: %.1f): '%self.valorFigy,
                              font=("Helvetica", 10)).grid(row=4, column=0, sticky="w",padx=20,pady=10)
            entryFigy = Entry(root, textvariable = varFigy,width=10)
            entryFigy.grid(row=4, column=0, sticky="w",padx=235,pady=10)
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
        root.title('Geosis - Sispick')
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

                messagebox.showinfo('Geosis - Sispick', 'Espaçamento entre geofones padrão será usado: 2 m')
                self.valordx = 2
                root.destroy()
                self.abrir_pt2()
                                    
        def cancelar():

            messagebox.showinfo('Geosis - Sispick', 'Espaçamento entre geofones padrão será usado: 2 m')
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


class sisref(Tk):

    def __init__(self):

        Tk.__init__(self)
        self.configure(background='#F3F3F3')
        self.title('Geosis - sisref')
        
        if platform.system() == 'Windows':

            self.wm_state('zoomed')

            try:

                self.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

            except:

                pass

        else:
            
            self.attributes('-zoomed',True)
        
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        parent = Frame(self,bg='#F3F3F3')
        parent.grid(row=0,column=0,sticky='nsew')
        barraDEmenu = Menu(self)
        self.configure(menu=barraDEmenu)
        menu_arquivo=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Arquivo',menu=menu_arquivo)
        menu_arquivo.add_command(label='Abrir arquivo tempo de percurso (.gp)                    Ctrl+A',
                                      command=self.abrirgp)
        menu_curva=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Curvas',menu=menu_curva)
        menu_curva.add_command(label='Editar curvas                    Ctrl+E',
                                      command=self.editarCurva)
        menu_inversao=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Inversão',menu=menu_inversao)
        menu_inversao.add_command(label='Atribuir camada 2                    Ctrl+E',
                                      command=self.camadas)
        menu_inversao.add_command(label='Atribuir camada 3                    Ctrl+E',
                                      command=self.camadas)
        menu_inversao.add_command(label='Calcular velocidades                    Ctrl+E',
                                      command=self.velocidades)

        Abrir = Button(parent, command = self.abrirgp)
        img_abrir = PhotoImage(file="%s/imagens/abrir.gif"%os.getcwd())
        Abrir.config(image=img_abrir)
        Abrir.grid(row=0,column=0,sticky=W)
        Salvar = Button(parent, command = self.abrirgp)
        img_salvar = PhotoImage(file="%s/imagens/salvar.gif"%os.getcwd())
        Salvar.config(image=img_salvar)
        Salvar.grid(row=0,column=1,sticky=W)
        Editor = Button(parent, command = self.editarCurva)
        img_edit = PhotoImage(file="%s/imagens/edit.gif"%os.getcwd())
        Editor.config(image=img_edit)
        Editor.grid(row=0,column=2,sticky=W)
        Camadas = Button(parent, command = self.camadas)
        img_camadas = PhotoImage(file="%s/imagens/camadas.gif"%os.getcwd())
        Camadas.config(image=img_camadas)
        Camadas.grid(row=0,column=3,sticky=W)
        VA = Button(parent, command = self.pickVA)
        img_vel = PhotoImage(file="%s/imagens/vel.gif"%os.getcwd())
        VA.config(image=img_vel)
        VA.grid(row=0,column=4,sticky=W)
        inv = Button(parent, command = self.velocidades)
        img_inv = PhotoImage(file="%s/imagens/inv.gif"%os.getcwd())
        inv.config(image=img_inv)
        inv.grid(row=0,column=5,sticky=W)
        
        self.status = Label(parent,text = '', fg='green',font=("Helvetica", 12))
        self.status.grid(row=0,column=6,sticky=E)
        self.frame = Frame(self,bg='#F3F3F3')
        self.frame.grid(row=1, column=0,sticky='nsew')

        self.xData = {}
        self.yData = {}
        self.linhas = []
        self.fontes = {}
        self.bolas = {}
        self.camadas = {}
        self.xDataCamada1 = {}
        self.yDataCamada1 = {}
        self.xDataCamada2 = {}
        self.yDataCamada2 = {}
        self.sublinhas = {}
        self.especiais = {}
        self.cores = {}
        self.temp = []
        self.coordx = []
        self.coordy = []
        self.linhasVel = []
        self.textosVel = []
        self.conexoes = []
        self.dCamada1 = None
        self.GCamada1 = None
        self.dCamada2 = None
        self.GCamada2 = None
        self.nlinhas = 0
        self.count = 1
        self.count2 = 0
        self.sublinha = 0
        self.linha = None
        self.cor = None
        self.artista = None
        self.linhaVel = None
        self.clickOn = False
        self.pickVelOn = False

        if platform.system() == 'Windows':
        
            self.valorFigx = self.winfo_screenwidth()/160

            if self.winfo_screenheight() == 1080:
                
                self.valorFigy = self.winfo_screenheight()/93.1

            elif self.winfo_screenheight() == 768:

                self.valorFigy = self.winfo_screenheight()/100.5

            elif self.winfo_screenheight() == 1024:

                self.valorFigy = self.winfo_screenheight()/94.1

            elif self.winfo_screenheight() == 900:

                self.valorFigy = self.winfo_screenheight()/96.5

            elif self.winfo_screenheight() == 720:

                self.valorFigy = self.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = self.winfo_screenheight()/99

        elif platform.system() == 'Linux':

            self.valorFigx = self.winfo_screenwidth()/168

            if self.winfo_screenheight() == 1080:
                
                self.valorFigy = self.winfo_screenheight()/93.1

            elif self.winfo_screenheight() == 768:

                self.valorFigy = self.winfo_screenheight()/96

            elif self.winfo_screenheight() == 1024:

                self.valorFigy = self.winfo_screenheight()/94.1

            elif self.winfo_screenheight() == 900:

                self.valorFigy = self.winfo_screenheight()/96.5

            elif self.winfo_screenheight() == 720:

                self.valorFigy = self.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = self.winfo_screenheight()/99

        plt.rcParams['keymap.zoom'] = 'z,Z'
        plt.rcParams['keymap.back'] = 'v,V'
        plt.rcParams['keymap.home'] = 'ctrl+z,ctrl+Z'
        plt.rcParams['keymap.save'] = 'ctrl+i,ctrl+I'
        plt.rcParams['keymap.pan'] = 'm,M'
        self.bind('<Control-a>', lambda x: self.abrirgp())
        self.bind('<Control-A>', lambda x: self.abrirgp())

        self.curvaExiste = False
        
        self.mainloop()

    def fechar(self):

        if messagebox.askyesno("Geosis - sisref", "Sair do programa?"):

            self.destroy()

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
                self.tela = FigureCanvasTkAgg(self.fig, self.frame)
                self.tela.show()
                self.tela.get_tk_widget().pack(fill='both', expand=True)
                toolbar = NavigationToolbar2TkAgg(self.tela, self.frame)
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
                            
                                if float(bola.get_offsets()[0][1]) >= float(event.artist.get_offsets()[0][1]):

                                    bola.set_color('#1BB270')
                                    self.camadas[event.artist] = 2
                                    self.xDataCamada2[linha].append(float(bola.get_offsets()[0][0]))
                                    self.yDataCamada2[linha].append(float(bola.get_offsets()[0][1]))

                                    for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = '#1BB270'
                                                break

                                elif float(bola.get_offsets()[0][1]) <= float(event.artist.get_offsets()[0][1]):

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

            for i in range(len(self.fontes)+len(self.xData[1])):
                    
                smooth[count][count] = 0.5
                smooth[count][count+1] = -0.5
                count+=1
            
            smooth_G2 = np.concatenate((self.GCamada2,smooth))
            smooth_d2 =  np.hstack((self.dCamada2,[i*0 for i in range(len(self.fontes)+len(self.xData[1]))]))
                    
            m1 = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(self.GCamada1),self.GCamada1)),np.transpose(self.GCamada1)),self.dCamada1)
            #m2 = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(self.GCamada2),self.GCamada2)),np.transpose(self.GCamada2)),self.dCamada2)
            m2 = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(smooth_G2),smooth_G2)),np.transpose(smooth_G2)),smooth_d2)
            
            messagebox.showinfo('','Velocidades médias: camada 1 = %.2f km/s, camada 2 = %.2f km/s'%(1/m1[-1],1/m2[-1]))
            xnew = np.linspace(0, 10, num=41, endpoint=True)

            frame2 = Frame(self)
            frame2.grid(row = 1, column = 1)
            fig2 = plt.figure(figsize=(self.valorFigx,self.valorFigy),facecolor='#F3F3F3')

            ax2 = fig2.add_subplot(111)

            x_smooth = np.linspace(np.array(temp).min(),np.array(temp).max(), 300)
            y_smooth = spline(np.array(temp),-1*(m2[len(self.fontes):-1]*(1/m1[-1])*(1/m2[-1]))/np.sqrt(((1/m2[-1])**2)-(1/m1[-1])**2), x_smooth)
            
            l, = ax2.plot(x_smooth,y_smooth)
            ax2.set_ylabel('Elevação (m)')
            ax2.set_xlabel('Distância (m)')
            ax2.set_xlim(temp[0],temp[-1])
            ax2.set_ylim(min(l.get_ydata())*2,2)
            ax2.fill_between(x_smooth, y_smooth, 0, color = '#FF00C8')
            ax2.fill_between(x_smooth, y_smooth, min(l.get_ydata())-2, color = 'blue')
            ax2.text(temp[int(len(temp)/2)], -1, '%.1f km/s'%(round(1/m1[-1],1)), fontsize=18)
            ax2.text(temp[int(len(temp)/2)], min(l.get_ydata())-1, '%.1f km/s'%(round(1/m2[-1],1)), fontsize=18)
            plt.show()

            print(m2)
            print(1/m1[-1],1/m2[-1])
            #f = open('matriz.txt','w')
           # for i in smooth_G2:
                
              #  f.write(str(i).strip('[]')+'\n')
                
           # print(-1*(m2[len(self.fontes):-1]*(1/m1[-1])*(1/m2[-1]))/np.sqrt(((1/m2[-1])**2)-(1/m1[-1])**2))

            tela2 = FigureCanvasTkAgg(fig2, frame2)
            tela2.show()
            tela2.get_tk_widget().pack(fill='both', expand=True)
            toolbar2 = NavigationToolbar2TkAgg(tela2, frame2)
            toolbar2.update()
            tela2._tkcanvas.pack(fill='both', expand=True)
            

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
                            activeforeground = 'black', command = self.entrada,width = 3)
        self.botaoSaida = Button(self.frame, text=' ... ', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black', command = self.saida,width = 3)
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
        self.Arquivos = ''
        self.liststreams = []
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.mainloop()

    def fechar(self):

        if messagebox.askyesno("Geosis - Siscon", "Sair do programa?"):

            self.destroy()
        
    def entrada(self):
         
        self.Arquivos = filedialog.askopenfilenames(title='Abrir',filetypes=(('seg2','*.dat'),
                                                ('segy','*.sgy'),('mseed','*.mseed'),('Todos os arquivos','*.*')))

        try:
            
            for i in self.Arquivos:
                self.liststreams.append(read(i))

            entradaOK = Label(self.frame, text='OK',fg = 'blue',font=("Helvetica", 11))
            entradaOK.grid(row=0,column=0,sticky='e',padx=150)

        except:

            messagebox.showerror('Geosis - Siscon','Arquivo inválido')

    def saida(self):

        self.arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('segy','*.sgy'),('mseed','*.mseed')])
                                                        
        if len(self.arquivoSaida)>0:
            
            saidaOK = Label(self.frame, text='OK',fg = 'blue',font=("Helvetica", 11))
            saidaOK.grid(row=4,column=0,sticky='e',padx=150)
                
    def formatar(self):

        if len(self.Arquivos) == 0:

            self.warning.configure(text='Nenhum arquivo selecionado')

        elif self.select == False:

            self.warning.configure(text='Marque uma opção')

        elif len(self.arquivoSaida) == 0:

            self.warning.configure(text='Escolha o diretório de saída')
        
        elif self.select == True and len(self.Arquivos) > 0 and len(self.arquivoSaida) > 0:
            
            if self.nome_formato.get() == 'SEGY':

                try:
                    
                    for i in self.liststreams:
                        
                        i.write(self.arquivoSaida+'.sgy',format=self.nome_formato.get())

                    messagebox.showinfo('Geosis - Siscon','Conversão concluida')
                    
                except:

                    messagebox.showerror('Geosis - Siscon','Formato inválido')

            elif self.nome_formato.get() == 'MSEED':

                try:
                     
                    for i in self.liststreams:
                        
                        i.write(self.arquivoSaida+'.mseed',format=self.nome_formato.get())
                        
                    messagebox.showinfo('Geosis - Siscon','Conversão concluida')

                except:

                    messagebox.showerror('Geosis - Siscon','Formato inválido')
            
            for i in self.liststreams:
                
                del self.liststreams[:]
                
            self.frame.destroy()
            self.destroy()
        
    def cancelar(self):

        for i in self.liststreams:
                
            del self.liststreams[:]

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
