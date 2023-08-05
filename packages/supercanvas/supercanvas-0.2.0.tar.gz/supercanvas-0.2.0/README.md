This package provides a `supercanvas` widget based on the original
`tkinter` canvas.  It provides a quickly useable canvas with a
usual cartesian coordinate system.

If you just want to have this `supercanvas` alone with no other
widget, see `magicTk` section at the end.

### class object

``` python3

>>> from supercanvas import *

```

Once package importation completed, you have to create a
supercanvas the usual way.

``` python3

r = tkinter.Tk()
c = supercanvas(r, bg="white", width=800, height=600)

```


### origin and units

By default, origin is located at `supercanvas`'s center and units
are both 1 pixel (and axes are drawn in french style with
arrows). You can change this with `setOrigin` and `setUnit`
methods:

 
``` python3

c.setUnit(80, 100)
c.setOrigin(50, 200)

```


### axes and ticks

By default, axes and ticks are shown/drawn. If you want them not to appear, you pass options `axes` and/or `ticks` to `False` in the `supercanvas` command.

Or you can these variables to `False` into your script. 


`setTicks` method allow you to set distance between ticks.


``` python3

c.axes = False
c.setTicks(1, .5)

```

For the moment, ticks come with texts.


### supercanvas items

`supercanvas` provides four drawing methods `drawPoint`, `drawLine`, `drawFunction` and `drawParam`.


* `drawPoint` method create a point at the desired coords.

``` python3

f = lambda x:x**2
x = 3
c.drawPoint(x, f(x), fill="red", outline="red")

```

It's based on `create_oval` so you can pass each option related to
`Oval` object.

* `drawLine` method create a line with a list of coords.

``` python3

c.drawLine([(-2, 2), (-1, 0), (0, 3)], fill="blue", width=3)

```

`drawLine` also supports a flat list of coords:

``` python3

c.drawLine([-2, 2, -1, 0, 0, 3], fill="blue", width=3)

```

gives the same line.


* `drawFunction` methode create a line representing a function passed.


``` python3

f = lambda x: 3 * x ** 1.2 + 2 
c.drawLine(f, -2, 7, fill="green")

```

-2 and 7 are the lower and upper values of argumentt's function.

You can use `step` method to specify difference between two
consecutive argguments, default is 1.


``` python3

f = lambda x: 3 * x ** 1.2 + 2
c.step = .1
c.drawLine(f, -2, 7, fill="green")

```


*  `drawParam` methode create a line representing a parametric curve.


this code create a unit circle:


``` python3

f = lambda x: math.cos(x)
g = lambda x: math.sin(x)
c.step = .01
c.drawParam(f, g, 0, 2 * math.pi)

```


### grab/release background

You can move the whole `supercanvas` content in grabing /
realeasing the background. It will refresh coords.

### `supercanvas` options

* `axes`

passing `axes=False` to `supercanvas` options disable axes, default
is `True`. For the moment, you cannot change axes style...

* `ticks`

passing `ticks=False` to `supercanvas` options disable ticks, default is `True`.

* `follow` 

passing `follow=False` to `supercanvas` options disable cursor follow with coords, default is `True`.


### full examples

* example 1

Points and functions using `drawPoint` and `drawLine`.


``` python3

from supercanvas import *
import math
r = tkinter.Tk()

c = supercanvas(r, bg="white", width=800, height=600, ticks=False)
c.setUnit(100, 100)

f=lambda x:math.cos(x)
g=lambda x:math.sin(x)

p = .1
a, b = -3, 3
x = a
listePointsF = []
listePointsG = []
for i in range(int(1 + (b - a) / p)):
    # creating points 
    c.drawPoint(x, f(x), fill="red", outline="red")
    # two lists
    # function f with tuples
    listePointsF += (x, f(x))
    # function g with flat list
    listePointsG += [x]+[g(x)]
    x += p

# drawings of the two curves
c.drawLine(listePointsF, fill="green")
c.drawLine(listePointsG, fill="blue", width=3)

# balancing canvas on the root
c.pack(expand=True)

# q to quit
r.bind("<q>", quit)
tkinter.mainloop()

```


* example 2

Function using `drawFunction`.

``` python3

from supercanvas import *
import math
r = tkinter.Tk()

c = supercanvas(r, bg="#00964a")
c.setOrigin(30, 150)
c.setUnit(10, 80)

f = lambda x: math.sin(x) / x
c.step=.1
c.drawFunction(f, c.step, 10*math.pi, width=3, fill="white")

c.pack()
r.bind("<q>", quit)
tkinter.mainloop()

```

* example 3

Cardioid curve using `drawParam`

``` python3

from supercanvas import *
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


```


### magicTk

Because remembering `tkinter` commands for just one widget is
awful, `supercanvas` provides two commands `beginMagicTk` and
`endMagicTk`.

Key `q` is bind to close/exit event.

Here's how to use them in a standalone example file:

``` python3

from supercanvas import *
w = beginMagicTk()

c = supercanvas(w, bg="white")
c.setUnit(100, 20)
c.setTicks(.5, 2)

f = lambda x: x ** 3
c.step=.1
c.drawFunction(f, -3, 3)

endMagicTk(w)

```

Assign first command output, use it in `supercanvas` and
`endMagicTk` commands.


### further

Much much more!


### about

supercanvas is rather an attempt to publish on the `PyPi` packages
index than a fully completed python project, I do not recommend
supercanvas usage for professionnal use. You have to consider this
package as an experiment.
