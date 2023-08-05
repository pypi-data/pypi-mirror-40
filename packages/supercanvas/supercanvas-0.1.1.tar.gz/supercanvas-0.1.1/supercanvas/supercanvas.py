# auteur : david cobac
# Début 27/12/2018
import tkinter

class supercanvas(tkinter.Canvas):
    def __init__(self, master, **options):
        #########################
        # traitement des options
        # valeurs par défaut
        self.axes   = True
        self.ticks  = True
        self.follow = True
        # parsing de ce qui a été passé à l'appel
        aSupprimer = []
        for k, v in options.items():
            if k=="axes":
                self.axes = v
                aSupprimer.append("axes")
            elif k=="ticks":
                self.ticks = v
                aSupprimer.append("ticks")
            elif k=="follow":
                self.follow = v
                aSupprimer.append("follow")
        # suppression des options particulières
        # pour permettre de passer le reste au canvas pur
        for option in aSupprimer:
            del options[option]
        #########################
        tkinter.Canvas.__init__(self, master, **options)
        #########################
        self.width, self.height  = map(int, self.getDim())
        self.x_origin = self.width / 2
        self.y_origin = self.height / 2
        self.x_unit   = 1
        self.y_unit   = 1
        ########################
        # tableau des coordonnées passées en arg. de tous
        # les objets créés (sauf axes)
        self.coordsInit = {}
        ########################
        self.drawAxes()
        ########################
        self.event_add("<<Suivi>>", "<Motion>")
        self.bind('<Configure>', self.refresh)
        self.bind('<<Suivi>>', self.followCursor)
        self.bind('<1>', self.savePosition)
        self.bind('<B1-Motion>', self.translation)
        self.bind('<ButtonRelease-1>', self.landing)
        
    def setOrigin(self, x, y):
        self.x_origin_sv = self.x_origin
        self.y_origin_sv = self.y_origin
        self.x_origin = x
        self.y_origin = y
        self.refresh()

    def getOrigin(self):
        return [self.x_origin, self.y_origin]

    def setUnit(self, x, y):
        self.x_unit_sv = self.x_unit
        self.y_unit_sv = self.y_unit
        self.x_unit = x
        self.y_unit = y
        self.refresh()

    def getUnit(self):
        return [self.x_unit, self.y_unit]

    def setDim(self, x, y):
        self.configure(width=x, height=y)
    
    def getDim(self):
        return [self.cget("width"), self.cget("height")]

    ############################################
    ############################################

    def refresh(self, *args):
        self.width, self.height  = map(int, self.getDim())
        self.drawAxes()
        self.drawTicks()
        for objet in self.find_all():
            if "axes" not in self.gettags(objet) \
               and "suivi" not in self.gettags(objet) \
               and "ticks" not in self.gettags(objet):
                # coords (liste)
                c = self.coords(objet)
                # type (type)
                t = self.type(objet)
                # style (dictionnaire)
                s = self.itemconfigure(objet)
                if t=="oval":
                    epaisseur = 1
                    liste = []
                    x, y = self.coordsInit[objet]
                    x, y = self.__coordsCal2Can__(x, y)
                    liste.append(x-epaisseur)
                    liste.append(y-epaisseur)
                    liste.append(x+epaisseur)
                    liste.append(y+epaisseur)
                    self.coords(objet, liste)
                elif t=="line":
                    liste = []
                    it = iter(self.coordsInit[objet])
                    for x in it:
                        x, y = self.__coordsCal2Can__(x, next(it))
                        liste.append(x)
                        liste.append(y)
                    self.coords(objet, liste)
                else:
                    pass

    #############################################
    #############################################

    # https://stackoverflow.com/questions/8131942/how-to-pass-a-default-argument-value-of-an-instance-member-to-a-method
    
    def __coordsCan2Cal__(self, x, y,
                          xo=None, yo=None,
                          xu=None, yu=None):
        xo = xo if xo is not None else self.x_origin
        yo = yo if yo is not None else self.y_origin
        xu = xu if xu is not None else self.x_unit
        yu = yu if yu is not None else self.y_unit
        #        
        x = (x - xo) / xu
        y = (yo - y) / yu
        return [x, y]

    def __coordsCal2Can__(self, x, y,
                          xo=None, yo=None,
                          xu=None, yu=None):
        xo = xo if xo is not None else self.x_origin
        yo = yo if yo is not None else self.y_origin
        xu = xu if xu is not None else self.x_unit
        yu = yu if yu is not None else self.y_unit
        #        
        x = x * xu + xo
        y = - y * yu + yo
        return [x, y]

    #############################################
    #############################################

    def followCursor(self, event):
        self.delete("suivi")
        if not self.follow: return
        x, y = event.x, event.y
        self.create_line(0, y, self.width, y, tags="suivi", dash=(2, 5))
        self.create_line(x, 0, x, self.height, tags="suivi", dash=(2,5))
        xc, yc = self.__coordsCan2Cal__(x, y)
        self.create_text(x, y, anchor='sw',
                         text="({:<0.2f};{:<0.2f})".format(xc, yc), tags="suivi")

    def savePosition(self, event):
        # init va servir à savoir comment globalement
        # on a bougé une fois qu'on a relâché
        self.initx, self.inity = event.x, event.y
        # pos pour la translation petit à petit
        self.posx, self.posy = event.x, event.y

    def translation(self, event):
        x, y = event.x, event.y
        self.move('all', x - self.posx, y - self.posy)
        self.posx, self.posy = x, y

    def landing(self, event):
        x, y = event.x, event.y
        xo, yo = self.getOrigin()
        self.setOrigin(xo + x - self.initx, yo + y - self.inity)
        self.refresh()

    #############################################
    #############################################

    def drawAxes(self, **options):
        self.delete("axes")
        if self.axes:
            self.create_line(0, self.y_origin,
                             self.width, self.y_origin,
                             tags="axes", arrow=tkinter.LAST,
                             width=2,
                             **options)
            self.create_line(self.x_origin, self.height,
                             self.x_origin, 0,
                             tags="axes", arrow=tkinter.LAST,
                             width=2,
                             **options)

    def drawTicks(self, dx=1, dy=1, **options):
        self.delete("ticks")
        #
        if not self.ticks: return
        #
        eloignement = 2
        #
        # absc. positives
        i = 1
        o1 = self.y_origin + eloignement
        o2 = self.y_origin - eloignement
        while self.x_unit * i * dx <= self.width - self.x_origin:
            a = self.x_origin + self.x_unit * i * dx
            self.create_line(a, o1, a, o2,
                             tags="ticks",
                             width=2,
                             **options)
            i += 1

        # abs. negatives
        i = 1
        o1 = self.y_origin + eloignement
        o2 = self.y_origin - eloignement
        while self.x_unit * i * dx <= self.x_origin:
            a = self.x_origin - self.x_unit * i * dx
            self.create_line(a, o1, a, o2,
                             tags="ticks",
                             width=2,
                             **options)
            i += 1

        # ord. positives
        i = 1
        a1 = self.x_origin + eloignement
        a2 = self.x_origin - eloignement
        while self.y_unit * i * dy <= self.y_origin:
            o = self.y_origin - self.y_unit * i * dy
            self.create_line(a1, o, a2, o,
                             tags="ticks",
                             width=2,
                             **options)
            i += 1

        # ord. negatives
        i = 1
        a1 = self.x_origin + eloignement
        a2 = self.x_origin - eloignement
        while self.y_unit * i * dx <= self.height - self.y_origin:
            o = self.y_origin + self.y_unit * i * dy
            self.create_line(a1, o, a2, o,
                             tags="ticks",
                             width=2,
                             **options)
            i += 1

    #############################################
    #############################################

    def drawPoint(self, x, y, **options):
        epaisseur = 1
        xcan, ycan = self.__coordsCal2Can__(x, y)
        id = self.create_oval(xcan - epaisseur, ycan - epaisseur,
                         xcan + epaisseur, ycan + epaisseur,
                         tags="point", **options)
        self.coordsInit[id] = [x, y]

    def drawLine(self, listeXY, **options):
        # si la liste est un composée de tuples,
        # on l'aplatit
        if type(listeXY[0])==tuple:
            l = []
            for x, y in listeXY:
                l.append(x)
                l.append(y)
            listeXY = l
        liste = []
        if len(listeXY) % 2 != 0:
            print("Please check coords list in drawLine method!")
        else:  
            # https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
            it = iter(listeXY)
            for x in it:
                x, y = self.__coordsCal2Can__(x, next(it)) 
                liste.append(x)
                liste.append(y)
            id = self.create_line(*liste, tags="line", join="round", cap="round", **options)
            self.coordsInit[id] = listeXY

