#author: b8horpet

from Graphics.SurfaceCommon import Surface
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class MatplotLibSurface(Surface.SurfaceInterface):
    def __init__(self,u):
        self.updater=u
        self.fig=plt.figure()
        # theres has to be a better way
        self.scat=plt.scatter([],[])
        plt.axis([-10,10,-10,10])
        def render(tick):
            offs,sizes,colors=self.updater()
            self.scat.set_offsets(offs)
            self.scat.set_sizes([(i*58)**2 for i in sizes])
            self.scat.set_facecolors(colors)
            return self.scat,
        #self.anim=animation.FuncAnimation(self.fig,render,interval=5)
        self.anim=animation.FuncAnimation(self.fig,render,frames=60)

    def StartRender(self):
        self.fig.set_size_inches(10,10)
        self.anim.save('simulation.gif', writer='imagemagick', fps=20, dpi=50)
        #plt.show()