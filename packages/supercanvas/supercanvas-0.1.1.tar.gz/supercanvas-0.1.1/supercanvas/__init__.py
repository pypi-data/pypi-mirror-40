from .supercanvas import *


if __name__ == '__main__':
    import math
    r = tkinter.Tk()
    c = supercanvas(r, bg="white", width=800, height=600,
                    axes=False,
                    ticks=False,
                    follow=False)

    c.setUnit(100, 100)
    #c.setOrigin(100,100)

    f=lambda x:math.cos(x)
    g=lambda x:math.sin(x)

    p = .1
    a, b = -3, 3
    x = a
    listePointsF = []
    listePointsG = []
    for i in range(int(1 + (b-a)/p)):
        c.drawPoint(x, f(x), fill="red", outline="red")
        listePointsF += (x, f(x))
        listePointsG += [x]+[g(x)]
        x += p

    c.drawLine(listePointsF, fill="green")
    c.drawLine(listePointsG, fill="blue", width=3)
    c.pack(expand=True)

    # force un refresh
    #c.setOrigin(400,400)

    r.bind("<q>", quit)

    tkinter.mainloop()
