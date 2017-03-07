#author: b8horpet

from Graphics.SurfaceCommon import Surface
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptchs
import matplotlib.animation as animation

class MatplotLibSurface(Surface.SurfaceInterface):
    def __init__(self,u,d=None):
        self.updater=u
        self.debugger=d
        self.fig=plt.figure()
        # theres has to be a better way
        self.ax=self.fig.add_subplot(111);
        plt.axis([-25,25,-25,25])
        def render(tick):
            for i in reversed(range(len(self.ax.patches))):
                del self.ax.patches[i]
            offs,sizes,colors,text=self.updater()
            for i in range(len(offs)):
                self.ax.add_patch(ptchs.Circle(offs[i],sizes[i],color=colors[i]))
            if self.debugger is not None:
                ps=self.debugger()
                for p in ps:
                    self.ax.add_patch(ptchs.Rectangle((p[0],p[1]),p[2]-p[0],p[3]-p[1],fill=False))
            return self.ax.patches,
        #self.anim=animation.FuncAnimation(self.fig,render,interval=5)
        self.anim=animation.FuncAnimation(self.fig,render,frames=20*60,blit=False)

    def StartRender(self):
        self.fig.set_size_inches(25,25)
        #Writer = animation.writers['avconv']
        #writer = Writer(fps=20, metadata=dict(artist='b8horpet'), bitrate=-1)
        #self.anim.save('simulation.mp4', writer=writer)
        plt.show()