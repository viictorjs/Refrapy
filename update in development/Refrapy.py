from matplotlib import pyplot as plt
import os                                                                              
import numpy as np
import sys
import random
from scipy.interpolate import interp1d, griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial import ConvexHull
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import warnings
from obspy import read

warnings.filterwarnings('ignore')

class Refrapy(object):
    def __init__(self):
        print("You're using Refrapy: a Python software for refraction analysis\n")

    class SeisView(object):
        def __init__(self):
            print("You're using SeisView!\n")
            
        def firstBreaks(self, files, fmt, sColor = "k"):
            print(len(files))
            for i in range(len(files)):
                self.gain = 1
                st = read(files[i])
                if fmt == "SEG2":
                    dx = float(st[1].stats.seg2['RECEIVER_LOCATION']) - float(st[0].stats.seg2['RECEIVER_LOCATION'])
                    fg = float(st[0].stats.seg2['RECEIVER_LOCATION'])
                    dt = 1/st[0].stats.sampling_rate

                for j in range(len(st)):
                    st[j].stats.distance = (fg+(j*dx))*1000
                gp = [fg+(j*dx) for j in range(len(st))]
                fig, ax = plt.subplots()
                st.plot(type = "section", fillcolors  = (None, sColor),
                        time_down = True, fig = fig, scale = self.gain)
                ax.set_title(files[i])
                ax.set_xlabel("Distance [m]")
                
                def onkey(event):
                    if event.key == "right":
                        self.gain += 1
                        ax.cla()
                        st.plot(type = "section", fillcolors  = (None, sColor),
                        time_down = True, fig = fig, scale = self.gain)
                        fig.canvas.draw()
                    elif event.key == "left":
                        self.gain -= 1
                        ax.cla()
                        st.plot(type = "section", fillcolors  = (None, sColor),
                        time_down = True, fig = fig, scale = self.gain)
                        fig.canvas.draw()

                #event = fig.canvas.mpl_connect('pick_event', onpick)
                #event2 = fig.canvas.mpl_connect('button_release_event', onrelease)
                keyConn = fig.canvas.mpl_connect('key_press_event', onkey)
            
            plt.show()

    class Inversion(object):
        def __init__(self):
            print("You're using Sisinv!\n")

        def editTT(self, in_ttFile, out_ttFile, ax = None, fig = None):
            print('''
            Editing travel-time curves function is on use now!
            Drag and drop the circles to edit travel-times.
            Press "D" when done to save a new .rp file.
            ''')
            x, t = np.genfromtxt(in_ttFile, usecols = (0,1), unpack = True)
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
            
            if ax == None and fig == None:
                fig, ax = plt.subplots()
                
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
                    with open(out_ttFile,'w') as arqpck:
                        arqpck.write("%d %d\n%.2f %.2f\n"%(len(sp),gn,fg,gs))
                        for i in range(len(sp)):
                            for j in range(len(datax[i][sp[i]])):
                                arqpck.write('%f %f 1\n'%(datax[i][sp[i]][j],datat[i][sp[i]][j]*1000))
                            arqpck.write('/ %f\n'%sp[i])
                    print("%s was saved!"%out_ttFile)
                    plt.close('all')

            event = fig.canvas.mpl_connect('pick_event', onpick)
            event2 = fig.canvas.mpl_connect('button_release_event', onrelease)
            event3 = fig.canvas.mpl_connect('key_press_event', onkey)
            plt.legend(loc="best")
            plt.show()

        def pgTomo(self, in_sgtFile, pltG = False, pltS = False, cMap = "gist_rainbow", showTT = False,
                   in_ttFile = None, out_ttFile = None, modelTT = False, showRP = False, triangularMesh = False,
                   zw = None, lam = None, vel = None, save = None):
            
            from pygimli.physics import Refraction
            import pygimli as pg
            
            a = np.genfromtxt(in_sgtFile, usecols = (0), unpack = True)
            with open(in_sgtFile) as f:
                head = [next(f).split() for x in range(2+int(a[0]))][2:]
            
            data = pg.DataContainer(in_sgtFile, 's g')
            ra = Refraction(data)
            m = ra.createMesh(paraMaxCellSize=5.0, secNodes=1)
            if vel:  
                vest = ra.invert(vTop = vel[0], vBottom = vel[1])
            else:
                vest = ra.invert()
            rrms = ra.inv.relrms() # relative RMS
            arms = ra.inv.absrms() # Absolute RMS
            print("Relative RMS = %.2f%%\nAbsolute RMS = %.6f ms"%(rrms,1000*arms))
            x = np.array([i for i in pg.x(m.cellCenters())])
            y = np.array([i for i in pg.y(m.cellCenters())])
            v = np.array([i for i in vest])
            spi = np.unique(ra.dataContainer("s"), return_inverse=False)
            gi = np.unique(ra.dataContainer("g"), return_inverse=False)
            a = np.genfromtxt(in_sgtFile, usecols = (0), skip_header = 2, unpack = True)
            sp = [a[:len(spi)+len(gi)][int(i)] for i in spi]
            gp = [a[:len(spi)+len(gi)][int(i)] for i in gi]

            if triangularMesh:
                ax, _ = pg.show(m, vest, label="Velocity [m/s]", cMap = plt.cm.get_cmap('gist_rainbow'))
                if pltG:
                    ax.scatter(gp,ge,marker = "v", color = 'k',label = "Geophones")
                    ax.legend(loc='best')
                if pltS:
                    ax.scatter(sp, se,marker = "*", color = 'yellow',edgecolor = "k", s = 100, label = "Sources")
                    ax.legend(loc='best')
                if showRP:
                    ra.showRayPaths(ax = ax)
            else:
                figvm, axvm = plt.subplots()
                x_grid = np.linspace(x.min(), x.max(), 500)
                y_grid = np.linspace(y.min(), y.max(), 500)
                xi,yi = np.meshgrid(x_grid,y_grid)
                zi = griddata((x, y), v, 
                                    (xi,yi), method='cubic')
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
                axvm.add_patch(poly)
                cm = axvm.imshow(zi, cmap = cMap, origin='lower', interpolation = 'spline36',
                                 vmin = vmin, vmax = max(v),
                                 extent=[x.min(),x.max(),y.min(),y.max()], clip_path=poly, clip_on=True)
                ge = [e[np.where(np.array(sgp) == np.array(gp)[i])[0]][0] for i in range(len(gp))]
                se = [e[np.where(np.array(sgp) == np.array(sp)[i])[0]][0] for i in range(len(sp))]
                if pltG:
                    axvm.scatter(gp,ge,marker = "v", color = 'k',label = "Geophones")
                    axvm.legend(loc='best')
                if pltS:
                    axvm.scatter(sp, se,marker = "*", color = 'yellow',edgecolor = "k", s = 100, label = "Sources")
                    axvm.legend(loc='best')
                if showRP:
                    ra.showRayPaths(ax = axvm)

                divider = make_axes_locatable(axvm)
                cax = divider.append_axes("right", size="1%", pad=0.05)
                plt.colorbar(cm,orientation="vertical",aspect =20,
                             cax = cax, label = "Velocity (m/s)")
                
                axvm.set_xlabel("Distance (m)")
                axvm.set_ylabel("Depth (m)")
                axvm.set_title("Velocity model")
                
            if showTT:
                axttfit = ra.showData(response = ra.inv.response())
                if in_ttFile and out_ttFile:
                    self.editTT(in_ttFile, out_ttFile, ax = axttfit, fig = plt.gcf())
                
            plt.show()
    
        def createSGT(self, in_ttFile, out_sgtFile, in_topoFile = None):
            
            if in_topoFile:
                p, e = np.loadtxt(in_topoFile, usecols = (0,1), unpack = True)
                                    
            x, t = np.genfromtxt(in_ttFile, usecols = (0,1), unpack = True)
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

            with open(out_sgtFile, "w") as f:
                f.write("%d # shot/geophone points\n#x y\n"%(gn+len(sp)))
                for i in range(len(sgp)):
                    if in_topoFile:
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
            print('The %s file has been created succesfully!'%out_sgtFile)

        def timeterms(self, in_ttFIle, in_topoFile = None, rs = 0.1, pltG = False, pltS = False,
               cL1 = "red", cL2 = "green", cL3 = "blue", save = False):
            print('''
            Time-terms analysis is now on use!
            To assigner layers, click on the circles.
            Use keys 1, 2 and 3 to switch between layers.
            Press "C" to clear all assignments.
            Press "I" when done to run inversion!
            ''')
            x, t = np.genfromtxt(in_ttFIle, usecols = (0,1), unpack = True)
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
            fig, ax = plt.subplots()
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

            def solve(layer, G, d, w):
                rMs = np.zeros((int(len(layer)), int(len(sp)+gn+1)))
                r = 0
                for i in range(len(gp)):
                    for j in range(len(sp)):
                        if  sp[j] > min(gp) and sp[j] < max(gp): #se for fonte intermediaria                       
                            if gp[i]+gs >= sp[j] and gp[i]-gs <= sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(sp)+i] = -w
                                r += 1
                        elif sp[j] <= min(gp):
                            if gp[i]-gs <= sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(sp)+i] = -w
                                r += 1
                        elif sp[j] >= max(gp):
                            if gp[i]+gs >= sp[j]:
                                rMs[r][j] = w
                                rMs[r][len(sp)+i] = -w
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
                    if self.layer1:
                        d1 = np.array([self.layer1[i][1] for i in range(len(self.layer1))])
                        G1 = np.array([self.layer1[i][3] for i in range(len(self.layer1))])
                        G1 = np.reshape(G1, (len(G1),1))
                        sol_layer1, res1, rank1, sv1 = np.linalg.lstsq(G1, d1)
                        v1 = 1000/sol_layer1[0] #m/s
                        rms1 = np.sqrt(res1/len(sol_layer1))
                        fvm, axvm = plt.subplots()
                        if in_topoFile != None:
                            p, e = np.loadtxt(in_topoFile, usecols = (0,1), unpack = True)
                            ge = [e[np.where(np.array(p) == np.array(gp)[i])[0]][0] for i in range(len(gp))]
                            se = [e[np.where(np.array(p) == np.array(sp)[i])[0]][0] for i in range(len(sp))]
                            axvm.set_ylabel("Elevation (m)")

                        if self.layer2:
                            d2 = np.array([self.layer2[i][1] for i in range(len(self.layer2))])
                            G2 = np.zeros((int(len(self.layer2)),
                                           int(len(sp)+gn+1)))

                            for i in range(len(self.layer2)):
                                G2[i][self.layer2[i][-2]] = 1
                                G2[i][self.layer2[i][-1]+len(sp)] = 1
                                G2[i][-1] = self.layer2[i][-3]

                            sol_layer2, sse = solve(self.layer2, G2, d2, rs)
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
           
                            sol_layer3, sse = solve(self.layer3, G3, d3, rs)
                            v3 = 1000/sol_layer3[-1] #m/s
                            rms3 = np.sqrt(sse/len(sol_layer3))
                            rmsMed = (rms2+rms3)/2

                        
                        axvm.grid(lw = .5, ls = "-", color = "grey", alpha = .35)
                        axvm.set_title(label='Velocity model')
                        axvm.set_xlabel("Distance (m)")
                        plt.gca().set_aspect('equal', adjustable='box')
                        sgp = np.sort(np.concatenate((np.arange(fg,fg+gn*gs,gs),np.array(sp))))
                        if self.layer1 and self.layer2 and not self.layer3:
                            
                            dtg = np.array([i for i in sol_layer2[:-1]]) #delay-time of all geophones
                            if in_topoFile != None:
                                dlayer2 = e-((dtg*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000)
                                
                                try:
                                    f = interp1d(p, dlayer2, kind = 'cubic', fill_value='extrapolate')
                                    sdlayer2 = f(np.linspace(p[0], p[-1], 1000))
                                    f = interp1d(p, e, kind = 'cubic', fill_value='extrapolate')
                                    s_surf = f(np.linspace(p[0], p[-1], 1000))
                                    axvm.fill_between(np.linspace(p[0], p[-1], 1000),sdlayer2,s_surf, color = cL1,
                                                      alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                                    axvm.fill_between(np.linspace(p[0], p[-1], 1000),sdlayer2, min(sdlayer2)*0.99,
                                                      alpha = .5,edgecolor = "k", color = cL2,
                                                      label = "%.0f m/s"%v2)
                                except:
                                    axvm.fill_between(sgp,dlayer2,e, color = cL1, alpha = .5,edgecolor = "k",
                                                      label = "%.0f m/s"%v1)
                                    axvm.fill_between(sgp,dlayer2, min(dlayer2)*0.99, alpha = .5,edgecolor = "k",
                                                      color = cL2, label = "%.0f m/s"%v2)
                            else:
                                dlayer2 = -1*(dtg*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000
                                axvm.set_ylabel("Depth (m)")
                                try:
                                    f = interp1d(sgp, dlayer2, kind = 'cubic', fill_value='extrapolate')
                                    sdlayer2 = f(np.linspace(sgp[0], sgp[-1], 1000))
                                    axvm.fill_between(np.linspace(sgp[0], sgp[-1], 1000),
                                                      sdlayer2,0, color = cL1, alpha = .5,edgecolor = "k",
                                                      label = "%.0f m/s"%v1)
                                    axvm.fill_between(np.linspace(sgp[0], sgp[-1], 1000), sdlayer2,
                                                      min(sdlayer2)*1.1, alpha = .5,edgecolor = "k", color = cL2,
                                                      label = "%.0f m/s"%v2)
                                except:
                                    axvm.fill_between(sgp,dlayer2,0, color = cL1, alpha = .5,edgecolor = "k",
                                                      label = "%.0f m/s"%v1)
                                    axvm.fill_between(sgp,dlayer2, min(dlayer2)*1.1, alpha = .5,edgecolor = "k",
                                                      color = cL2, label = "%.0f m/s"%v2)
                            if pltG:
                                axvm.scatter(np.arange(fg, int((gn*gs))+fg, gs),
                                          [i*0 for i in range(int(gn))],marker = 7, color = 'k',
                                             label = "Geophones")
                            if pltS:
                                axvm.scatter(sp, [i*0 for i in range(len(sp))],marker = "*", color = 'yellow',
                                         edgecolor = "k", s = 100, label = "Sources")
                            axvm.legend(loc='best')
                            #axvm.set_ylim((min(sdlayer2)*1.1-5,5))
                            print('Velocity model was created!')
                            print('RMS = %.5f ms'%rms2)
                            plt.show()
                                    
                        elif self.layer1 and self.layer2 and self.layer3:
                            dtg2 = np.array([i for i in sol_layer2[:-1]]) #delay-time of all geophones
                            dtg3 = np.array([i for i in sol_layer3[:-1]]) #delay-time of all geophones
                            upvmed = (v1+v2)/2
                            if in_topoFile != None:
                                dlayer2 = e-((dtg2*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000)
                                dlayer3 = e-((dtg3*upvmed*v3)/(np.sqrt((v3**2)-(upvmed**2)))/1000)
                                try:
                                    s_surf = f(np.linspace(p[0], p[-1], 1000))
                                    f2 = interp1d(np.arange(fg, (gn*gs)+fg, gs), dlayer2, kind = 'cubic', fill_value='extrapolate')
                                    sdlayer2 = f2(np.linspace(fg, fg+(gn*gs)-gs, 1000))
                                    f3 = interp1d(np.arange(fg, (gn*gs)+fg, gs), dlayer3, kind = 'cubic', fill_value='extrapolate')
                                    sdlayer3 = f3(np.linspace(fg, fg+(gn*gs)-gs, 1000))
                                    axvm.fill_between(np.linspace(p[0], p[-1], 1000),sdlayer2,s_surf, color = cL1,
                                                      alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                                    axvm.fill_between(np.linspace(p[0], p[-1], 1000),sdlayer2, sdlayer3, alpha = .5,
                                                      edgecolor = "k", color = cL2, label = "%.0f m/s"%v2)
                                    axvm.fill_between(np.linspace(p[0], p[-1], 1000),sdlayer3, min(sdlayer3)*1.1,
                                                      alpha = .5,edgecolor = "k", color = cL3,
                                                      label = "%.0f m/s"%v3)
                                except:
                                    axvm.fill_between(sgp,dlayer2,e, color = cL1, alpha = .5,edgecolor = "k",
                                                      label = "%.0f m/s"%v1)
                                    axvm.fill_between(sgp,dlayer2, dlayer3, alpha = .5,edgecolor = "k", color = cL2,
                                                      label = "%.0f m/s"%v2)
                                    axvm.fill_between(sgp,dlayer3, min(dlayer3)*1.1, alpha = .5,edgecolor = "k",
                                                      color = cL3, label = "%.0f m/s"%v3)

                            else:
                                dlayer2 = -1*(dtg2*v1*v2)/(np.sqrt((v2**2)-(v1**2)))/1000
                                dlayer3 = -1*(dtg3*upvmed*v3)/(np.sqrt((v3**2)-(upvmed**2)))/1000
                                
                                try:
                                    f2 = interp1d(sgp, dlayer2, kind = 'cubic',fill_value='extrapolate')
                                    sdlayer2 = f2(np.linspace(sgp[0], sgp[-1], 1000))
                                    f3 = interp1d(sgp, dlayer3, kind = 'cubic',fill_value='extrapolate')
                                    sdlayer3 = f3(np.linspace(sgp[0], sgp[-1], 1000))
                                    axvm.fill_between(np.linspace(fg, fg+(gn*gs)-gs, 1000),sdlayer2,0, color = cL1,
                                                      alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                                    axvm.fill_between(np.linspace(fg, fg+(gn*gs)-gs, 1000),
                                                      sdlayer2, sdlayer3, alpha = .5,edgecolor = "k",
                                                      color = cL2, label = "%.0f m/s"%v2)
                                    axvm.fill_between(np.linspace(fg, fg+(gn*gs)-gs, 1000),sdlayer3,
                                                      min(sdlayer3)*1.1, alpha = .5,edgecolor = "k", color = cL3,
                                                      label = "%.0f m/s"%v3)
                                except:
                                    axvm.fill_between(sgp,dlayer2,0, color = cL1, alpha = .5,edgecolor = "k",
                                                      label = "%.0f m/s"%v1)
                                    axvm.fill_between(sgp,dlayer2, dlayer3, alpha = .5,edgecolor = "k",
                                                      color = cL2, label = "%.0f m/s"%v2)
                                    axvm.fill_between(sgp,dlayer3, min(dlayer3)*1.1, alpha = .5,edgecolor = "k",
                                                      color = cL3,label = "%.0f m/s"%v3)
                                
                            if pltG:
                                axvm.scatter(np.arange(fg, int((gn*gs))+fg, gs),
                                          [i*0 for i in range(int(gn))],marker = 7, color = 'k',
                                             label = "Geophones")
                            if pltS:
                                axvm.scatter(sp, [i*0 for i in range(len(sp))],marker = "*", color = 'yellow',
                                         edgecolor = "k", s = 100, label = "Sources")
                            axvm.legend(loc='best')
                            #axvm.set_ylim((min(sdlayer3)*1.1-5,5))
                            print('RMS = %.5f ms'%rmsMed)
                            print('Velocity model was created!')
                            plt.show()

                        if save:
                            fvm.savefig('timeterm_vm.png', dpi=fvm.dpi)
                            with open('timeterm_vm.txt', "w") as arq:
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
                            print('Time-term analysis was saved succesfully!')
                    else:
                        messagebox.showinfo('Refrainv', 'To invert data you must interpret at least direct wave arrivals!')

                fig.canvas.draw()

            event = fig.canvas.mpl_connect('pick_event', onpick)
            event2 = fig.canvas.mpl_connect('key_press_event', onkey)
            
            plt.show()

rp = Refrapy()
inv = rp.Inversion()
#inv.editTT("2012_edit.rp", "2012_edit2.rp")
#inv.timeterms(in_ttFIle = "3cam.rp", in_topoFile = "topo_3cam.txt")
#inv.timeterms(in_ttFIle = "2012.rp", in_topoFile = "topo_2012.txt")
#inv.createSGT("2012.rp", "2012.sgt", in_topoFile = "topo_2012.txt")
#inv.pgTomo("2012.sgt", showTT = True, showRP = True, in_ttFile = "2012.rp", out_ttFile = "2012_edit.rp",
#           triangularMesh = True)

viewer = rp.SeisView()
viewer.firstBreaks(files = ["2001.dat","2002.dat"], fmt = "SEG2")


              
