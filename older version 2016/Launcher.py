
from tkinter import *
from tkinter import filedialog, messagebox
import os                                                                              
import sys
import warnings
import platform

warnings.filterwarnings('ignore')     


class Launcher(Frame):
    
    def __init__(self, master, *args, **kwargs):

        print('''

    GEOSIS v1.0
    
    AUTOR: VICTOR JOSÉ C. B. GUEDES
    E-MAIL: vjs279@hotmail.com
    
    GEOFÍSICA - UNIVERSIDADE DE BRASILIA

    *fechar esta janela encerrará o programa*

                                        ''')
        Frame.__init__(self, master)
        self.winConfig()
        self.grid(row = 0,column = 0, sticky = 'nsew')
        self.menus()
        self.buttons()

    def winConfig(self):
        
        root.geometry('640x400')
        root.title('Geosis v1.0')

        try:
        
            photo = PhotoImage(file="%s/imagens/unb_geof.gif"%os.getcwd())

            if platform.system() == 'Windows':
            
                root.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

        except:

            messagebox.showerror('',"Arquivos faltando na pasta 'imagens'")

        labelPhoto = Label(self, image = photo)
        labelPhoto.image = photo
        labelPhoto.grid(row=0,column=0,sticky='nsew')
        root.protocol("WM_DELETE_WINDOW", self.fechar)

    def menus(self):
        
        menuBar = Menu(root)
        modMenu = Menu(menuBar)
        menuBar.add_cascade(label = 'Módulos', menu = modMenu)
        modMenu.add_command(label = 'Sispick',
                            command= self.chamarSispick)
        modMenu.add_command(label='Siscon',
                            command = self.chamarSiscon)
        helpMenu = Menu(menuBar)
        menuBar.add_cascade(label = 'Ajuda', menu = helpMenu)
        helpMenu.add_command(label = 'Sobre o software',
                             command = self.Sobre)
        root.config(menu = menuBar)

    def buttons(self):
        
        botaoSispick = Button(self, text='sispick',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSispick).grid(row=0,column=0,sticky='w')   
        botaosiscon = Button(self, text='siscon',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSiscon).grid(row=0,column=0,sticky='e')
        botaosisref = Button(self, text='sisref',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarsisref).grid(row=0,column=0,padx=50)
            
    def fechar(self):

        if messagebox.askyesno("Geosis", "Fechar o launcher?"):
            
            self.destroy()
            root.destroy()

    def chamarsisref(self):

        self.destroy()
        root.destroy()
        import Sisref

    def chamarSispick(self):

        self.destroy()
        root.destroy()
        import Sispick

    def chamarSiscon(self):

        self.destroy()
        root.destroy()
        import Sisref

    def Sobre(self):

        root = Tk()
        root.geometry('630x300')
        root.title('Info')
        titulo = Label(root, text='Sobre o software',fg='green',font=("Helvetica", 14))
        root.resizable(0,0)
        root.mainloop()
        

root = Tk()
Launcher(root)
root.mainloop()
