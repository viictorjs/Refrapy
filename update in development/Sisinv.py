from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
import os                                                                              
import numpy as np
import sys
import warnings
from pygimli.physics import Refraction
import random
from scipy.interpolate import interp1d
import scipy.interpolate
import pygimli as pg
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial import ConvexHull
from matplotlib.path import Path
from matplotlib.patches import PathPatch

np.set_printoptions(threshold=sys.maxsize)

warnings.filterwarnings('ignore')

class Sisinv(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row = 0, column = 0, sticky = NSEW)
        root.title('Refrainv')
        root.geometry("480x200")
        ttinv = Button(self, text = "Time-terms inversion", command = self.tt)
        ttinv.grid(row=0,column=0,sticky=E, padx = 70, pady = 25)
        tomoinv = Button(self, text = "Tomography inversion", command = self.tomo)
        tomoinv.grid(row=0,column=1,sticky=E)
        mod = Button(self, text = "Edit travel-times", command = self.editTT)
        mod.grid(row=1,column=0,sticky=E,padx = 70, pady = 25)

    def editTT(self, ax, fig):
        messagebox.showinfo('Refrainv', 'Select the .rp file with first arrival times.')
        try:
            ttFile = filedialog.askopenfilename(title='Open',filetypes=[('Refrapy pick','*.rp'),
                                                                        ('Refrapy pick old','*.gp'),
                                                                ('All files','*.*')])
        except:
            pass
        
        if ttFile != None:
            x, t = np.genfromtxt(ttFile, usecols = (0,1), unpack = True)
            fg = x[1]
            gn = t[0]
            gs = t[1]
            x = np.delete(x,[0,1])
            t = np.delete(t,[0,1])/1000
            sp = []
            for i in range(len(t)):
                if np.isnan(x[i]):
                    sp.append(t[i])
            sp = np.array(sp)*1000
            #fig = plt.figure()
            #ax = fig.add_subplot(111)
            #plt.grid(ls = '--', lw = 0.5)
            #ax.set_xlabel("Distance (m)")
            #ax.set_ylabel("Time (ms)")
            datax, datat = [], []
            artb = []
            for i in range(len(sp)):
                datax.append({sp[i]:[]})
                datat.append({sp[i]:[]})
                artb.append({sp[i]:[]})

            colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(sp))]

            s = 0
            for i in range(len(t)):
                if not np.isnan(x[i]):
                    datax[s][sp[s]].append(x[i])
                    datat[s][sp[s]].append(t[i])
                    if i == 0:
                        b = ax.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4,zorder=10,
                                       label = "Observed travel-times")
                    else:
                        b = ax.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4,zorder=10)
                    artb[s][sp[s]].append(b)
                else:
                    s+=1
            lines = []
            for i in range(len(sp)):
                ax.scatter(sp[i],0, marker = "*", c = "yellow", edgecolor = "k", s = 200, zorder=10)
                l = ax.plot(datax[i][sp[i]],datat[i][sp[i]], c = "k", lw = 0.75)
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
                            self.arti = np.where(np.array(datax[i][sp[i]]) == artx)[0][0]
      
            def onrelease(event):
                try:
                    datat[self.i][self.arts][self.arti] = event.ydata
                    self.art.set_offsets((self.art.get_offsets()[0][0],event.ydata))
                    for i in range(len(sp)):
                        lines[i][0].set_data(datax[i][sp[i]],datat[i][sp[i]])
                    fig.canvas.draw()
                except:
                    pass
                self.art = None
                self.arts = None
                self.i = None
                self.arti = None

            def onkey(event):
                if event.key == "d" or event.key == "D":
                    try:
                        rpFileOut = filedialog.asksaveasfilename(title='Save',filetypes=[('Refrapy pick', '*.rp')])
                    except:
                        pass
                    with open(rpFileOut+'.rp','w') as arqpck:
                        arqpck.write("%d %d\n%.2f %.2f\n"%(len(sp),gn,fg,gs))
                        for i in range(len(sp)):
                            for j in range(len(datax[i][sp[i]])):
                                arqpck.write('%f %f 1\n'%(datax[i][sp[i]][j],datat[i][sp[i]][j]*1000))
                            arqpck.write('/ %f\n'%sp[i])

            event = fig.canvas.mpl_connect('pick_event', onpick)
            event2 = fig.canvas.mpl_connect('button_release_event', onrelease)
            event3 = fig.canvas.mpl_connect('key_press_event', onkey)
            plt.legend(loc="best")
            plt.show()
                
    
    def tt(self):
        
        messagebox.showinfo('Refrainv', 'Select the .rp file with first arrival times.')
        try:
            ttFile = filedialog.askopenfilename(title='Open',filetypes=[('Refrapy pick','*.rp'),
                                                                        ('Refrapy pick old','*.gp'),
                                                                ('All files','*.*')])
        except:
            pass
        
        if ttFile != None:
            x, t = np.genfromtxt(ttFile, usecols = (0,1), unpack = True)
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
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.grid(ls = '--', lw = 0.5)
            ax.set_xlabel("Distance (m)")
            ax.set_ylabel("Time (ms)")
            datax, datat = [], []
            artb = []
            for i in range(len(sp)):
                datax.append({sp[i]:[]})
                datat.append({sp[i]:[]})
                artb.append({sp[i]:[]})

            colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(sp))]
            
            s = 0
            for i in range(len(t)):
                if not np.isnan(x[i]):
                    datax[s][sp[s]].append(x[i])
                    datat[s][sp[s]].append(t[i])
                    b = ax.scatter(x[i],t[i], s = 20, c = "white", edgecolor = "k", picker = 4)
                    artb[s][sp[s]].append(b)
                else:
                    s+=1
            lines = []
            for i in range(len(sp)):
                ax.scatter(sp[i],0, marker = "*", c = 'white', edgecolor = "k", s = 200)
                l = ax.plot(datax[i][sp[i]],datat[i][sp[i]], c = colors[i], lw = 0.75)
                lines.append(l)
                
            self.layer = 1
            ax.set_title('Layer %d interpratation activated!'%self.layer)
            self.layer1, self.layer2, self.layer3 = [],[],[]
            
            def onpick(event):
                art = event.artist
                artx = art.get_offsets()[0][0]
                artt = art.get_offsets()[0][1]

                for i in range(len(sp)):
                    if art in artb[i][sp[i]]:
                        arts = sp[i]
                        iS = i 
                        
                if artx >= arts:
                    for b in artb[iS][arts]:
                        bx = b.get_offsets()[0][0]
                        iG = np.where(np.array(artb[iS][arts]) == b)[0][0]
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
                    for b in artb[iS][arts]:
                        bx = b.get_offsets()[0][0]
                        iG = np.where(np.array(artb[iS][arts]) == b)[0][0]
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

                fig.canvas.draw()

            def findW(layer, G, d):
                w = 0.000000001
                sses, ws = [], []
                while w < 1:
                    rMs = np.zeros((int(len(layer)), int(len(sp)+gn+1)))
                    r = 0
                    for i in range(len(gp)):
                        for j in range(len(sp)):
                            if  sp[j] > min(gp) and sp[j] < max(gp): #se for fonte intermediaria                       
                                if gp[i]+gs >= sp[j] and gp[i]-gs <= sp[j]:

                                    rMs[r][j] = w
                                    rMs[r][len(sp)+i] = -w
                                    #print(sp[j],gp[i])
                                    r += 1
                            elif sp[j] <= min(gp):
                                if gp[i]-gs <= sp[j]:
                                    rMs[r][j] = w
                                    rMs[r][len(sp)+i] = -w
                                    #print(sp[j],gp[i])
                                    r += 1
                            elif sp[j] >= max(gp):
                                if gp[i]+gs >= sp[j]:
                                    rMs[r][j] = w
                                    rMs[r][len(sp)+i] = -w
                                    #print(sp[j],gp[i])
                                    r += 1      
                    rMs = rMs[~np.all(rMs == 0, axis=1)] #regularization matrix of time-terms from sources
                    rMg = np.zeros((int(len(layer)), int(len(sp)+gn+1)))
                    for i,j in zip(range(np.shape(rMg)[0]), range(np.shape(rMg)[1])):
                        try:
                            rMg[i][len(sp)+j] = w
                            rMg[i][len(sp)+j+1] = -w
                        except:
                            pass
                       
                    rMg = rMg[~np.all(rMg == 0, axis=1)][:-2] #regularization matrix of time-terms from geophones
                    rM = np.concatenate((rMs, rMg))
                    rd = np.hstack((d, [i*0 for i in range(np.shape(rM)[0])]))
                    rG = np.concatenate((G, rM))
                    sol, sse, rank, sv = np.linalg.lstsq(rG, rd)
                    if (sol <= 0).any():
                        pass
                    else:
                        try:
                            ws.append(w)
                            sses.append(sse[0])
                        except:
                            pass
                    w+=w*0.01
                return ws[sses.index(min(sses))]

            def solve(layer, G, d, w):
                
                rMs = np.zeros((int(len(layer)), int(len(sp)+gn+1)))
                r = 0
                for i in range(len(gp)):
                    for j in range(len(sp)):
                        if  sp[j] > min(gp) and sp[j] < max(gp): #se for fonte intermediaria                       
                            if gp[i]+gs >= sp[j] and gp[i]-gs <= sp[j]:

                                rMs[r][j] = w
                                rMs[r][len(sp)+i] = -w
                                #print(sp[j],gp[i])
                                r += 1
                        elif sp[j] <= min(gp):
                            if gp[i]-gs <= sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(sp)+i] = -w
                                #print(sp[j],gp[i])
                                r += 1
                        elif sp[j] >= max(gp):
                            if gp[i]+gs >= sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(sp)+i] = -w
                                #print(sp[j],gp[i])
                                r += 1      
                rMs = rMs[~np.all(rMs == 0, axis=1)] #regularization matrix of time-terms from sources
                rMg = np.zeros((int(len(layer)), int(len(sp)+gn+1)))
                for i,j in zip(range(np.shape(rMg)[0]), range(np.shape(rMg)[1])):
                    try:
                        rMg[i][len(sp)+j] = w
                        rMg[i][len(sp)+j+1] = -w
                    except:
                        pass
                   
                rMg = rMg[~np.all(rMg == 0, axis=1)][:-2] #regularization matrix of time-terms from geophones
                rM = np.concatenate((rMs, rMg))
                rd = np.hstack((d, [i*0 for i in range(np.shape(rM)[0])]))
                rG = np.concatenate((G, rM))
                sol, sse, rank, sv = np.linalg.lstsq(rG, rd)
                return sol, sse[0]

            
            def onkey(event):
                if event.key == "1":
                    self.layer = 1
                elif event.key == "2":
                    self.layer = 2
                elif event.key == "3":
                    self.layer = 3
                ax.set_title('Layer %d interpratation activated!'%self.layer)
                
                if event.key == "C" or event.key == "c":
                    if messagebox.askyesno("Refrainv", "Clear layer interpretation?"):
                        del self.layer1[:]
                        del self.layer2[:]
                        del self.layer3[:]
                        for i in range(len(sp)):
                            
                            for b in artb[i][sp[i]]:
                                b.set_color("white")
                                b.set_edgecolor("k")
                                
                if event.key == "i" or event.key == "I":
                    eFile = None
                    if self.layer1:
                        d1 = np.array([self.layer1[i][1] for i in range(len(self.layer1))])
                        G1 = np.array([self.layer1[i][3] for i in range(len(self.layer1))])
                        G1 = np.reshape(G1, (len(G1),1))
                        sol_layer1, res1, rank1, sv1 = np.linalg.lstsq(G1, d1)
                        v1 = 1000/sol_layer1[0] #m/s
                        rms1 = np.sqrt(res1/len(sol_layer1))

                        if messagebox.askyesno("Refrainv", "Use elevation file?"):
                            try:
                                eFile = filedialog.askopenfilename(title='Open',filetypes=[('Elevation file','*.txt'),
                                                                                    ('All files','*.*')])
                            except:
                                pass
                            
                            if eFile != None:
                                p, e = np.loadtxt(eFile, usecols = (0,1), unpack = True)
                                

                        if self.layer2:
                            d2 = np.array([self.layer2[i][1] for i in range(len(self.layer2))])
                            G2 = np.zeros((int(len(self.layer2)),
                                           int(len(sp)+gn+1)))

                            for i in range(len(self.layer2)):
                                G2[i][self.layer2[i][-2]] = 1
                                G2[i][self.layer2[i][-1]+len(sp)] = 1
                                G2[i][-1] = self.layer2[i][-3]

                            #w = findW(self.layer2, G2, d2)
                            sol_layer2, sse = solve(self.layer2, G2, d2, 0.1)
                            v2 = 1000/sol_layer2[-1] #m/s
                            rms2 = np.sqrt(sse/len(sol_layer2))

                        if self.layer3:
                            d3 = np.array([self.layer3[i][1] for i in range(len(self.layer3))])
                            G3 = np.zeros((int(len(self.layer3)),
                                           int(len(sp)+gn+1)))

                            for i in range(len(self.layer3)):
                                G3[i][self.layer3[i][-2]] = 1
                                G3[i][self.layer3[i][-1]+len(sp)] = 1
                                G3[i][-1] = self.layer3[i][-3]

                            w = findW(self.layer3, G3, d3)
           
                            sol_layer3, sse = solve(self.layer3, G3, d3, w)
                            print(sol_layer3,sse)
                            v3 = 1000/sol_layer3[-1] #m/s
                            rms3 = np.sqrt(sse/len(sol_layer3))
                            print(v3,rms3)
                            rmsMed = (rms2+rms3)/2

                        fvm = plt.figure()
                        axvm = fvm.add_subplot(111)
                        axvm.grid(lw = .5, ls = "-", color = "grey", alpha = .35)
                        axvm.set_title(label='Velocity model')
                        axvm.set_xlabel("Distance (m)")
                        
                        plt.gca().set_aspect('equal', adjustable='box')

                        if self.layer1 and self.layer2 and not self.layer3:
                            dtg = np.array([i for i in sol_layer2[:-1]]) #delay-time of all geophones
                            if eFile != None:

                                ge = [e[np.where(np.array(p) == np.array(gp)[i])[0]][0] for i in range(len(gp))]
                                se = [e[np.where(np.array(p) == np.array(sp)[i])[0]][0] for i in range(len(sp))]
                                dlayer2 = e-((dtg*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000)
                                axvm.set_ylabel("Elevation (m)")
                                f = interp1d(p, dlayer2, kind = 'cubic', fill_value='extrapolate')
                                sdlayer2 = f(np.linspace(p[0], p[-1], 1000))
                                
                                f = interp1d(p, e, kind = 'cubic', fill_value='extrapolate')
                                s_surf = f(np.linspace(p[0], p[-1], 1000))
                                axvm.fill_between(np.linspace(p[0], p[-1], 1000),sdlayer2,s_surf, color = "red", alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                                axvm.fill_between(np.linspace(p[0], p[-1], 1000),sdlayer2, min(sdlayer2)*0.99, alpha = .5,edgecolor = "k", color = "green", label = "%.0f m/s"%v2)
                                axvm.scatter(gp,ge,marker = 7, color = 'k',label = "Geophones")
                                axvm.scatter(sp, se,marker = "*", color = 'yellow',edgecolor = "k", s = 100, label = "Sources")
                            else:
                                dlayer2 = -1*(dtg*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000
                                sgp = np.sort(np.concatenate((np.arange(fg,fg+gn*gs,gs),np.array(sp))))
                                axvm.set_ylabel("Depth (m)")
                                try:
                                    f = interp1d(sgp, dlayer2, kind = 'cubic', fill_value='extrapolate')
                                    sdlayer2 = f(np.linspace(sgp[0], sgp[-1], 1000))
                                    axvm.fill_between(np.linspace(sgp[0], sgp[-1], 1000),
                                                      sdlayer2,0, color = "red", alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                                    axvm.fill_between(np.linspace(sgp[0], sgp[-1], 1000),
                                                      sdlayer2, min(sdlayer2)*1.1, alpha = .5,edgecolor = "k", color = "green", label = "%.0f m/s"%v2)
                                except:
                                    print(sgp)
                                    axvm.fill_between(sgp,
                                                      dlayer2,0, color = "red", alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                                    axvm.fill_between(sgp,
                                                      dlayer2, min(dlayer2)*1.1, alpha = .5,edgecolor = "k", color = "green", label = "%.0f m/s"%v2)
                                
                                axvm.scatter(np.arange(fg, int((gn*gs))+fg, gs),
                                          [i*0 for i in range(int(gn))],marker = 7, color = 'k',
                                             label = "Geophones")
                                axvm.scatter(sp, [i*0 for i in range(len(sp))],marker = "*", color = 'yellow',
                                         edgecolor = "k", s = 100, label = "Sources")
                            axvm.legend(loc='best')
                            #axvm.set_ylim((min(sdlayer2)*1.1-5,5))
                            messagebox.showinfo('Refrainv', 'RMS = %.5f ms'%rms2)
                            
                            plt.show()
                                    
                        elif self.layer1 and self.layer2 and self.layer3:
                
                            dtg2 = np.array([i for i in sol_layer2[len(sp):-1]]) #delay-time of all geophones
                            dlayer2 = -1*(dtg2*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000

                            f = interp1d(np.arange(fg, (gn*gs)+fg, gs), dlayer2, kind = 'cubic', fill_value='extrapolate')
                            sdlayer2 = f(np.linspace(fg, fg+(gn*gs)-gs, 1000))
                            
                            dtg3 = np.array([i for i in sol_layer3[len(sp):-1]]) #delay-time of all geophones

                            upvmed = (v1+v2)/2
                            dlayer3 = -1*(dtg3*upvmed*v3)/(np.sqrt((v3**2)-(upvmed**2)))/1000
                            
                            f = interp1d(np.arange(fg, (gn*gs)+fg, gs), dlayer3, kind = 'cubic', fill_value='extrapolate')
                            sdlayer3 = f(np.linspace(fg, fg+(gn*gs)-gs, 1000))
                            
                            axvm.fill_between(np.linspace(fg, fg+(gn*gs)-gs, 1000),
                                              sdlayer2,0, color = "red", alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                            axvm.fill_between(np.linspace(fg, fg+(gn*gs)-gs, 1000),
                                              sdlayer2, sdlayer3, alpha = .5,edgecolor = "k", color = "green", label = "%.0f m/s"%v2)
                            axvm.fill_between(np.linspace(fg, fg+(gn*gs)-gs, 1000),
                                              sdlayer3, min(sdlayer3)*1.1, alpha = .5,edgecolor = "k", color = "blue", label = "%.0f m/s"%v3)
                            axvm.scatter(np.arange(fg, int((gn*gs))+fg, gs),
                                      [i*0 for i in range(int(gn))],marker = 7, color = 'k',
                                         label = "Geophones")
                            axvm.scatter(sp, [i*0 for i in range(len(sp))],marker = "*", color = 'yellow',
                                     edgecolor = "k", s = 100, label = "Sources")
                            axvm.legend(loc='best')
                            axvm.set_ylim((min(sdlayer3)*1.1-5,5))
                            #axvm.set_ylim((min(sdlayer3)*1.1-5,5))
                            messagebox.showinfo('Refrainv', 'RMS = %.5f ms'%rmsMed)
                            plt.show()

                        if messagebox.askyesno("Refrainv", "Save velocity model results?"):
                            fvm.savefig(os.path.dirname(ttFile)+'\\timeterm_vm.png', dpi=fvm.dpi)
                            with open(os.path.dirname(ttFile)+'\\timeterm_vm.txt', "w") as arq:
                                if self.layer1 and self.layer2 and not self.layer3:
                                    arq.write("depth %.2f\nvtop %.2f\nvbottom %.2f\nrays 0\n"%(abs(min(dlayer2))*1.1,v1,v2))
                                elif self.layer1 and self.layer2 and self.layer3:
                                    arq.write("depth %.2f\nvtop %.2f\nvbottom %.2f\nrays 0\n"%(abs(min(dlayer3))*1.1,v1,v3))
                                arq.write("fg %.2f\ngn %d\ngs %.2f\n"%(fg,gn,gs))
                                arq.write("// sources\n")
                                for i in sp:
                                    arq.write("s %.2f\n"%i)
                                
                                if self.layer1 and self.layer2 and not self.layer3:
                                    arq.write("// layer2\n")
                                    for i in dlayer2:
                                        arq.write("d %.2f\n"%i)
                                elif self.layer1 and self.layer2 and self.layer3:
                                    arq.write("// layer3\n")
                                    for i in dlayer2:
                                        arq.write("d %.2f\n"%i)
                                    for i in dlayer3:
                                        arq.write("d %.2f\n"%i)
                            messagebox.showinfo('Refrainv', 'Time-term analysis was saved succesfully!')

                    else:
                        messagebox.showinfo('Refrainv', 'To invert data you must interpret at least direct wave arrivals!')

                fig.canvas.draw()

            event = fig.canvas.mpl_connect('pick_event', onpick)
            event2 = fig.canvas.mpl_connect('key_press_event', onkey)
            
            plt.show()

    def tomo(self):
        eFile = None
        if messagebox.askyesno("Refrainv", "Use elevation file?"):
            try:
                eFile = filedialog.askopenfilename(title='Open',filetypes=[('Elevation file','*.txt'),
                                                                    ('All files','*.*')])
            except:
                pass
            
            if eFile != None:
                p, e = np.loadtxt(eFile, usecols = (0,1), unpack = True)
                                
        if messagebox.askyesno("Refrainv", "Create a new pyGIMLy's tomography file?"):
            messagebox.showinfo('Refrainv', 'Select the .rp file with first arrival times.')
            rpFile = None
            try:
                rpFile = filedialog.askopenfilename(title='Open',filetypes=[('Refrapy pick','*.rp'),
                                                                            ('Refrapy pick old','*.gp'),
                                                                    ('All files','*.*')])
            except:
                pass

            if rpFile != None:
                x, t = np.genfromtxt(rpFile, usecols = (0,1), unpack = True)
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

                with open(rpFile[:-3]+"_tomo.txt", "w") as f:
                    f.write("%d # shot/geophone points\n#x y\n"%(gn+len(sp)))
                    for i in range(len(sgp)):
                        if eFile != None:
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
                messagebox.showinfo('Refrainv', '%s was created succesfully!'%(rpFile+"_tomo.txt"))
                
        else:
            messagebox.showinfo('Refrainv', "Select a pyGIMLy's tomography file for inversion.")
            pgFile = None
            try:
                pgFile = filedialog.askopenfilename(title='Open',filetypes=[("pyGIMLy's file",'*.txt'),
                                                                    ('All files','*.*')])
            except:
                pass

            if pgFile != None:
                a = np.genfromtxt(pgFile, usecols = (0), unpack = True)
                with open(pgFile) as f:
                    head = [next(f).split() for x in range(2+int(a[0]))][2:]
                
                data = pg.DataContainer(pgFile, 's g')
                ra = Refraction(data)

                if messagebox.askyesno("Refrainv", "Run default inversion?"):
                    
                    m = ra.createMesh(paraMaxCellSize=5.0, secNodes=1)
                    vest = ra.invert()
                    rrms = ra.inv.relrms() # relative RMS
                    arms = ra.inv.absrms() # Absolute RMS
                    messagebox.showinfo('Refrainv', "Inversion completed!\nRelative RMS = %.2f%%\nAbsolute RMS = %.6f ms"%(rrms,1000*arms))
                    x = np.array([i for i in pg.x(m.cellCenters())])
                    y = np.array([i for i in pg.y(m.cellCenters())])
                    v = np.array([i for i in vest])
                    spi = np.unique(ra.dataContainer("s"), return_inverse=False)
                    gi = np.unique(ra.dataContainer("g"), return_inverse=False)
                    a = np.genfromtxt(pgFile, usecols = (0), skip_header = 2, unpack = True)
                    sp = [a[:len(spi)+len(gi)][int(i)] for i in spi]
                    gp = [a[:len(spi)+len(gi)][int(i)] for i in gi]

                    figvm, axvm = plt.subplots()
                    x_grid = np.linspace(x.min(), x.max(), 500)
                    y_grid = np.linspace(y.min(), y.max(), 500)
                    xi,yi = np.meshgrid(x_grid,y_grid)
                    zi = scipy.interpolate.griddata((x, y), v, 
                                        (xi,yi), method='cubic')
                    if min(v) < 0:
                        vmin = 0
                    else:
                        vmin = min(v)

                    def convexhull(p):
                        p = np.array(p)
                        hull = ConvexHull(p)
                        return p[hull.vertices,:]
                    
                    def ccw_sort(p):
                        p = np.array(p)
                        mean = np.mean(p,axis=0)
                        d = p-mean
                        s = np.arctan2(d[:,0], d[:,1])
                        return p[np.argsort(s),:]

                    d = ra.getDepth()
                    head = [(float(head[i][0]),float(head[i][1])) for i in range(len(head))]
                    e = np.array([head[i][1] for i in range(len(head))])
                    sgp = np.array([head[i][0] for i in range(len(head))])

                    tail = [(head[i][0],max(y)-d) for i in range(len(head))]
                    
                    p = head+list(reversed(tail))

                    poly = plt.Polygon(p, ec="none", fc="none")
                    axvm.add_patch(poly)

                    cm = axvm.imshow(zi, cmap = 'gist_rainbow', origin='lower', interpolation = 'spline36',vmin = vmin, vmax = max(v),
                                     extent=[x.min(),x.max(),y.min(),y.max()], clip_path=poly, clip_on=True)

                    
                    ge = [e[np.where(np.array(sgp) == np.array(gp)[i])[0]][0] for i in range(len(gp))]
                    se = [e[np.where(np.array(sgp) == np.array(sp)[i])[0]][0] for i in range(len(sp))]

                    axvm.scatter(gp,ge,marker = "v", color = 'k',label = "Geophones")
                    axvm.scatter(sp, se,marker = "*", color = 'yellow',
                                 edgecolor = "k", s = 100, label = "Sources")
                    #axvm.set_ylim((-d,1))
                    #axvm.set_xlim((min(sp)-1,max(sp)+1))
                    axvm.legend(loc='best')
                    divider = make_axes_locatable(axvm)
                    cax = divider.append_axes("right", size="1%", pad=0.05)
                    plt.colorbar(cm,orientation="vertical",aspect =20,
                                 cax = cax, label = "Velocity (m/s)")
                    
                    axvm.set_xlabel("Distance (m)")
                    axvm.set_ylabel("Depth (m)")
                    axvm.set_title("Velocity model")
                    
                    axttfit = ra.showData(response = ra.inv.response())
                    ax, _ = pg.show(m, vest, label="Velocity [m/s]", cMap = plt.cm.get_cmap('gist_rainbow'))
              
                    self.editTT(axttfit, plt.gcf())
                    
                    #ax, cb = ra.showResult()
                    #axrp, crp = ra.showRayPaths(ax = axvm)
                    plt.show()
                else:
                    parFile = None
                    messagebox.showinfo('Refrainv', "Select the Time-terms analysis file for inversion's parameters.")
                    pars = ["depth", "vtop", "vbottom", "lam", "zWeight", "maxIter"]
                    try:
                        parFile = filedialog.askopenfilename(title='Open',filetypes=[("Parameters's file",'*.txt'),
                                                                            ('All files','*.*')])
                    except:
                        pass
                    
                    if parFile != None:
                        p, v = np.genfromtxt(parFile, usecols = (0,1), unpack = True, dtype='str')
                        d = ra.getDepth()
                        v1 = 300
                        v2 = 3000
                        l = 0.2
                        w = 0.2
                        mi = 10
                        rp = 0
                        sources = []
                        for i in range(len(p)):
                            if p[i] == "depth":
                                d = float(v[i])
                            elif p[i] == "vtop":
                                v1 = float(v[i])
                            elif p[i] == "vbottom":
                                v2 = float(v[i])
                            elif p[i] == "lam":
                                l = float(v[i])
                            elif p[i] == "zWeight":
                                w = float(v[i])
                            elif p[i] == "maxIter":
                                mi = float(v[i])
                            elif p[i] == "rays":
                                rp = bool(float(v[i]))
                            elif p[i] == "fg":
                                fg = float(v[i])
                            elif p[i] == "gn":
                                gn = float(v[i])
                            elif p[i] == "gs":
                                gs = float(v[i])
                            elif p[i] == "s":
                                sources.append(float(v[i]))
                        
                        m = ra.createMesh(paraMaxCellSize=5.0, secNodes=1)
                        vest = ra.invert(vtop = v1, vbottom = v2)
                        rrms = ra.inv.relrms() # relative RMS
                        arms = ra.inv.absrms() # Absolute RMS
                        x = np.array([i for i in pg.x(m.cellCenters())])
                        y = np.array([i for i in pg.y(m.cellCenters())])
                        v = np.array([i for i in vest])

                        figvm, axvm = plt.subplots()
                        x_grid = np.linspace(x.min(), x.max(), 500)
                        y_grid = np.linspace(y.min(), y.max(), 500)
                        xi,yi = np.meshgrid(x_grid,y_grid)
                        zi = scipy.interpolate.griddata((x, y), v, 
                                            (xi,yi), method='cubic')

                        cm = axvm.imshow(zi, cmap = 'gist_rainbow', origin='lower', interpolation = 'spline36',
                                         vmin = v1, vmax = v2, extent=[x.min(),x.max(),y.min(),y.max()])

                        axvm.scatter(np.arange(fg, int((gn*gs))+fg, gs),
                                      [i*0 for i in range(int(gn))],marker = "v", color = 'k',
                                         label = "Geophones")
                        axvm.scatter(sources, [i*0 for i in range(len(sources))],marker = "*", color = 'yellow',
                                     edgecolor = "k", s = 100, label = "Sources")
                        axvm.set_xlim((min(sources)-1,max(sources)+1))
                        axvm.legend(loc='best')
                        divider = make_axes_locatable(axvm)
                        cax = divider.append_axes("right", size="2%", pad=0.05)
                        plt.colorbar(cm,orientation="vertical",
                                     cax = cax, label = "Velocity (m/s)")
                        
                        axvm.set_xlabel("Distance (m)")
                        axvm.set_ylabel("Depth (m)")
                        axvm.set_title("Velocity model")
                        
                        axttfit = ra.showData(response = ra.inv.response())
                        
                        
                        ra.showResult(vtop = v1, vbottom = v2, rays = rp)
                        axrp, crp = ra.showRayPaths()
                        
                        
                        
                        
                        messagebox.showinfo('Refrainv', "Inversion completed!\nRelative RMS = %.2f%%\nAbsolute RMS = %.6f ms"%(rrms,1000*arms))
                        
                        #ra.showResult()
                        #ra.showResultAndFit(cMin = v1, cMax = v2, rays = rp)
                        plt.show()
                if messagebox.askyesno("Refrainv", "Do you want to save the results?"):
                    m.exportMidCellValue("mydata.xyz", vest)
                    ra.saveResult()
                    messagebox.showinfo('Refrainv', "Results were saved succesfully!")
                            
                                
                            
                    
                    
        

root = Tk()
Sisinv(root)
root.mainloop()
