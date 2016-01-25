#author: b8horpet

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Graphics.SurfaceCommon import Surface
import numpy as np
from enum import  Enum
import sys


class Keys(Enum):
    Escape = b'\x1b'


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:
            Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def keyPressed(*args):
    if args[0] == Keys.Escape.value:
        sys.exit()


class OpenGL2DSurface(Surface.SurfaceInterface):
    def __init__(self,u):
        self.window=0
        self.updater=u
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(0, 0)
        self.window = glutCreateWindow(b"Genesis")
        glutDisplayFunc(Surface.renderfunctor(self,OpenGL2DSurface.DrawGLScene))
        #glutFullScreen()
        glutIdleFunc(Surface.renderfunctor(self,OpenGL2DSurface.DrawGLScene))
        glutReshapeFunc(ReSizeGLScene)
        glutKeyboardFunc(keyPressed)
        InitGL(640, 480)

    def StartRender(self):
        glutMainLoop()

    def DrawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        scale=1.0
        dist=20.0
        p,s,c=self.updater()
        for i in range(0,len(p)):
            glTranslatef(p[i][0]/scale, p[i][1]/scale, -dist)
            glBegin(GL_POLYGON)
            glColor3f(c[i][0],c[i][1],c[i][2])
            r=s[i]/scale
            for j in range(0,360):
                a=j*np.pi/180.0
                x=np.cos(a)*r
                y=np.sin(a)*r
                glVertex3f(x, y, 0.0)
            glEnd()
            glTranslatef(p[i][0]/-scale, p[i][1]/-scale, dist)

        glutSwapBuffers()
