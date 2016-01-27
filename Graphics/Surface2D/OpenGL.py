#author: b8horpet

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Graphics.SurfaceCommon import Surface
import numpy as np
from enum import  Enum
import sys
from Physics.Basics import Vector2D
import datetime


class Keys(Enum):
    Escape = b'\x1b'
    Up = b'w'
    Down = b's'
    Left = b'a'
    Right = b'd'
    ZoomIn = b'+'
    ZoomOut = b'-'


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, float(Width)/float(Height), 0.1, 1000.0)

    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:
            Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def foo():
    pass


class OpenGL2DSurface(Surface.SurfaceInterface):
    def __init__(self,u):
        self.window=0
        self.updater=u
        self.scale=1.0
        self.dist=10
        self.shift=Vector2D()
        self.Width=640
        self.Height=480
        self.TimeMS=20
        now=datetime.datetime.now()
        self.LastRender=[now for i in range(0,10)]
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.Width, self.Height)
        glutInitWindowPosition(0, 0)
        self.window = glutCreateWindow(b"Genesis")
        #glutDisplayFunc(Surface.memberfunctor(self, OpenGL2DSurface.DrawGLScene))
        #glutFullScreen()
        #glutIdleFunc(Surface.memberfunctor(self, OpenGL2DSurface.DrawGLScene))
        glutReshapeFunc(ReSizeGLScene)
        glutKeyboardFunc(Surface.memberfunctor(self,OpenGL2DSurface.keyPressed))
        InitGL(self.Width, self.Height)

    def StartRender(self):
        glutTimerFunc(self.TimeMS,Surface.memberfunctor(self, OpenGL2DSurface.DrawGLScene),0)
        glutMainLoop()

    def DrawGLScene(self,*args,**kwargs):
        glutTimerFunc(self.TimeMS,Surface.memberfunctor(self, OpenGL2DSurface.DrawGLScene),0)
        now=datetime.datetime.now()
        timediff=now-self.LastRender.pop()
        self.LastRender.insert(0,now)
        timediff/=(len(self.LastRender))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(self.shift.x,self.shift.y,-self.dist)
        p,s,c=self.updater()
        for i in range(0,len(p)):
            glTranslatef(p[i][0], p[i][1], 0)
            glBegin(GL_POLYGON)
            glColor3f(c[i][0],c[i][1],c[i][2])
            r=s[i]/self.scale
            for j in range(0,360):
                a=j*np.pi/180.0
                x=np.cos(a)*r
                y=np.sin(a)*r
                glVertex3f(x, y, 0.0)
            glEnd()
            glTranslatef(-p[i][0], -p[i][1], 0)
        glTranslatef(-self.shift.x,-self.shift.y,self.dist)

        glColor3f(1,1,1)
        glWindowPos2i(0,self.Height-18)
        glutBitmapString(OpenGL.GLUT.GLUT_BITMAP_HELVETICA_18,bytes("%5.2f FPS" % (1000000.0/timediff.microseconds),'utf-8'))
        glutSwapBuffers()

    def keyPressed(self, *args):
        k=args[0]
        if k == Keys.Escape.value:
            sys.exit()
        elif k == Keys.Up.value:
            self.shift.y-=self.dist/10.0
        elif k == Keys.Down.value:
            self.shift.y+=self.dist/10.0
        elif k == Keys.Left.value:
            self.shift.x+=self.dist/10.0
        elif k == Keys.Right.value:
            self.shift.x-=self.dist/10.0
        elif k == Keys.ZoomIn.value:
            if self.dist>1:
                self.dist//=2
        elif k == Keys.ZoomOut.value:
            if self.dist<1024:
                self.dist*=2
