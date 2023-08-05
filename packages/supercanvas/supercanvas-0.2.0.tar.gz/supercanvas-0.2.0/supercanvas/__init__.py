from .supercanvas import *


if __name__ == '__main__':

    example = 5
    
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 1
    ######################################################
    ######################################################
    ######################################################
    if example==1:
        import math
        r = tkinter.Tk()
        c = supercanvas(r, bg="white", width=800, height=600,
                        axes=True,
                        ticks=True,
                        follow=True)

        c.setUnit(100, 100)
        c.setTicks(1, .5)
        #c.setOrigin(100,100)

        f=lambda x: x #(x!=0 and math.cos(x) / x) or 0
        g=lambda x:x>=0 and x**.5 or x<0 and (-x)**.5

        p = .1
        a, b = -5, 5
        x = a
        listePointsF = []
        listePointsG = []
        for i in range(round(1 + (b-a)/p)):
            c.drawPoint(x, f(x), fill="red", outline="red")
            listePointsF += (x, f(x))
            listePointsG += [x] + [g(x)]
            x += p

        c.drawLine(listePointsF, fill="green")
        c.drawLine(listePointsG, fill="blue", width=3)

        h=lambda x:math.sin(x)
        c.step = .01
        c.drawFunction(h, -math.pi, math.pi, fill="#ff00ff", width=1)


        c.pack(expand=True)
        # force un refresh
        #c.setOrigin(400,400)

        r.bind("<q>", quit)

        tkinter.mainloop()

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 2
    ######################################################
    ######################################################
    ######################################################

    elif example==2:
        import math
        r = tkinter.Tk()
        
        c = supercanvas(r, bg="#00964a")
        c.setOrigin(30, 150)
        c.setUnit(10, 80)

        f = lambda x: math.sin(x)/x
        c.step=.1
        c.drawFunction(f, c.step, 10*math.pi, width=3, fill="white")

        c.pack()
        r.bind("<q>", quit)
        tkinter.mainloop()
        
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 3
    ######################################################
    ######################################################
    ######################################################

    elif example==3:
        import math
        r = tkinter.Tk()
        
        c = supercanvas(r, bg="red", width=500, height=500)
        c.setOrigin(100, 250)
        c.setUnit(150, 150)

        x = lambda t: 2 * (1 - t ** 2) / (1 + t ** 2) ** 2
        y = lambda t: 4 * t / (1 + t ** 2) ** 2
        c.step=.001
        c.drawParam(x, y, -10, 10, width=3, fill="white")

        c.pack()
        r.bind("<q>", quit)
        tkinter.mainloop()
        
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 4
    ######################################################
    ######################################################
    ######################################################

    elif example==4:
        w = beginMagicTk()

        c = supercanvas(w, bg="white")
        c.setUnit(100, 20)
        c.setTicks(.5, 2)

        f=lambda x: x**3
        c.step=.1
        c.drawFunction(f, -3, 3)

        endMagicTk(w)
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 5
    ######################################################
    ######################################################
    ######################################################

    elif example==5:
        import math
        w = beginMagicTk()

        c = supercanvas(w, bg="white", ticks=False)
        c.setUnit(100, 100)
        
        f=lambda x: math.cos(x)
        g=lambda x: math.sin(x)
        c.step = .01
        c.drawParam(f, g, 0, 2 * math.pi)

        endMagicTk(w)
    
